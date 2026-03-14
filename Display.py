from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
import time

class Display:
  def __init__(self):
    self.console = Console()

  def render(game):
    state = Table.grid(padding=(0, 2))
    state.add_row(
      f"Deck: {len(game.deck)}"
    )
    game_panel = Panel(state, title="Game State", border_style="cyan")
    from rich.console import Group
    return Group(game_panel)