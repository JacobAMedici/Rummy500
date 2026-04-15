from model.Card import *

# Possible scores based on rank
RANK_SCORE = {
  Rank.TWO: 5,
  Rank.THREE: 5,
  Rank.FOUR: 5,
  Rank.FIVE: 5,
  Rank.SIX: 5,
  Rank.SEVEN: 5,
  Rank.EIGHT: 5,
  Rank.NINE: 5,
  Rank.TEN: 10,
  Rank.JACK: 10,
  Rank.QUEEN: 10,
  Rank.KING: 10,
  Rank.ACE: 15
}

# Total the score of the player at the end of the round and add it to their total score
def tally_scores(player):
  score = 0

  for card in player.played_cards:
    score += RANK_SCORE[card.rank]
  for card in player.hand:
    score -= RANK_SCORE[card.rank]

  player.score += score


# Get all possible melds based off the player's hand and the current state
def get_all_possible_melds(unmelded_cards, set_cards, run_cards):
  possible_melds = []

  total_set_cards = unmelded_cards + set_cards
  for rank in Rank:
    cards_of_rank = [card for card in total_set_cards if card.rank == rank]
    if len(cards_of_rank) >= 3:
      possible_melds.append((cards_of_rank, MeldType.SET))
      if len(cards_of_rank) == 4:
        for excluded_index in range(4):
          three_card_meld = []
          for card_index, card in enumerate(cards_of_rank):
            if card_index != excluded_index:
              three_card_meld.append(card)
          possible_melds.append((three_card_meld, MeldType.SET))

  total_run_cards = unmelded_cards + run_cards
  for suit in Suit:
    suited_cards = [card for card in total_run_cards if card.suit == suit]
    card_array = [False] * 14
    for card in suited_cards:
      if card.rank == Rank.ACE:
        card_array[0] = True
        card_array[13] = True
      else:
        card_array[card.rank - 1] = True

    for meld_size in range(13, 2, -1):
      for period in range(15 - meld_size):
        window = card_array[period:period + meld_size]
        if all(window):
          possible_meld = []
          for card in suited_cards:
            if card.rank == Rank.ACE:
                position = 0 if period == 0 else 13
            else:
                position = card.rank - 1
            if period <= position < period + meld_size:
              possible_meld.append(card)
          possible_melds.append((possible_meld, MeldType.RUN))

  return possible_melds

