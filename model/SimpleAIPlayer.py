import random

from model import Helpers
from model.AIPlayer import AIPlayer

class SimpleAIPlayer(AIPlayer):
  def have_player_draw(self, game, epsilon, decay):
    return -1

  def have_player_act(self, game, epsilon, decay):
    actions = [None]
    for meld in Helpers.get_all_possible_melds(game.players_turn.hand, [], []):
      card_indices = [game.players_turn.hand.index(card) for card in meld[0]]
      actions.append((card_indices, meld[1]))

    for card_index in range(len(game.players_turn.hand)):
      for meld in game.can_play_cards([game.players_turn.hand[card_index]]):
        actions.append(([card_index], meld.meld_type))

    return random.choice(actions)

  def have_player_discard(self, game, epsilon, decay):
    return random.randint(0, len(game.players_turn.hand) - 1)