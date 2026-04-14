import copy
import random

from model import Helpers
from model.AIPlayer import AIPlayer

class AdvancedAIPlayer(AIPlayer):
  def have_player_draw(self, game):
    index_result = []

    indices = [-1]
    indices.extend(game.get_legal_discard_draws())

    for draw in indices:
      game_copy = copy.deepcopy(game)
      if draw == -1:
        number_hidden_cards, _ = self._expected_number_of_turns(game_copy)
        total_equity = 0
        for card in self._get_n_hidden_cards(game_copy, number_hidden_cards):
          new_game_copy = copy.deepcopy(game)
          new_game_copy.players_turn.hand.append(card)
          new_game_copy.deck.pop()
          total_equity += self._get_state_equity(new_game_copy)
        if number_hidden_cards <= 0:
          pass
        index_result.append((draw, total_equity / number_hidden_cards))
      else:
        game_copy = copy.deepcopy(game)
        game_copy.draw_from_discard(draw)
      index_result.append((draw, self._get_state_equity(game_copy)))

    return self._make_choice(index_result)


  def have_player_act(self, game):
    action_result = []

    game_copy = copy.deepcopy(game)
    action_result.append((None, self._get_state_equity(game_copy)))

    for meld in Helpers.get_all_possible_melds(game_copy.players_turn.hand, [], []):
        game_copy = copy.deepcopy(game)
        card_indices = [game_copy.players_turn.hand.index(card) for card in meld[0]]
        game_copy.player_must_use = None
        try:
            game_copy.play_cards(card_indices, meld[1])
        except (ValueError, Exception) as e:
            print(e)
            continue
        equity = self._get_state_equity(game_copy)
        action_result.append(((card_indices, meld[1]), equity))

    hand = game.players_turn.hand
    for first_card_index in range(len(hand)):
      for second_card_index in range(first_card_index + 1, len(hand)):
        possible_melds = game.can_play_cards([hand[first_card_index], hand[second_card_index]])
        for meld in possible_melds:
          game_copy = copy.deepcopy(game)
          game_copy.player_must_use = None
          try:
              game_copy.play_cards([first_card_index, second_card_index], meld.meld_type)
          except (ValueError, Exception) as e:
              print(e)
              continue
          equity = self._get_state_equity(game_copy)
          action_result.append((([first_card_index, second_card_index], meld.meld_type), equity))

    for card_index in range(len(game.players_turn.hand)):
      possible_melds = game.can_play_cards([game.players_turn.hand[card_index]])
      for meld in possible_melds:
        game_copy = copy.deepcopy(game)
        game_copy.player_must_use = None
        try:
            game_copy.play_cards([card_index], meld.meld_type)
        except (ValueError, Exception) as e:
            print(e)
            continue
        equity = self._get_state_equity(game_copy)
        action_result.append((([card_index], meld.meld_type), equity))

    if game.player_must_use:
      valid_melds = []
      for action, equity in action_result:
        if action is not None:
          cards_in_action = [game.players_turn.hand[i] for i in action[0]]
          if game.player_must_use in cards_in_action:
            valid_melds.append((action, equity))
      if valid_melds:
        return max(valid_melds, key=lambda x: x[1])[0]
      return None

    return self._make_choice(action_result)


  def have_player_discard(self, game):
    unplayable_index_net_result = []
    playable_index_net_result = []

    for discard in range(len(game.players_turn.hand)):
      game_copy = copy.deepcopy(game)
      monte_carlo_rounds = max(10, 50 - len(game.players_turn.played_cards))
      if game_copy.player_can_play_card(game_copy.players_turn, game_copy.players_turn.hand[discard]):
        game_copy.discard(discard)
        playable_index_net_result.append((discard, self._get_state_equity(game_copy) - self._estimate_opp_equity(game_copy, monte_carlo_rounds)))
      else:
        game_copy.discard(discard)
        unplayable_index_net_result.append((discard, self._get_state_equity(game_copy) - self._estimate_opp_equity(game_copy, monte_carlo_rounds)))

    if unplayable_index_net_result:
      return self._make_choice(unplayable_index_net_result)
    else:
      return self._make_choice(playable_index_net_result)


  @staticmethod
  def _get_n_hidden_cards(game, number_hidden_cards):
    possible_cards = []
    possible_cards.extend(game.deck.deck)
    possible_cards.extend(hidden_card for hidden_card in game.players_turn.hand if hidden_card not in game.players_turn.visible_hand)
    random.shuffle(possible_cards)
    return possible_cards[:number_hidden_cards]


  def _make_choice(self, index_result):
    index_result.sort(key=lambda x: x[1], reverse=True)

    weights = []
    for weight in range(len(index_result)):
      weights.append(self.lamda ** weight)

    choice = random.choices(index_result, weights=weights)[0]

    return choice[0]


  @staticmethod
  def _get_melded_value(game):
    return sum(Helpers.RANK_SCORE[card.rank] for card in game.players_turn.played_cards)


  @staticmethod
  def _get_max_hand_melded_value(game):
    return sum(Helpers.RANK_SCORE[card.rank] for card in game.players_turn.hand)


  @staticmethod
  def _get_opponent(game):
    return game.player2 if game.players_turn == game.player1 else game.player1


  def _expected_number_of_turns(self, game):
    opponent = self._get_opponent(game)
    if len(opponent.visible_hand) > len(opponent.hand):
      pass
    number_hidden_cards = len(game.deck) + len(opponent.hand) - len(opponent.visible_hand)
    conservative_estimated_num_turns = min(len(game.deck), len(opponent.hand), len(game.players_turn.hand)) / 2
    return number_hidden_cards, conservative_estimated_num_turns


  def _prob_card_played(self, card, game):
    if game.player_can_play_card(game.players_turn, card):
      return 1.0

    cards_of_rank = 0
    for hand_card in game.players_turn.hand + game.discard_pile:
      if hand_card.rank == card.rank and hand_card.suit != card.suit:
        cards_of_rank += 1

    cards_one_away = 0
    cards_two_away = 0
    for hand_card in game.players_turn.hand + game.discard_pile:
      if hand_card.suit == card.suit and abs(hand_card.rank - card.rank) == 1:
        cards_one_away += 1
      elif hand_card.suit == card.suit and abs(hand_card.rank - card.rank) == 2:
        cards_two_away += 1

    def prob_get_one_out(outs, hidden_cards, turns):
      if outs >= hidden_cards:
        return 1.0
      prob_miss_outs = 1.0
      for turn in range(int(turns)):
        prob_miss_outs *= max(0, hidden_cards - outs - turn) / max(1, hidden_cards - turn)
      return 1 - prob_miss_outs

    prob_set = 0
    prob_outside_run = 0
    prob_inside_run = 0
    prob_backdoor_run = 0

    num_hidden_cards, est_num_turns = self._expected_number_of_turns(game)

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
      prob_backdoor_run = prob_two_out * prob_two_out + prob_two_out * prob_one_out - prob_two_out * prob_two_out * prob_two_out * prob_one_out

    prob_gets_played = 1 - (1 - prob_set) * (1 - prob_outside_run) * (1 - prob_inside_run) * (1 - prob_backdoor_run)
    return min(prob_gets_played, 1.0)


  def _get_expected_deadwood_value(self, game):
    deadwood_value = 0
    for card in game.players_turn.hand:
      deadwood_value += Helpers.RANK_SCORE[card.rank] * (1 - self._prob_card_played(card, game))
    return deadwood_value


  def _get_state_equity(self, game):
    melded_value = self._get_melded_value(game)
    max_melded_value = self._get_max_hand_melded_value(game)
    expected_deadwood_value = self._get_expected_deadwood_value(game)
    return melded_value + max_melded_value - expected_deadwood_value


  def _estimate_opp_equity(self, game, monte_carlo_rounds):
    equity = []
    # TODO: Revert
    monte_carlo_rounds = 100
    for _ in range(monte_carlo_rounds):
      game_copy = copy.deepcopy(game)
      target_hand_length = len(game_copy.players_turn.hand)
      new_hand = []
      num_hidden_cards = target_hand_length - len(game_copy.players_turn.visible_hand)
      new_hand.extend(self._get_n_hidden_cards(game_copy, num_hidden_cards))
      new_hand.extend(game_copy.players_turn.visible_hand)
      game_copy.players_turn.hand = new_hand
      equity.append(self._get_state_equity(game_copy))
    return sum(equity) / len(equity)
