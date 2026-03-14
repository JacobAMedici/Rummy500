from Card import *

class Game:
  def __init__(self, player1, player2):
    self.deck = Deck()
    self.deck.shuffle()
    self.discardPile = []
    self.discardPile.append(self.deck.pop())
    self.player1 = player1
    self.player2 = player2
    self.gameOver = False
    self.playersTurn = player1
    # Give each player 13 cards
    for cardNum in range(1, 14):
      self.player2.appendPlayerCard(self.deck.pop())
      self.player1.appendPlayerCard(self.pop())
    self.startGame()

  def startRound(self):
    roundOver = False
    while (not roundOver):
      # Wait for current player to make their draw
      # Wait for current player to play
      # Wait for current player to discard
      # Check if round is over
      # If round is over, then tally the scores and record them
      # Check if the game is over
      pass

  # Check if it can be played off of current melds for the current player
  def canPlayCardSet(self, card):
    pass

  # Check if it can be played off of current melds for the current player
  def canPlayCardRun(self, card):
    pass

  def discardCard(self, cardIndex):
    discardPile.append(self.playersTurn.pop(cardIndex))