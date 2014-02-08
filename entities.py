from random import randint

#
# Constants
# TODO. Subject to change.

class EmailType:
    power_up = 0
    virus_scanner = 1


class AttackType:
    none = 0
    trojan = 1
    malware = 2
    worm = 3
    spyware = 4
    virus = 5




#
# Player Classes
#

# Parent class that represents a generic player.
class Player:
    # Server related
    # Number of player instances (static)
    __number_of_players = 0

    #Construct Me
    def __init__(self, name):
        # Game related
        # Unique id number
        self.__id = Player.__number_of_players
        Player.__number_of_players += 1
        # Player name
        self.__name = name
        # Indicates whether or not a player instance has been fired.
        self.__fired = False
        # Represents a list of emails that a player instance sent
        self.__sent_emails = []
        # Represents a list of other player instances that a player instance is accusing.
        self.__accusations = []
      # Server related
        # Indicates whether or not a player instnace is connected to the server or not.
        self.__connection = True


# Represents an office drone user. 
class OfficeDrone(Player):

    #Construct Me
    def __init__(self, name):
        Player.__init__(self, name)
      # Game related
        # Represents a players system health.
        self.__health = 100
        # Indicatess whether or not a OfficeDrone instance has been compromised. 
        self.__compromised = False
        # Represents a list of past emails that a OfficeDrone instance opened.
        self.__opened_emails = []
        # Represents the infections that a OfficeDrone instance is infected with at a given time.
        self.__infections = []

    # Creates an email op
    def createEmail(self, email_type):
        email = Email(self, email_type, AttackType.none)
        self.__sent_emails.append(email)
        return email

    # Opens an email op
    def openEmail(self, email):
        # First checks email if it contains power ups or virus scanners and applies them.
        self.__opened_emails.append(email)
        if email.getType() == EmailType.power_up:
            if self.health <= (100 - PowerUp.boost):
                self.health += PowerUp.boost
        elif email.getType() == EmailType.virus_scanner:
            if len(self.__infections) > 0:
                for i in len(self.__infections):
                    if not (self.__infections[i].getDelay() > 0):
                        self.__infections.remove(i)
        else:
            print 'Check the Hacker.openEmail() method in entities.py, line 102, for a unresolved logical path has been reached.'
        # Second check if there is any attacks attached in the email. If there is, append it.
        virus = email.checkForInfection()
        if virus:
            self.__infections.append(virus)

    # Applies damages if any and removes any finished infections.
    def takeEffects(self):
        if len(self.__infections) > 0:
            for attack in (self.__infections):
                if attack.getDelay() == 0:
                    self.__health += attack.getDpi()
                if attack.step() == -1:
                    self.__infections.remove(i)


# Represents a hacker user.
class Hacker(Player):

    #Construct Me
    def __init__(self, name):
        Player.__init__(self, name)
      # Game related
        # Represents the player instances that are under a hacker instances control.
        __bots = []
        # Represents a key pair of active virus : OfficeDrone instance. 
        __active_viruses = []

    # Creates an email op
    def createEmail(self, email_type, attack_type):
        email = Email(self, email_type, attack_type)
        self.__sent_emails.append(email)
        return email

    # Adding a bot to list of bots op
    def addBot(office_drone_turned_bot):
        self.__bots.append(office_drone_turned_bot)     



#
# Other Game Entity Classes
#

# Represents an attack
class Attack:
  # Server related
    # Number of attack instances
    __number_of_attacks = 0

    # Construct me
    def __init__(self, delay, iterations, dpi):
      # Game related
        # Unique id number
        self.__id = Attack.__number_of_attacks
        Attack.__number_of_attacks += 1
        # Delay before attack activates
        self.__delay = delay
        # Number of times the attack does damage
        self.__iterations = iterations
        # Damage dealt per iteration
        self.__damage_per_iteration = dpi

    # Update
    def step(self):
        if self.__delay > 0:
            self.__delay -= 1
        elif self.__iterations > 0:
            self.__iterations -= 1
            return __damage_per_iteration
        else:
            return -1

    # getter delay
    def getDelay(self):
        return self.__delay

    # getter damage per iteration
    def getDpi(self):
        return self.__damage_per_iteration


# Represents a simple power up
class PowerUp:
    # The amount of health that is healed
    boost = 10


# Represents an email
class Email:
  # Server related
    # Number of email instances
    __number_of_emails = 0

    # Construct Me
    def __init__(self, email_type, attack_type):
      # Game related
        # Unique id
        self.id = Email.__number_of_emails
        Email.__number_of_emails += 1
        # Only EmailType enums apply
        self.email_type = email_type
        # Only AttackType enums apply
        self.attack_type = attack_type


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

