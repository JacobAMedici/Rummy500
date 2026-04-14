from model.Game import Game
from model.AIPlayer import AIPlayer

class NoViewGameController:
  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2
    self.winner = None


  def play_game(self):
    while self.player1.score < 500 and self.player2.score < 500:
      self.player1.new_game()
      self.player2.new_game()
      self.play_round()
    return self.player1.score, self.player2.score


  def play_round(self):
    game = Game(self.player1, self.player2)
    while not game.check_round_over():
      AIPlayer.handle_AI_turn(game)
