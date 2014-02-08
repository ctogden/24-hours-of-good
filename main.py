from entities import *
from flask import *
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# Set a secret key for encryping sessions
app.secret_key = 'adsgjkatQ$WTasW$Twa4tJT$/$3'



# Global variables track games in play
MAX_PLAYERS = 3

games = []
players = []
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
        self.this_turn = 0
        #self.emails_sent_this_turn = []
    def add_player(self, player):
        self.players.append(player)
    def get_player_count(self):
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
    return render_template('game.html')

@app.route('/connect')
def connect():
    display_name = request.args.get('displayName')
    global game_counter
    global all_games_full
    if all_games_full:
        p1 = Hacker(display_name)
        players.append(p1)
        session['game'] = game_counter
        games.append(Game(p1))
        session['player'] = p1.id
        all_games_full = False
    else:
        user = OfficeDrone(display_name)
        session['player'] = user.id
        session['game'] = game_counter
        players.append(user)
        games[game_counter].add_player(user)
        if games[game_counter].get_player_count() >= MAX_PLAYERS:
            all_games_full = True
    return jsonify(result=True)

@app.route('/has_game_started')
def has_game_started():
    game_id = session['game']
    if games[game_id].get_player_count() >= MAX_PLAYERS:
        user = players[session['player']] 
        hacker = isinstance(user, Hacker)
        display_names = []
        idNumbers = []
        for p in games[game_id].players:
            if not p.fired:
                display_names.append(p.name)
                idNumbers.append(p.id)
        if hacker:
            health = -1
        else:
            health = user.health;
        return jsonify(result=True,isHacker=hacker, names=display_names, hp=health, ids = idNumbers)
    else:
        return jsonify(result=False)

@app.route('/send_email')
def send_email():
    game_id = session['game']
    email_type = display_name = request.args.get('email_type')
    user = players[session['player']]		
    if not email_type == EmailType.accusation:
        #Do email stuffs for powerup and virus scanner
        user.createEmail(email_type, -1, games[game_id].this_turn)
        #games[game_id].email_sent_this_turn.append(user.createEmail(email_type, -1, games[game_id].this_turn))
    else:
        #accused said person
        target_user = request.args.get('accused')
        user.createEmail(email_type, target_user, games[game_id].this_turn)
        #games[game_id].email_sent_this_turn .append(user.createEmail(email_type, target_user, games[game_id].this_turn))
    return jsonify(result = True)
		
@app.route('/all_emails_sent')
def all_emails_sent():
    game_id = session['game']
    current_game = games[game_id]
    emails_sent_this_turn = []
    for p in current_game.players:
        for e in p.sent_emails:
            if e.sent_turn == current_game.this_turn:
                emails_sent_this_turn.append(e)
    if len(emails_sent_this_turn) == len(current_game.players):
        return jsonify(emails = emails_sent_this_turn, result = True)
    else:
        return jsonify(result = False)
	#get list of all emails sent this turn in this game
	#if size of list is equal to number of emails sent this turn, return true with results of emails related else false
	#check if all emails sent by users this turn
    
@app.route('/test')
def test():
    return render_template('24hoursofgood.html')

@app.route('/hacker')
def hacker():
    return render_template('hackers.html')

@app.route('/drone')
def drone():
    return render_template('drones.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404

# Only needed to run locally
app.debug = True;
app.run()
