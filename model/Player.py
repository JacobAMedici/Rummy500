from abc import ABC, abstractmethod

# This is the general form of the player that the human player uses and other player classes inherit from
class Player(ABC):
  def __init__(self):
    self.played_cards = []
    self.hand = []
    self.melds = []
    # Visible hand just clarifies which cards the other player knows if they are tracking their draws
    self.visible_hand = []
    self.score = 0


  # At the start of the new game, reset the player's info, except for score
  def new_game(self):
    self.played_cards = []
    self.hand = []
    self.melds = []
    self.visible_hand = []

  # Add a card to the player's hand
  def append_player_card(self, card):
    self.hand.append(card)