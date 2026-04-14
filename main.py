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
    player1 = player1_type(0.5)
    player2 = player2_type(0.5)
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
    run_benchmark(p1_type, p2_type, 50)

    # Benchmark Results:

    # Lamda 0.01
    # 14975 29395 1 49 0
    # 28750 14465 50 0 0

    # Lamda 0.25
    # 29640 11600 50 0 0
    # 11515 30210 0 50 0

    # Lamda 0.5
    # Simple Model Goes First
    # 5850 15495 0 25 0
    # 5225 15060 0 25 0
    # Advanced model goes first
    # 14455 5355 25 0 0
    # 15060 5550 25 0 0

    # Lamda 0.75
    # 11130 29575 0 50 0
    # 29600 10795 50 0 0

    # Lamda 0.99
    # 29775 10120 50 0 0
    # 10990 29620 0 50 0


    # n=1
    # 10805 29750 0 50 0
    # 29955 11850 50 0 0

    # n=5
    # 30475 11520 50 0 0
    # 10110 30095 0 50 0

    # n=25
    # 11355 29990 0 50 0
    # 29585 11435 50 0 0

    # n=100
    # 29355 10425 50 0 0
    # 10540 30130 0 50 0
