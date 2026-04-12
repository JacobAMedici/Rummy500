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

  for card in player.played_cards:
    score += rank_score[card.rank]
  for card in player.hand:
    score -= rank_score[card.rank]

  player.score += score


def get_all_possible_melds(unmelded_cards, set_cards, run_cards):
  possible_melds = []

  total_set_cards = unmelded_cards + set_cards
  for rank in Rank:
    cards_of_rank = [card for card in total_set_cards if card.rank == rank]
    if len(cards_of_rank) >= 3:
      possible_melds.append((cards_of_rank, MeldType.SET))

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
            #TODO: Fix this :)
            position = 0 if card.rank == Rank.ACE and period == 0 else (13 if card.rank == Rank.ACE else card.rank - 1)
            if period <= position < period + meld_size:
              possible_meld.append(card)
          possible_melds.append((possible_meld, MeldType.RUN))

  return possible_melds

def handle_AI_turn(game):
  while True:
    draw_index = game.players_turn.have_player_draw(game, 0.9, 0.5)
    if draw_index == -1:
      if game.draw_from_deck():
        break
      else:
        break
    else:
      if game.draw_from_discard(draw_index):
        break

  while True:
    action = game.players_turn.have_player_act(game, 0.9, 0.5)
    if action is None:
      if not game.done_acting():
        continue
      if game.phase == 'discard':
        break
    else:
      try:
        game.play_cards(action[0], action[1])
      except ValueError as e:
        if str(e) == 'Not enough cards to discard':
          game.player_must_use = None
          game.done_acting()
          break

  while True:
    discard_index = game.players_turn.have_player_discard(game, 0.9, 0.5)
    if game.discard(discard_index):
      break

