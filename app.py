from flask import Flask, render_template, session, request, jsonify

from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"

boggle_game = Boggle()

@app.route("/")
def index():
    "Showing the boggle board game"
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    "check if word is in dictionary"
    word = request.args("word")
    board = session['board']
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'results': response})

@app.route("/post-score")
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    
    return jsonify(brokeRecord=score > highscore)
