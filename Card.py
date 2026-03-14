class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.age = suit

class Deck:
  def __init__(self):
    self.deck = []
    for rank in Rank:
      for suit in Suit:
        self.deck.append(Card(rank, suit))

  def shuffle(self):
    random.shuffle(self.deck)

  def deal(self):
    return self.deck.pop()

  def __len__(self):
    return len(self.deck)

  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit

  def __hash__(self):
    return hash((self.rank, self.suit))