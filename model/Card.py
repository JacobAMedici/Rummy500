import random
from enum import IntEnum, Enum

# Possible ranks and corresponding values for cards
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


# Possible suits for cards
class Suit(Enum):
  CLUBS = "Clubs"
  DIAMONDS = "Diamonds"
  HEARTS = "Hearts"
  SPADES = "Spades"


# Possible types of melds
class MeldType(Enum):
  SET = "Set"
  RUN = "Run"
  INVALID = "Invalid"


# Defines the card object used to store rank and suit data
class Card:
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  # Get the string of the card, return the value
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


  # Check if a card has the same suit and rank, return the boolean result
  def __eq__(self, other):
    if not isinstance(other, Card):
      return False
    return self.rank == other.rank and self.suit == other.suit


  def __hash__(self):
    return hash((self.rank, self.suit))


# Represent the collection of cards in the hidden deck
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


 # Check if a set of cards forms a valid meld, return the boolean result and resulting type
def is_valid_meld(cards):
  if len(cards) < 3:
    return False, MeldType.INVALID

  for card in cards:
    if isinstance(card, int):
      print(cards)

  if len({card.rank for card in cards}) == 1:
    return True, MeldType.SET

  if len({card.suit for card in cards}) == 1:
    ranks = [card.rank for card in cards]
    min_rank = min(ranks)
    if Rank.ACE in ranks and min_rank == Rank.TWO:
      ranks.remove(Rank.ACE)
    max_rank = max(ranks)
    if max_rank - min_rank == len(set(ranks)) - 1:
      return True, MeldType.RUN

  return False, MeldType.INVALID


# Represents a meld, holding cards and a type
class Meld:
  def __init__(self, cards):
    self.cards = cards
    validity_result, meld_type = is_valid_meld(cards)
    if not validity_result:
      raise Exception("Invalid Meld")
    self.meld_type = meld_type


  # Check to see if you can add a card to the meld
  def accepts(self, new_cards):
    return is_valid_meld(self.cards + new_cards)[0]


  # Add a card to the meld
  def add(self, new_cards):
    if is_valid_meld(self.cards + new_cards):
      self.cards.extend(new_cards)


  def __str__(self):
    sorted_cards = sorted(self.cards, key=lambda card: card.rank)
    return ' '.join(str(card) for card in sorted_cards)