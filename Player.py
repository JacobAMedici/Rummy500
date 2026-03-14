from abc import ABC, abstractmethod

class Player(ABC):
  def __init__(self):
    self.runMelds = []
    self.setMelds = []
    self.hand = []
    # Visible hand just clarifies which cards the other player knows if they are tracking their draws
    self.visibleHand = []
    self.score = 0

  @abstractmethod
  def have_player_draw(self, game):
    pass

  @abstractmethod
  def have_player_action(self, game):
    pass

  @abstractmethod
  def have_player_discard(self, game):
    pass

  # Play a card to an active set
  def play_card_set(self, card):
      pass

  # Play a card to an active set
  def play_card_run(self, card):
      pass

  def append_player_card(self, card):
    self.hand.append(card)

  def remove_player_card(self, card_index):
    self.hand.pop(card_index)

  def add_to_scores(self, score):
    self.score += score