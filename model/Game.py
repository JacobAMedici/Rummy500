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
    self.phase = 'draw'  # phases: draw, act, discard
    for cardNum in range(1, 14):
      self.player2.append_player_card(self.deck.pop())
      self.player1.append_player_card(self.deck.pop())
    self.discard_pile.append(self.deck.pop())
    self.player1.hand.sort(key=lambda x: (x.rank, x.suit.name))
    self.player2.hand.sort(key=lambda x: (x.rank, x.suit.name))

  def discard(self, index):
    self.discard_pile.append(self.players_turn.hand.pop(index))
    self._change_turn()

  def draw_from_deck(self):
    try:
      card = self.deck.pop()
      self.players_turn.hand.append(card)
      self.phase = 'act'
      self.players_turn.hand.sort(key=lambda x: (x.rank, x.suit.name))
    except Exception as e:
      pass

  def draw_from_discard(self, index):
    try:
      for main_index in range(len(self.discard_pile) - 1, index + 1, -1):
        card = self.discard_pile.pop(main_index)
        self.players_turn.hand.append(card)
        self.players_turn.visible_hand.append(card)
      # TODO: Ensure they play that round
      self.phase = 'act'
      self.players_turn.hand.sort(key=lambda x: (x.suit.name, x.rank))
    except Exception as e:
      pass

  def play_cards(self, cards, meld_type):
    if len(cards) == 1:
      melds = self.can_play_cards(cards)
      for meld in melds:
        if meld.meld_type == meld_type:
          meld.add(cards)
          for card in cards:
            self.players_turn.hand.remove(card)
    elif len(cards) == 2:
      melds = self.can_play_cards(cards)
      meld = melds[0]
      meld.add(cards)
      for card in cards:
        self.players_turn.hand.remove(card)
    else:
      try:
        possible_meld = Meld(cards)
        self.melds.append(possible_meld)
        for card in cards:
          self.players_turn.hand.remove(card)
      except Exception as e:
        print(e)
    for card in cards:
      self.players_turn.played_cards.append(card)

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
    for card in self.discard_pile:
      if self.player_can_play_card(self.players_turn, card):
        legal_draws.append(card)
    return legal_draws

  def player_can_play_card(self, player, card):
    for meld in self.melds:
      if meld.accepts(card):
        return True
    potential_player_hand = player.hand.copy()
    potential_player_hand.append(card)
    if len(get_all_possible_melds(potential_player_hand)) > 1:
      return True
    return False

  def can_play_cards(self, cards):
    possible_melds = []
    for meld in self.melds:
      if meld.accepts(cards):
        possible_melds.append(meld)
    return possible_melds