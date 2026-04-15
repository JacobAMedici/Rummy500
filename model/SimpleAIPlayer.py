import random

from model import Helpers
from model.AIPlayer import AIPlayer

# The simple baseline AI used to evaluate the advanced AI
class SimpleAIPlayer(AIPlayer):
  # Return -1 to always draw from the deck
  def have_player_draw(self, game):
    return -1


  # Get the indices of the chosen cards to play or None to skip
  def have_player_act(self, game):
    actions = []
    actions.append(None)

    for meld in Helpers.get_all_possible_melds(game.players_turn.hand, [], []):
      card_indices = [game.players_turn.hand.index(card) for card in meld[0]]
      actions.append((card_indices, meld[1]))

    for card_index in range(len(game.players_turn.hand)):
      for meld in game.can_play_cards([game.players_turn.hand[card_index]]):
        actions.append(([card_index], meld.meld_type))

    return random.choice(actions)

  # Have the player choose which card to discard
  def have_player_discard(self, game):
    return random.randint(0, len(game.players_turn.hand) - 1)