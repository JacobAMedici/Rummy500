from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
import time

# Used to create the live Display
# https://rich.readthedocs.io/en/latest/live.html
class Display:
  def __init__(self):
    self.console = Console()
    self.live = Live(console=self.console, refresh_per_second=100, transient=False)

  def start(self):
    self.live.start()

  def stop(self):
    self.live.stop()

  def render(self, game):
    state = Table.grid(padding=(0, 2))
    state.add_row(
      f"Deck: {len(game.deck)}",
      f"Scores: P1: {game.player1.score} | P2: {game.player2.score}",
    )
    state.add_row(
      f"Discard: {' '.join(str(c) for c in game.discard_pile[-3:])}"
    )
    game_panel = Panel(state, title="Game State", border_style="cyan")
    from rich.console import Group
    self.live.update(Group(game_panel))
    self.live.refresh()
    return Group(game_panel)