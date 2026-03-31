from model.Player import Player

class HumanPlayer(Player):
  def have_player_draw(self, game):
    while True:
      choice = game.display.prompt("Write '-1' to drop from the deck, write 0 to n to draw from the discards: ", game)
      try:
        index = int(choice)
        if index == -1:
          self.hand.append(game.deck.pop())
          break
        elif 0 <= index < len(game.discard_pile):
          actual_index = len(game.discard_pile) - 1 - index
          self.hand.append(game.discard_pile.pop(actual_index))
          break
      except ValueError:
        pass

  def have_player_act(self, game):
    pass

  def have_player_discard(self, game):
    pass