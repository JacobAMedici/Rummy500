from enum import IntEnum, Enum

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.age = suit

  def __str__(self):
    SUIT_SYMBOLS = {
      SPADES: '♠',
      HEARTS: '♥',
      DIAMONDS: '♦',
      CLUBS: '♣'
    }
    RANK_LETTERS = {
      TWO: '2',
      THREE: '3',
      FOUR: '4',
      FIVE: '5',
      SIX: '6',
      SEVEN: '7',
      EIGHT: '8',
      NINE: '9',
      TEN: 'T',
      JACK: 'J',
      QUEEN: 'Q',
      KING: 'K',
      ACE: 'A'
    }
    return f"{RANK_LETTERS[self.rank]}{SUIT_SYMBOLS[self.suit]}"

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

  def pop(self):
    return self.deck.pop()


class Rank(IntEnum):
  TWO = 2
  THREE = 3
  FOUR = 4
  FIVE = 5
  SIX = 6
  SEVEN = 7
  EIGHT = 8
  NINE = 9
  TEN = 10
  JACK = 11
  QUEEN = 12
  KING = 13
  ACE = 14

class Suit(Enum):
  CLUBS = "Clubs"
  DIAMONDS = "Diamonds"
  HEARTS = "Hearts"
  SPADES = "Spades"