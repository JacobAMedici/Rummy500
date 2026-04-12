import sys
from model.AIPlayer import AIPlayer
from controller.GameController import create_app
from model.Player import Player

MODES = {
  'hh': (Player, Player),
  'ha': (Player, AIPlayer),
  'ah': (AIPlayer, Player),
  'aa': (AIPlayer, AIPlayer)
}

def run_game(player1_type, player2_type):
  player1 = player1_type()
  player2 = player2_type()

  app = create_app(player1, player2)
  app.run(debug=True)

if __name__ == '__main__':
  mode = sys.argv[1] if len(sys.argv) > 1 else 'hh'

  if mode not in MODES:
    exit()

  p1_type, p2_type = MODES[mode]
  run_game(p1_type, p2_type)