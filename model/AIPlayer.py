from abc import abstractmethod

from model.Player import Player

# This is the class that the two AI Players inherit from
class AIPlayer(Player):
  def __init__(self, lamda = 1):
    super().__init__()
    self.lamda = lamda

  @abstractmethod
  def have_player_draw(self, game):
    pass


  @abstractmethod
  def have_player_act(self, game):
    pass


  @abstractmethod
  def have_player_discard(self, game):
    pass


  @staticmethod
  def handle_AI_turn(game):
    # Handle Draw Phase
    while True:
      draw_index = game.players_turn.have_player_draw(game)
      if draw_index == -1:
        game.draw_from_deck()
        break
      else:
        if game.draw_from_discard(draw_index):
          break

    # Handle action phase
    while True:
      action = game.players_turn.have_player_act(game)
      if action is None:
        if not game.done_acting():
          continue
        if game.phase == 'discard':
          break
      else:
        try:
          game.play_cards(action[0], action[1])
        except ValueError as e:
          if str(e) == 'Not enough cards to discard':
            game.player_must_use = None
            game.done_acting()
            break

    # Handle discard phase
    while True:
      discard_index = game.players_turn.have_player_discard(game)
      if game.discard(discard_index):
        break