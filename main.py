import sys
from model.AdvancedAIPlayer import AdvancedAIPlayer
from controller.ViewGameController import create_app
from model.Player import Player
from model.SimpleAIPlayer import SimpleAIPlayer
from controller.NoViewGameController import NoViewGameController


MODES = {
  'hh': (Player, Player),
  'ha': (Player, AdvancedAIPlayer),
  'ah': (AdvancedAIPlayer, Player),
  'aa': (AdvancedAIPlayer, AdvancedAIPlayer),
  'benchmark': (SimpleAIPlayer, AdvancedAIPlayer)
}


def run_game(player1_type, player2_type):
  player1 = player1_type()
  player2 = player2_type()

  app = create_app(player1, player2)
  app.run(debug=True)


def run_benchmark(player1_type, player2_type, number_of_games):
  simple_score = 0
  advanced_score = 0
  simple_win = 0
  advanced_win = 0
  ties = 0

  for game_num in range(number_of_games):
    print("Game num: ", game_num)
    player1 = player1_type()
    player2 = player2_type()
    game_controller = NoViewGameController(player1, player2)
    player1_score, player2_score = game_controller.play_game()
    simple_score += player1_score
    advanced_score += player2_score
    if player1_score > player2_score:
      simple_win += 1
    elif player1_score < player2_score:
      advanced_win += 1
    else:
      ties += 1
    print("Player 1 score: ", player1_score)
    print("Player 2 score: ", player2_score)

  print(simple_score, advanced_score, simple_win, advanced_win, ties)



if __name__ == '__main__':
  mode = sys.argv[1] if len(sys.argv) > 1 else 'hh'

  if mode not in MODES:
    exit()

  p1_type, p2_type = MODES[mode]
  if mode in ('hh', 'ha', 'ah', 'aa'):
    run_game(p1_type, p2_type)
  else:
    run_benchmark(p2_type, p1_type, 25)
    # Simple Model Goes First
    # 5850 15495 0 25 0
    # 5225 15060 0 25 0
    # Advanced model goes first
    # 14455 5355 25 0 0
    # 15060 5550 25 0 0
