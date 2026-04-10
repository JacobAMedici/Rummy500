from flask import Flask, render_template, jsonify, request, redirect, url_for

from model.AIPlayer import AIPlayer
from model.Card import Meld, MeldType
from model.Game import Game
from model.Helpers import tally_scores

def create_app(player1, player2):
  app = Flask(__name__, template_folder='../view/templates')
  game = Game(player1, player2)

  @app.route('/')
  def index():
    if isinstance(game.players_turn, AIPlayer):
      handle_AI_turn()
    return render_template('index.html', game=game)

  @app.route('/draw', methods=['POST'])
  def draw():
    source = request.form.get('source')
    index = request.form.get('index')
    if source == 'deck':
      game.draw_from_deck()
    elif source == 'discard':
      game.draw_from_discard(int(index))
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
    cards = [game.players_turn.hand[index] for index in indices]
    try:
      game.play_cards(cards, meld_type)
    except Exception as e:
      pass
    return redirect(url_for('index'))

  @app.route('/done_acting', methods=['POST'])
  def done_acting():
    game.phase = 'discard'
    return redirect(url_for('index'))

  @app.route('/discard', methods=['POST'])
  def discard():
    index = request.form.get('index')
    game.discard(int(index))
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
      game = Game(player1, player2)
      if player1.score > 500 or player2.score > 500:
        return redirect(url_for('winner'))
    return redirect(url_for('index'))

  def handle_AI_turn():
    nonlocal game
    draw_index = game.players_turn.have_player_draw(game, 0.9, 0.5)
    while True:
      if draw_index == -1:
        if game.draw_from_deck():
          break
      else:
        if game.draw_from_discard(draw_index):
          break

    while True:
      action = game.players_turn.have_player_act()
      if not action:
        break
      else:
        game.play_cards(action[0], action[1])

    while True:
      discard_index = game.players_turn.have_player_discard(game, 0.9, 0.5)
      if game.discard(discard_index):
        break

  return app