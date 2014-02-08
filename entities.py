from random import randint

#
# Constants
# TODO. Subject to change.


# Number of player instances (static)
number_of_players = 0

class EmailType:
    power_up = 0
    virus_scanner = 1
    accusation = 2

class AttackType:
    none = 0
    trojan = 1
    malware = 2
    worm = 3
    spyware = 4
    virus = 5


# Represents an office drone user. 
class OfficeDrone:

    #Construct Me
    def __init__(self, name):
        global number_of_players
		# Unique id number
        self.id = number_of_players
        number_of_players += 1
        # Player name
        self.name = name
        # Indicates whether or not a player instance has been fired.
        self.fired = False
        # Represents a list of emails that a player instance sent
        self.sent_emails = []
        # Represents a list of other player instances that a player instance is accusing.
        self.accusations = []
        # Indicates whether or not a player instnace is connected to the server or not.
        self.connection = True
        # Represents a players system health.
        self.health = 100
        self.fired = False
        # Indicatess whether or not a OfficeDrone instance has been compromised. 
        self.compromised = False
        # Represents a list of past emails that a OfficeDrone instance opened.
        self.opened_emails = []
        # Represents the infections that a OfficeDrone instance is infected with at a given time.
        self.infections = []
		

    # Creates an email op
    def createEmail(self, email_type, accused_user, turn):
        email = Email(email_type, AttackType.none, accused_user, self.id, turn)
        self.sent_emails.append(email)
        return email

    # Opens an email op
    def openEmail(self, email):
        # First checks email if it contains power ups or virus scanners and applies them.
        self.opened_emails.append(email)
        if email.getType() == EmailType.power_up:
            if self.health <= (100 - PowerUp.boost):
                self.health += PowerUp.boost
        elif email.getType() == EmailType.virus_scanner:
            if len(self.infections) > 0:
                for i in len(self.infections):
                    if not (self.infections[i].getDelay() > 0):
                        self.infections.remove(i)
        else:
            print 'Check the Hacker.openEmail() method in entities.py, line 102, for a unresolved logical path has been reached.'
        # Second check if there is any attacks attached in the email. If there is, append it.
        virus = email.checkForInfection()
        if virus:
            self.infections.append(virus)

    # Applies damages if any and removes any finished infections.
    def takeEffects(self):
        if len(self.infections) > 0:
            for attack in (self.infections):
                if attack.getDelay() == 0:
                    self.health += attack.getDpi()
                if attack.step() == -1:
                    self.infections.remove(i)
		if accused(self):
			self.fired = True
		if health <= 0:
			self.compromised = True


# Represents a hacker user.
class Hacker:

    #Construct Me
    def __init__(self, name):
        global number_of_players
		# Unique id number
        self.id = number_of_players
        number_of_players += 1
        # Player name
        self.name = name
        # Indicates whether or not a player instance has been fired.
        self.fired = False
        # Represents a list of emails that a player instance sent
        self.sent_emails = []
        # Represents a list of other player instances that a player instance is accusing.
        self.accusations = []
        # Indicates whether or not a player instnace is connected to the server or not.
        self.connection = True
        # Represents the player instances that are under a hacker instances control.
        bots = []
        # Represents a key pair of active virus : OfficeDrone instance. 
        active_viruses = []

    # Creates an email op
    def createEmail(self, email_type, attack_type, accused_user, turn):
        email = Email(self, email_type, attack_type, accused_user, self.id, turn)
        self.sent_emails.append(email)
        return email

    # Adding a bot to list of bots op
    def addBot(office_drone_turned_bot):
        self.bots.append(office_drone_turned_bot)     


#
# Other Game Entity Classes
#

# Represents an attack
class Attack:
  # Server related
    # Number of attack instances
    number_of_attacks = 0

    # Construct me
    def __init__(self, delay, iterations, dpi):
      # Game related
        # Unique id number
        self.id = Attack.number_of_attacks
        Attack.number_of_attacks += 1
        # Delay before attack activates
        self.delay = delay
        # Number of times the attack does damage
        self.iterations = iterations
        # Damage dealt per iteration
        self.damage_per_iteration = dpi

    # Update
    def step(self):
        if self.delay > 0:
            self.delay -= 1
        elif self.iterations > 0:
            self.iterations -= 1
            return damage_per_iteration
        else:
            return -1

    # getter delay
    def getDelay(self):
        return self.delay

    # getter damage per iteration
    def getDpi(self):
        return self.damage_per_iteration


# Represents a simple power up
class PowerUp:
    # The amount of health that is healed
    boost = 10


# Represents an email
class Email:
  # Server related
    # Number of email instances
    number_of_emails = 0

    # Construct Me
    def __init__(self, email_type, attack_type, user_accused, sender_id, sent_turn):
      # Game related
        # Unique id
        self.id = Email.number_of_emails
        Email.number_of_emails += 1
        # Only EmailType enums apply
        self.email_type = email_type
        # Only AttackType enums apply
        self.attack_type = attack_type
        self.user_accused = user_accused
        self.sender_id = sender_id
        self.sent_turn = sent_turn


    def checkForInfection(self):
        return Attack()

#
# Class-less Functions
#

# Generates a random power up
def generateRandomPowerUp():
    power_ups = ['Change Password','Install Updates',
                 'Enable 2-Factor Authentication', 'Lock Your Device',
                 'Update Privacy Settings', 'Only Use Secure Websites']

    index = randint(0, len(power_ups))
    return power_ups[index]

# Generates an attack with a specifc AttackType enum only.
def generateAttack(attack_type):
    attacks = { AttackType.none : (0,0,0),
                AttackType.trojan : (0,0,0),
                AttackType.malware : (0,0,0),
                AttackType.worm : (0,0,0),
                AttackType.spyware : (0,0,0),
                AttackType.virus : (0,0,0)}
    return Attack(attacks[attack_type][0],attacks[attack_type][1],attacks[attack_type][2])

