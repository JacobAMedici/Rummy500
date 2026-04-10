from model.Card import *

def tally_scores(player):
  score = 0

  rank_score = {
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

  for meld in player.played_cards:
    for card in meld.cards:
      score += rank_score[card]

  player.score += score


def get_all_possible_melds(unmelded_cards, set_cards, run_cards):
  possible_melds = []

  total_set_cards = unmelded_cards + set_cards
  for rank in Rank:
    cards_of_rank = [card for card in total_set_cards if card.rank == rank]
    if len(cards_of_rank) >= 3:
      card_indices = [index for index, card in enumerate(total_set_cards) if card in cards_of_rank]
      possible_melds.append((card_indices, MeldType.SET))

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
      for period in range(14 - meld_size):
        window = card_array[period:period + meld_size]
        if all(window):
          possible_meld = []
          for index in range(period, period + meld_size + 1):
            possible_meld.append(index)
          possible_melds.append((possible_meld, MeldType.RUN))

  return possible_melds
