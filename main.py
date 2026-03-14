from HumanPlayer import HumanPlayer
from Display import Display
from Game import Game

# TODO: implement the following comment
# Player1 is the first dealer (so in the first round they go second) and it switches each round
player1 = HumanPlayer()
player2 = HumanPlayer()
display = Display()
display.start()
dealer = player1

while player1.score < 500 and player2.score < 500:
  game = Game(player1, player2, display)

display.stop()

if player1.score < player2.score:
  print("Player 2 Wins!")
else:
  print("Player 1 Wins!")