from flask import *
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Set a secret key for encryping sessions
app.secret_key = 'adsgjkatQ$WTasW$Twa4tJT$/$3'



# Global variables track games in play
MAX_PLAYERS = 3

games = []
all_games_full = True
game_counter = -1

# Game class holds all our game data
class Game:
    def __init__(self, first_player):
        global game_counter
        game_counter += 1
        self.id = game_counter 
        self.players = []
        self.players.append(first_player)
    def add_player(name):
        self.players.append(name)
    def get_player_count():
        return len(self.players)
    def __str__(self):
        print "Game #" + str(self.id)

@app.route('/')
def index():
    """Create an index page that allows entrance to a game"""
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    """Renders game page"""
    session.clear() # TODO: remove if we can reload page and take care of state
    render_template('game.html')

@app.route('/temp')
def temp():
    return str(session['game']) + " - " + session['name']
    return render_template('game.html')

@app.route('/connect')
def connect():
    display_name = request.args.get('displayName')
    global game_counter
    global all_games_full
    if all_games_full:
        session['game'] = game_counter + 1
        session['name'] = request.form['name']
        games.append(Game(session['name']))
        all_games_full = False
        print "New game created"
    else:
        session['game'] = game_counter + 1
        session['name'] = request.form['name']
        games[game_counter].add_player(session['name'])
        if games[game_counter].get_player_count() > MAX_PLAYERS:
            all_games_full = True
        print "Added to existing game"
    return jsonify(result=True)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

# Only needed to run locally
app.debug = True;
app.run()
