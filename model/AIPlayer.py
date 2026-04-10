import random

from model import Helpers
from model.Card import MeldType
from model.Player import Player

class AIPlayer(Player):
  def have_player_draw(self, game, epsilon, decay):
    index_result = []

    indices = [-1]
    indices.extend(game.get_legal_discard_draws())

    for draw in indices:
      game_copy = game.deepcopy(game)
      if draw == -1:
        game_copy.draw_card()
      else:
        game_copy.draw_card(draw)
      index_result.append((draw, self.get_state_equity(game_copy)))

    return self.make_choice(index_result, epsilon, decay)

  def have_player_act(self, game, epsilon, decay):
    action_result = []

    game_copy = game.deepcopy(game)
    action_result.append((None, self.get_state_equity(game_copy)))

    set_cards = [card for meld in self.melds if meld.meld_type == MeldType.SET for card in meld.cards]
    run_cards = [card for meld in self.melds if meld.meld_type == MeldType.RUN for card in meld.cards]
    for meld in Helpers.get_all_possible_melds(game.players_turn.hand, set_cards, run_cards)():
        game_copy = game.deepcopy(game)
        game_copy.play_meld(meld[0])
        # TODO: Multiply this by the coefficient to disincentive playing early
        equity = self.get_state_equity(game_copy)
        action_result.append(((meld[0], meld[1]), equity))

    for card in game.players_turn.hand:
      possible_melds = game.can_play_cards([card])
      for meld in possible_melds:
        game_copy = game.deepcopy(game)
        game_copy.play_cards([card], meld.meld_type)
        # TODO: Multiply this by the coefficient to disincentive playing early
        equity = self.get_state_equity(game_copy)
        action_result.append((([card]), equity))

    return self.make_choice(action_result, epsilon, decay)

  def have_player_discard(self, game, epsilon, decay):
    index_result = []

    for discard in range(len(game.players_turn.hand)):
      game_copy = game.deepcopy(game)
      game_copy.discard(discard)
      index_result.append((discard, self.get_state_equity(game_copy)))

    return self.make_choice(index_result, epsilon, decay)

  def make_choice(self, index_result, epsilon, decay):
    index_result.sort(key=lambda x: x[1], reverse=True)

    weights = []
    for weight in range(len(index_result)):
      weights.append(epsilon * decay ** weight)

    choice = random.choices(index_result, weights=weights)[0]

    return choice

  def get_state_equity(self, game):
    melded_value = self.get_melded_value(game)
    max_melded_value = self.get_max_melded_value(game)
    expected_deadwood_value = 0
    return melded_value + max_melded_value - expected_deadwood_value

  def get_melded_value(self, game):
    melded_value = 0
    for card in game.players_turn.played_cards:
      melded_value += card.rank
    return melded_value

  def get_max_melded_value(self, game):
    max_melded_value = 0
    for card in game.players_turn.hand:
      max_melded_value += card.rank
    return max_melded_value

  def get_expected_deadwood_value(self, game):
    deadwood_value = 0
    for card in game.players_turn.hand:
      deadwood_value += card.rank * (1 - self.prob_card_played(card, game))
    return deadwood_value

  def expected_number_of_turns(self, game):
    if game.players_turn == game.player1:
      opponent = game.player2
    else:
      opponent = game.player1

    number_hidden_cards = len(game.deck) + len(opponent.hand) - len(opponent.visible_hand)
    conservative_estimated_num_turns = min(len(game.deck), len(opponent.hand), len(game.players_turn.hand)) / 2
    return number_hidden_cards, conservative_estimated_num_turns

  def prob_card_played(self, card, game):
    if game.player_can_play_card(card):
      return 1.0

    cards_of_rank = 0
    for hand_card in [game.players_turn.hand, game.discard_pile]:
      if hand_card.rank == card.rank and hand_card.suit != card.suit:
        cards_of_rank += 1

    cards_one_away = 0
    cards_two_away = 0
    for hand_card in [game.players_turn.hand, game.discard_pile]:
      if hand_card.suit == card.suit and abs(hand_card.rank - card.rank) == 1:
        cards_one_away += 1
      elif hand_card.suit == card.suit and abs(hand_card.rank - card.rank) == 2:
        cards_two_away += 1

    def prob_get_one_out(outs, hidden_cards, turns):
      if outs >= hidden_cards:
        return 1.0
      prob_miss_outs = 0
      for turn in range(int(turns)):
        prob_miss_outs *= max(0, hidden_cards - outs - turn) / max(1, hidden_cards - turn)
      return 1 - prob_miss_outs

    prob_set = 0
    prob_outside_run = 0
    prob_inside_run = 0
    prob_backdoor_run = 0

    num_hidden_cards, est_num_turns = self.expected_number_of_turns(game)

    prob_three_out = prob_get_one_out(3, num_hidden_cards, est_num_turns)
    prob_two_out = prob_get_one_out(2, num_hidden_cards, est_num_turns)
    prob_one_out = prob_get_one_out(1, num_hidden_cards, est_num_turns)

    if cards_of_rank == 1:
      prob_set = prob_three_out * prob_two_out
    elif cards_of_rank == 2:
      prob_set = prob_two_out
    elif cards_of_rank == 3 or cards_of_rank == 4:
      prob_set = 1.0

    if cards_one_away == 1:
      prob_outside_run = prob_two_out
    elif cards_one_away == 2:
      prob_outside_run = 1.0

    if cards_two_away == 1 or cards_two_away == 2:
      prob_inside_run = prob_one_out

    if cards_one_away == 0 and cards_two_away == 0:
      prob_backdoor_run = prob_two_out * prob_three_out

    prob_gets_played = 1 - (1 - prob_set) * (1 - prob_outside_run) * (1 - prob_inside_run) * (1 - prob_backdoor_run)
    return min(prob_gets_played, 1.0)