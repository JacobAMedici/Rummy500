from HumanPlayer import HumanPlayer
from Display import Display
from Game import Game

player1 = HumanPlayer()
player2 = HumanPlayer()

while (player1.score < 500 and player2.score < 500):
  display = Display()
  game = Game(player1, player2)
  display.render(game)