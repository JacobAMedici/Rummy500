import sys
from model.Game import Game
from model.HumanPlayer import HumanPlayer
from model.AIPlayer import AIPlayer
from controller.GameController import create_app

MODES = {
  'hh': (HumanPlayer, HumanPlayer),
  'ha': (HumanPlayer, AIPlayer),
  'aa': (AIPlayer, AIPlayer)
}

def run_game(player1_type, player2_type):
  player1 = player1_type()
  player2 = player2_type()
  needs_flask = isinstance(player1, HumanPlayer) or isinstance(player2, HumanPlayer)

  if needs_flask:
    app = create_app(player1, player2)
    app.run(debug=True)
  else:
    while player1.score < 500 and player2.score < 500:
      game = Game(player1, player2)
      while not game.check_round_over():
        # TODO: Add logic for AI vs AI (This will be used the most)
        pass

if __name__ == '__main__':
  mode = sys.argv[1] if len(sys.argv) > 1 else 'hh'

  if mode not in MODES:
    exit()

  p1_type, p2_type = MODES[mode]
  run_game(p1_type, p2_type)