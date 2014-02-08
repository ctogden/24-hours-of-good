from flask import *
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Set a secret key for encryping sessions
app.secret_key = 'adsgjkatQ$WTasW$Twa4tJT$/$3'


games = []
all_games_full = True
game_counter = -1

class Game:
    def __init__(self, first_player):
        global game_counter
        game_counter += 1
        self.id = game_counter 
        self.players = []
        self.players.append(first_player)
    def add_player(name):
        self.players.append(name)
    def __str__(self):
        print "Game #" + str(self.id)

@app.route('/')
def index():
    """Create an index page that creates a user session"""
    global game_counter
    global all_games_full
    if session:
        print "session"
    else:
        if all_games_full:
            session['game'] = game_counter + 1
            games.append(Game("Hanne"))
            ##
            i = 0
            while i < len(games):
                games[i].__str__()
                i += 1
        else:
            session['game'] = game_counter + 1
            games[game_counter].add_player("Chris")
            i = 0
            while i < len(games):
                games[i].__str__()
                i += 1
    return str(session['game'])

@app.route('/play')
def play():
    return render_template('play.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

# Only needed to run locally
app.debug = True;
app.run()
