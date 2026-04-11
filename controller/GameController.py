from flask import Flask, render_template, request, redirect, url_for

from model import Helpers
from model.AIPlayer import AIPlayer
from model.Card import MeldType
from model.Game import Game

def create_app(player1, player2):
  app = Flask(__name__, template_folder='../view/templates')
  game = Game(player1, player2)

  @app.route('/')
  def index():
    if isinstance(game.players_turn, AIPlayer):
      Helpers.handle_AI_turn(game)
      handle_game_over_check()
    return render_template('index2.html', game=game)

  @app.route('/draw', methods=['POST'])
  def draw():
    source = request.form.get('source')
    index = request.form.get('index')
    if source == 'deck':
      game.draw_from_deck()
    elif source == 'discard':
      try:
        game.draw_from_discard(int(index))
      except Exception as e:
        pass
    return redirect(url_for('index'))

  @app.route('/meld', methods=['POST'])
  def meld():
    source = request.form.get('source')
    if source == 'set':
      meld_type = MeldType.SET
    elif source == 'run':
      meld_type = MeldType.RUN
    else:
      meld_type = MeldType.INVALID

    input_indices = request.form.get('index')
    indices = [int(index) for index in input_indices.split(" ")]
    try:
      game.play_cards(indices, meld_type)
    except Exception as e:
      pass
    return redirect(url_for('index'))

  @app.route('/done_acting', methods=['POST'])
  def done_acting():
    game.done_acting()
    return redirect(url_for('index'))

  @app.route('/discard', methods=['POST'])
  def discard():
    try:
      index = request.form.get('index')
      game.discard(int(index))
    except Exception as e:
      pass
    return handle_game_over_check()

  @app.route('/winner', methods=['POST'])
  def winner():
    if game.player1.score > game.player2.score:
      return render_template('winner.html', winner="Player 1 Wins")
    elif game.player1.score < game.player2.score:
      return render_template('winner.html', winner="Player 2 Wins")
    else:
      return render_template('winner.html', winner="Tie")

  def handle_game_over_check():
    # https://www.w3schools.com/python/ref_keyword_nonlocal.asp
    nonlocal game
    if game.check_round_over():
      player1.new_game()
      player2.new_game()
      game = Game(player1, player2)
      if player1.score >= 500 or player2.score >= 500:
        return redirect(url_for('winner'))
    return redirect(url_for('index'))

  return app