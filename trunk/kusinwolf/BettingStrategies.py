from random import Random
from datetime import datetime

class Master:
    def __init__(self):
        self.info = "release_date(year.month.day)\nversion(year.month)\nmodified(year.month.day)\nUbuntu Style version control"
        self.modified = '9.1.8'
        self.release_date = '0.0.0'
        self.version = '9.1'
        
        self.ids = 10000
    
    def __repr__(self):
        return self.program()
    
    def getID(self):
        self.ids += 1
        return "PLAYER_%s:%s" % (int(self.ids / 10000) - 1, self.ids % 10000)
    
    def program(self):
        return "<Version: %7s\t- Modified: %7s\t- Released: %7s>" % (self.version, self.modified, self.release_date)

class Roulette(Master):
    def __init__(self):
        self.playercount = 0
        self.group = []
        self.wheel = Dice(1,38)
        
        self.selection = {
                '0': 0,
                '00': 37,
                '1-18': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                '19-36': [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
                '1st12': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                '2nd12': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                '3rd12': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36],
                'black': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
                'column1': [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
                'column2': [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35],
                'column3': [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
                'even': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
                'five number bet': [0, 37, 1, 2, 3],
                'odd': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35],
                'red': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
                'row 00': [0, 37],
                'row1': (1, 2, 3),
                'row10': (28, 29, 30),
                'row11': (31, 32, 33),
                'row2': (4, 5, 6),
                'row3': (7, 8, 9),
                'row4': (10, 11, 12),
                'row5': (13, 14, 15),
                'row6': (16, 17, 18),
                'row7': (19, 20, 21),
                'row8': (22, 23, 24),
                'row9': (25, 26, 27),
                'straight up': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36] }
        self.payout = {
                '0': 35,
                '00': 35,
                'Straight up': 35,
                'Row 00': 17,
                'row1': 11,
                'row10': 11,
                'row11': 11,
                'row2': 11,
                'row3': 11,
                'row4': 11,
                'row5': 11,
                'row6': 11,
                'row7': 11,
                'row8': 11,
                'row9': 11,
                'five number bet': 6,
                '1st12': 2,
                '2nd12': 2,
                '3rd12': 2,
                'column1': 2,
                'column2': 2,
                'column3': 2,
                'black': 1,
                'red': 1,
                'even': 1,
                'odd': 1,
                '1-18': 1,
                '19-36': 1 }
        
        print "Playing Roulette :D"
    
    def __repr__(self):
        return "<Game: Roulette - Players: %s - Online: %s>" % (self.playercount, self.group)

    def playerJoin(self, player):
        if not player in self.group:
            player.game = self
            self.playercount += 1
            self.group.append(player)
        else:
            self.playerLeave(player)
            self.playerJoin(player)
    
    def playerLeave(self, player):
        if player in self.group:
            player.game = None
            self.playercount -= 1
            self.group.remove(player)
        else:
            print "Player has already left"
    
    def playerWinnings(self, player, won):
        if won:
            player.money += player.bet * self.payout[player.additionalInformation['BettingName']]
            player.exchange += player.bet * self.payout[player.additionalInformation['BettingName']]
            player.additionalInformation['won'] = True
        else:
            player.money -= player.bet
            player.exchange -= player.bet
            player.additionalInformation['won'] = False
        player.options[player.method]

    def play(self):
        while self.playercount: # has numbers
            landed = self.wheel.roll() - 1 # making it [0:37] 0 = 0, 37 = 00
            for player in self.group:
                if landed in player.additionalInformation['BettingNumber']:
                    self.playerWinnings(player, True)
                else:
                    self.playerWinnings(player, False)


    def playerBet(self, player):
        if player.stratpoint < Random(datetime.now()).random(): # If they change their mind on their betting number
            player.additionalInformation['BettingName'] = self.selection.keys()[int( len(self.selection.keys()) * Random(datetime.now()).random() )]
            if player.additionalInformation['BettingName'] != 'straight up':
                player.additionalInformation['BettingNumber'] = self.selection[player.additionalInformation['BettingName']]
            else: # This is if it's a single number
                player.additionalInformation['BettingNumber'] = [self.selection['straight up'][int( len(self.selection['straight up']) * Random(datetime.now()).random() )],]


class Player(Master):
    def __init__(self, **kw):
        self.rand = Random()
        self.rand.seed(datetime.now())
        
        self.successrate = successrate # default is 50% of the time
        
        # Default mode
        self.name = 'Bob'
        self.id = self.getID()
        self.additionspan = self.rand() # How long they'll spend playing the game
        self.stratpoint = self.rand() # How llong they'll spend using the same stradegy lower number is shorter
        # Always changes
        self.bet = 10
        
        self.wins = 0
        self.losses = 0
        
        ## Never touched by the player
        self.exchange = 0
        self.money = 20000
        ##
        
        self.plays = 20
        self.method = 'Martingale'
        self.options = {'Martingale': self.martingale(), 'Labouchere': self.labouchere()}
        self.game = None
        if kw:
            self.additionalInformation = kw
        else:
            self.additionalInformation = {}
        
        self.additionalInformation['starterbet'] = self.bet
        #Methods
        #--------
        #[Progression]
            #Martingale
            #Labouchere - roulette games
            #D'Alembert
        #[Staking Systems]
            #Follow the Shoe
            #Avant Dernier
            #Regression Modelling
        
        # Enhanced mode
        if kw.has_key('bet') and kw['bet']:
            self.bet = kw['bet']
        if kw.has_key('dice') and kw['dice']:
            self.dice = kw['dice']
        if kw.has_key('money') and kw['money']:
            self.money = kw['money']
            if self.money <= 0:
                print "You're broke"
        if kw.has_key('plays') and kw['plays']:
            self.plays = kw['plays']
        if kw.has_key('method') and kw['method']:
            self.method = kw['method']

    def __repr__(self):
        return "<Player: %s - ID: %s - Money: %s - TotalExchange: %s - Wins: %s - Losses: %s>" % (self.name, self.id, self.money, self.totalExchange, self.numberOfWins, self.numberOfLosses)

    def continuePlaying(self):
        if self.game:
            if self.additionspan < self.rand():
                self.game.playerLeave(self) # Quit the game
    
    def Labouchere(self):
        self.dice.die = 1 # only need one
        self.dice.sides = 36 # standard size roulette table
        
        if self.bet % 2 != 0:
            if self.bet != 1:
                self.bet -= 1
            else:                        
                self.bet -= 1
            print "Even number required for betting in this method"
            
        # Generate Betting Numbers
        self.bettingNumbers = [2]
        while sum(self.bettingNumbers) < self.bet:
            nextNum = self.bettingNumbers[len(self.bettingNumbers) - 1] * 2
            if (sum(self.bettingNumbers) + nextNum) < self.bet:
                self.bettingNumbers.append(nextNum)
            else:
                diff = self.bet - sum(self.bettingNumbers)
                if diff != 2:
                    self.bettingNumbers.append((self.bet - sum(self.bettingNumbers) / 2))
                else:
                    self.bettingNumbers.append(2)

    def martingale(self, **ikw):
        if not self.additionalInformation['won']:
            self.losses += 1
            self.bet *= 2
        else:
            self.wins += 1
            self.bet = self.additionalInformation['starterbet']

class Dice(Master):
    
    def __init__(self, die = 1, sides = 6, **kw):
        self.rand = Random()
        self.rand.seed(datetime.now())
        self.die = die # Standard is 1
        self.sides = sides # Standard is 6
        
        if kw.has_key('random') and kw['random']:
            self.randomDice()
            self.randomSides()

    def __repr__(self):
        return "<Dice Die: %s - Sides: %s>" % (self.die, self.sides)
    
    def randomSides(self):
        self.sides = int(self.rand.random() * 100) + 1
        print "Die now has %s sides" % self.sides
    
    def randomDice(self):
        self.die = int(self.rand.random() * 100) + 1
        if self.die != 1:
            print "There are now %s dice to be thrown" % self.die
        else:
            print "There is only %s die to be thrown" % self.die
    
    def roll(self):
        return int(self.rand.random() * self.sides) + 1


#Methods
#--------
#[Progression]
    #Martingale
    #Labouchere
    #D'Alembert
#[Staking Systems]
    #Follow the Shoe
    #Avant Dernier
    #Regression Modelling


