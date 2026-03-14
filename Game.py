import time

from Helpers import tally_scores
from Card import *

class Game:
  def __init__(self, player1, player2, display):
    self.player1 = player1
    self.player2 = player2
    self.display = display
    self.deck = Deck()
    self.deck.shuffle()
    self.discard_pile = []
    self.players_turn = player1
    # Give each player 13 cards
    for cardNum in range(1, 14):
      self.player2.append_player_card(self.deck.pop())
      self.player1.append_player_card(self.deck.pop())
    self.discard_pile.append(self.deck.pop())
    self.start_round()

  def start_round(self):
    round_over = False
    while not round_over:
      self.display.render(self)
      if self.display:
        time.sleep(0.02)
      self.handle_draw(self.players_turn)
      self.handle_action(self.players_turn)
      self.handle_discard(self.players_turn)
      if self.check_round_over():
        round_over = True
        tally_scores(self.player1)
        tally_scores(self.player2)
      else:
        if self.players_turn == self.player1:
          self.players_turn = self.player2
        else:
          self.players_turn = self.player1

  def handle_draw(self, player):
    pass

  def handle_action(self, player):
    pass

  def handle_discard(self, player):
    pass

  def check_round_over(self):
    pass

  # Check if it can be played off of current melds for the current player
  def can_play_card_set(self, card):
    pass

  # Check if it can be played off of current melds for the current player
  def can_play_card_run(self, card):
    pass

  def discard_card(self, card_index):
    self.discard_pile.append(self.players_turn.pop(card_index))