import random
from enum import IntEnum, Enum

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

class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__(self):
    suit_symbols = {
      Suit.SPADES: '♠',
      Suit.HEARTS: '♥',
      Suit.DIAMONDS: '♦',
      Suit.CLUBS: '♣'
    }
    rank_letters = {
      Rank.TWO: '2',
      Rank.THREE: '3',
      Rank.FOUR: '4',
      Rank.FIVE: '5',
      Rank.SIX: '6',
      Rank.SEVEN: '7',
      Rank.EIGHT: '8',
      Rank.NINE: '9',
      Rank.TEN: 'T',
      Rank.JACK: 'J',
      Rank.QUEEN: 'Q',
      Rank.KING: 'K',
      Rank.ACE: 'A'
    }
    return f"{rank_letters[self.rank]}{suit_symbols[self.suit]}"

  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit

  def __hash__(self):
    return hash((self.rank, self.suit))

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

  def pop(self):
    return self.deck.pop()