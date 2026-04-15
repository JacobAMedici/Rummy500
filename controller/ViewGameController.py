from flask import Flask, render_template, request, redirect, url_for, make_response

from model.AdvancedAIPlayer import AIPlayer
from model.Card import MeldType
from model.Game import Game

def create_app(player1, player2):
  app = Flask(__name__, template_folder='../view/templates')
  game = Game(player1, player2)


  @app.route('/')
  def index():
    if isinstance(game.players_turn, AIPlayer):
      AIPlayer.handle_AI_turn(game)
      result = handle_game_over_check()
      if result.location == url_for('winner'):
        return result
    response = make_response(render_template('index.html', game=game))
    if isinstance(game.players_turn, AIPlayer):
      response.headers['Refresh'] = '0.1'
    return response


  @app.route('/draw', methods=['POST'])
  def draw():
    source = request.form.get('source')
    draw_index = request.form.get('index')
    if source == 'deck':
      game.draw_from_deck()
    elif source == 'discard':
      try:
        game.draw_from_discard(int(draw_index))
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
    indices = [int(meld_index) for meld_index in input_indices.split(" ")]
    try:
      game.play_cards(indices, meld_type)
    except Exception as e:
      print(e)
    return redirect(url_for('index'))


  @app.route('/done_acting', methods=['POST'])
  def done_acting():
    game.done_acting()
    return redirect(url_for('index'))


  @app.route('/discard', methods=['POST'])
  def discard():
    try:
      discard_index = request.form.get('index')
      game.discard(int(discard_index))
    except Exception as e:
      print(e)
    return handle_game_over_check()


  @app.route('/winner', methods=['GET'])
  def winner():
    player1_score = game.player1.score
    player2_score = game.player2.score
    if player1_score > player2_score:
      result = "Player 1 Wins"
    elif player1_score < player2_score:
      result = "Player 2 Wins"
    else:
      result = "Tie"
    return render_template('winner.html', winner=result, p1_score=player1_score, p2_score=player2_score)


  # Check if the game over, and if it is, then handle it
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