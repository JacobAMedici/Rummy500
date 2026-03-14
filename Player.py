class Player:
  def __init__(self):
    self.runMelds = []
    self.setMelds = []
    self.hand = []
    self.visibleHand = []
    self.score = 0
    self.humanPlayer = False

  # Return -1 to draw from the stack, return the index of the desired card to draw from discard
  def getDrawAction(self):
    # Choose the best draw action
    pass

  # Lets the player take the actions that they wish to take
  def performMeldActions(self):
    # Choose the best meld action(s)
    pass

  # Return the index of the card that the player wishes to discard
  def getDiscardAction(self):
    # Choose the best card to discard
    pass

  def appendPlayerCard(self, card):
    self.hand.append(card)

  def removePlayerCard(self, cardIndex):
    self.hand.pop(card)

  # Check if it can be played off of current melds for both players and play it, otherwise throw an error
  def playCard(self, cardIndex):
    pass

  def findAllDrawActions(self):
    pass

  def findAllMeldActions(self):
    pass

  # Play a card to an active set
  def playCardSet(self, card):
    if (self.canPlayCard(card)):
      pass

  # Play a card to an active set
  def playCardRun(self, card):
    if (self.canPlayCard(card)):
      pass