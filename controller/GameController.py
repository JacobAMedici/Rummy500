from flask import Flask, render_template, jsonify, request, redirect, url_for

from model.Card import Meld, MeldType
from model.Game import Game
from model.Helpers import tally_scores
from model.HumanPlayer import HumanPlayer

def create_app(player1, player2):
  app = Flask(__name__, template_folder='../view/templates')
  game = Game(player1, player2)

  @app.route('/')
  def index():
    return render_template('index.html', game=game)

  @app.route('/draw', methods=['POST'])
  def draw():
    source = request.form.get('source')
    index = request.form.get('index')

    try:
      if source == 'deck':
        card = game.deck.pop()
        game.players_turn.hand.append(card)
      elif source == 'discard':
        card = game.discard_pile.pop(int(index))
        game.players_turn.hand.append(card)
      game.phase = 'act'
    except Exception as e:
      print(e)
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
    indices = [int(index) for index in input_indices.split()]
    cards = [game.players_turn.hand[index] for index in indices]
    game.play_cards(cards, meld_type)
    handle_game_over()

  @app.route('/done_acting', methods=['POST'])
  def done_acting():
    game.phase = 'discard'
    return redirect(url_for('index'))

  @app.route('/discard', methods=['POST'])
  def discard():
    index = request.form.get('index')
    game.discard(index)
    handle_game_over()

  @app.route('/winner', methods=['POST'])
  def winner():
    if game.player1.score > game.player2.score:
      return render_template('winner.html', winner="Player 1 Wins")
    elif game.player1.score < game.player2.score:
      return render_template('winner.html', winner="Player 2 Wins")
    else:
      return render_template('winner.html', winner="Tie")

  def handle_game_over():
    # https://www.w3schools.com/python/ref_keyword_nonlocal.asp
    nonlocal game
    if game.check_round_over():
      game = Game(player1, player2)
      if player1.score > 500 or player2.score > 500:
        return redirect(url_for('winner'))
    return redirect(url_for('index'))

  return app