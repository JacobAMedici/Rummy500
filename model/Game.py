import copy

from model.Helpers import tally_scores, get_all_possible_melds
from model.Card import *

class Game:
  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2
    self.melds = []
    self.deck = Deck()
    self.deck.shuffle()
    self.discard_pile = []
    self.players_turn = player1
    self.phase = 'draw'
    for cardNum in range(1, 14):
      self.player2.append_player_card(self.deck.pop())
      self.player1.append_player_card(self.deck.pop())
    self.discard_pile.append(self.deck.pop())
    self.player1.hand.sort(key=lambda x: (x.rank, x.suit.name))
    self.player2.hand.sort(key=lambda x: (x.rank, x.suit.name))
    self.player_must_use = None

  def discard(self, index):
    try:
      self.discard_pile.append(self.players_turn.hand.pop(index))
      self._change_turn()
      return True
    except IndexError as e:
      return False

  def draw_from_deck(self):
    try:
      card = self.deck.pop()
      self.players_turn.hand.append(card)
      self.phase = 'act'
      self.players_turn.hand.sort(key=lambda x: (x.rank, x.suit.name))
      return True
    except Exception as e:
      print(e)
      return False

  def draw_from_discard(self, index):
    try:
      if index not in self.get_legal_discard_draws():
        return False
      for main_index in range(len(self.discard_pile) - 1, index - 1, -1):
        card = self.discard_pile.pop(main_index)
        self.players_turn.hand.append(card)
        self.players_turn.visible_hand.append(card)
      self.phase = 'act'
      self.player_must_use = self.players_turn.hand[-1]
      self.players_turn.hand.sort(key=lambda x: (x.suit.name, x.rank))
      return True
    except Exception as e:
      print(e)
      return False

  def done_acting(self):
    if self.player_must_use is not None:
      self.phase = 'act'
      return False
    else:
      self.phase = 'discard'
      return True

  def play_cards(self, card_indices, meld_type):
    cards = [self.players_turn.hand[index] for index in card_indices]
    if self.player_must_use and not self.player_must_use in cards:
      raise ValueError("You must use the card you drew")
    if len(cards) >= len(self.players_turn.hand):
      raise ValueError("Not enough cards to discard")
    success = False
    if len(cards) == 1:
      melds = self.can_play_cards(cards)
      for meld in melds:
        if meld.meld_type == meld_type:
          meld.add(cards)
          self.removed_played_cards(cards)
          success = True
          break
    elif len(cards) == 2:
      melds = self.can_play_cards(cards)
      if melds:
        meld = melds[0]
        meld.add(cards)
        self.removed_played_cards(cards)
        success = True
    else:
      try:
        possible_meld = Meld(cards)
        self.melds.append(possible_meld)
        self.removed_played_cards(cards)
        success = True
      except Exception as e:
        print(e)
    if success:
      for card in cards:
        self.players_turn.played_cards.append(card)
      self.player_must_use = None

  def removed_played_cards(self, cards):
    for card in cards:
      self.players_turn.hand.remove(card)
      try:
        card_index = self.players_turn.visible_hand.index(card)
        self.players_turn.visible_hand.pop(card_index)
      except ValueError or IndexError as e:
        pass

  def _change_turn(self):
    if self.players_turn == self.player1:
      self.players_turn = self.player2
    else:
      self.players_turn = self.player1
    self.phase = 'draw'

  def check_round_over(self):
    if len(self.player1.hand) == 0 or len(self.player2.hand) == 0 or len(self.deck) == 0:
      tally_scores(self.player1)
      tally_scores(self.player2)
      return True
    return False

  def get_legal_discard_draws(self):
    legal_draws = []
    player = copy.deepcopy(self.players_turn)
    for main_index in range(len(self.discard_pile) - 1, -1, -1):
      if self.player_can_play_card(player, self.discard_pile[main_index]):
        legal_draws.append(main_index)
      player.hand.append(self.discard_pile[main_index])

    return legal_draws

  def player_can_play_card(self, player, card):
    for meld in self.melds:
      if meld.accepts([card]):
        return True
    potential_player_hand = player.hand.copy()
    potential_player_hand.append(card)
    set_cards = [card for meld in self.melds if meld.meld_type == MeldType.SET for card in meld.cards]
    run_cards = [card for meld in self.melds if meld.meld_type == MeldType.RUN for card in meld.cards]
    all_melds = get_all_possible_melds(potential_player_hand, set_cards, run_cards)
    all_melds_with_card = [meld for meld in all_melds if card in meld[0]]
    if len(all_melds_with_card) >= 1:
      return True
    else:
      return False

  def can_play_cards(self, cards):
    possible_melds = []
    for meld in self.melds:
      if meld.accepts(cards):
        possible_melds.append(meld)
    return possible_melds