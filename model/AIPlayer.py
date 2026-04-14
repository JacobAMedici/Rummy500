from abc import abstractmethod

from model.Player import Player

class AIPlayer(Player):
  @abstractmethod
  def have_player_draw(self, game, epsilon, decay):
    pass


  @abstractmethod
  def have_player_act(self, game, epsilon, decay):
    pass


  @abstractmethod
  def have_player_discard(self, game, epsilon, decay):
    pass


  @staticmethod
  def handle_AI_turn(game):
    while True:
      draw_index = game.players_turn.have_player_draw(game, 0.9, 0.5)
      if draw_index == -1:
        game.draw_from_deck()
        break
      else:
        if game.draw_from_discard(draw_index):
          break

    while True:
      action = game.players_turn.have_player_act(game, 0.9, 0.5)
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

    while True:
      discard_index = game.players_turn.have_player_discard(game, 0.9, 0.5)
      if game.discard(discard_index):
        break