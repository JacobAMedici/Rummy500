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

  def discard(self, index):
    self.discard_pile.append(self.players_turn.hand.pop(index))
    self._change_turn()

  def play_cards(self, cards, meld_type):
    if len(cards) == 1:
      melds = self.can_play_cards(cards)
      meld = melds[0]
      meld.add(cards)
      self.players_turn.hand.append(card for card in cards)
      for meld in melds:
        if meld.meld_type == meld_type:
          meld.add(meld)
    elif len(cards) == 2:
      melds = self.can_play_cards(cards)
      meld = melds[0]
      meld.add(cards)
      self.players_turn.hand.append(card for card in cards)
    else:
      try:
        possible_meld = Meld(cards)
        self.melds.append(possible_meld)
        self.players_turn.hand.append(card for card in cards)
      except Exception as e:
        print(e)

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

  def player_can_play_card(self, player, card):
    for meld in self.melds:
      if meld.accepts(card):
        return True
    potential_player_hand = player.hand
    potential_player_hand.append(card)
    if len(get_all_possible_melds(potential_player_hand)) > 1:
      return True
    return False

  def can_play_cards(self, cards):
    possible_melds = []
    for meld in self.melds:
      if meld.accepts(cards):
        return possible_melds.append(meld)
    return possible_melds