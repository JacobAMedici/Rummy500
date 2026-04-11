from abc import ABC, abstractmethod

class Player(ABC):
  def __init__(self):
    self.played_cards = []
    self.hand = []
    self.melds = []
    # Visible hand just clarifies which cards the other player knows if they are tracking their draws
    self.visible_hand = []
    self.score = 0

  def new_game(self):
    self.played_cards = []
    self.hand = []
    self.melds = []
    self.visible_hand = []

  def append_player_card(self, card):
    self.hand.append(card)

  def remove_player_card(self, card_index):
    self.hand.pop(card_index)

  def add_to_scores(self, score):
    self.score += score