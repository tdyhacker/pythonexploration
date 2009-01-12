from random import Random
from datetime import datetime

class Master:
    # Private Globals
    __info = "release_date(year.month.day)\nversion(year.month)\nmodified(year.month.day)\nUbuntu Style version control"
    __modified = '9.1.9'
    __release_date = '0.0.0'
    __version = '9.1'
    __ids = 10000
    
    def __init__(self):
        self.attributes = {'program': self._program()}
    
    def __repr__(self):
        return self._program()
    
    def _playergetID(self):
        if not self.__class__ == Player().__class__:
            self.__ids += 1
            return "PLAYER_%s:%s" % (int(self.__ids / 10000) - 1, self.__ids % 10000)
        else:
            return "Unknown" # The Game is the only one that is allowed to assign IDs
    
    def _program(self):
        return "<Version: %7s\t- Modified: %7s\t- Released: %7s>" % (self.__version, self.__modified, self.__release_date)
    
class Roulette(Master):
    def __init__(self):
        self.playercount = 0
        self.__group = []
        self.__wheel = Dice(1,38)
        self.__ranks = {}
        
        self.__verbose = False
        
        self.selection = {
                '0': [0,],
                '00': [37,],
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
        self.__payout = {
                '0': 35,
                '00': 35,
                'straight up': 35,
                'row 00': 17,
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
        
        self.tag = "Roulette"
    
    def __repr__(self):
        return "<Roulette| PlayerCount: %s>" % (self.playercount)

    def playerJoin(self, player):
        if not player in self.__group:
            # Client
            player.game = self
            player.id = self._playergetID()
            player.Information[self.tag] = {}
            player.Information[self.tag]['Rank'] = len(self.__ranks) + 1
            # Server
            self.playercount += 1
            self.__group.append(player)
            self.__ranks[self.__ranks + 1] = player
        else:
            self.playerLeave(player)
            self.playerJoin(player)
    
    def playerLeave(self, player):
        if player in self.__group:
            # Server
            self.playercount -= 1
            self.__group.remove(player)
            self.__ranks[player.Information]
            # Client
            player.game = None
            player.id = "Unknown"
            del player.Information[self.tag]
            player.reset(2)
        else:
            print "Player has already left"
    
    def playerMethod(self, player):
        '''
        Methods
        --------
        [Progression]
            Martingale
            Labouchere - roulette games
            D'Alembert
        [Staking Systems]
            Follow the Shoe
            Avant Dernier
            Regression Modelling
        '''
        meth = player.method.lower()
        if meth == 'martingale':
            player.martingale()
        elif meth == 'labouchere':
            player.labouchere()
        elif meth == 'dalembert':
            player.dalembert()
        else:
            player.martingale() # simplest type
    
    def __playerWinnings(self, player, won):
        if won:
            player.money += player.bet * self.__payout[player.Information['Roulette']['BettingName']]
            player.exchange += player.bet * self.__payout[player.Information['Roulette']['BettingName']]
            player.Information['won'] = True
        else:
            player.money -= player.bet
            player.exchange -= player.bet
            player.Information['won'] = False
        self.playerMethod(player)
    
    def __evaluateRanks(self):
        for player in self.__group:
            for rank in range(1, a.keys()[len(a.keys())])

    def play(self):
        landed = self.__wheel.roll() - 1 # making it [0:37] 0 = 0, 37 = 00
        for player in self.__group:
            if player.plays <= 0 or player.money <= 0:
                if self.__verbose:
                    print "Player %s has" % player.name,
                    if player.plays <= 0:
                        print "quit"
                    else:
                        print "gone broke"
                self.playerLeave(player)
            else:
                self.playerBet(player)
                player.plays -= 1
                player.Information['Roulette']['Winner'] = landed
                if landed in player.Information['Roulette']['BettingNumber']:
                    self.__playerWinnings(player, True)
                else:
                    self.__playerWinnings(player, False)
            player.setCurrent() # update no matter what


    def playerBet(self, player, amount, selection, **kw):
        player.changemind()
        player.Information[self.tag]['BettingName'] = selection
        player.Information[self.tag]['BettingNumber'] = self.selection[selection]

class Player(Master):
    def __init__(self, **kw):
        self.rand = Random(datetime.now())
        
        self.successrate = 0.5 # default is 50% of the time
        
        # Default mode
        self.name = 'Bob'
        self.id = "Unknown" # Assigned by Game
        self.attentionspan = self.rand.random() # How long they'll spend playing the game
        self.stratpoint = self.rand.random() # How llong they'll spend using the same stradegy lower number is shorter
        # Always changes
        self.bet = 10
        
        self.wins = 0
        self.losses = 0
        
        ## Never touched by the player
        self.exchange = 0
        self.money = 500
        ##
        
        self.plays = 20 # Number of times they'll play before they just quit playing all together
        self.method = 'Martingale'
        self.game = None # Assigned by Game
        
        if kw:
            self.Information = kw
        else:
            self.Information = {}
        
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
        if kw.has_key('name') and kw['name']:
            self.name = kw['name']
        
        self.Information['starterbet'] = self.bet
        
        # Saving all old information for resetting purposes
        self.Information['originalInfo'] = {}
        self.Information['originalInfo']['bet'] = self.bet
        self.Information['originalInfo']['successrate'] = self.successrate
        self.Information['originalInfo']['name'] = self.name
        self.Information['originalInfo']['id'] = self.id
        self.Information['originalInfo']['attentionspan'] = self.attentionspan
        self.Information['originalInfo']['wins'] = self.wins
        self.Information['originalInfo']['losses'] = self.losses
        self.Information['originalInfo']['exchange'] = self.exchange
        self.Information['originalInfo']['money'] = self.money # statistical only
        self.Information['originalInfo']['plays'] = self.plays
        self.Information['originalInfo']['method'] = self.method
        
        self.setCurrent()
    
    def setCurrent(self):
        self.Information['current'] = {}
        self.Information['current']['bet'] = self.bet
        self.Information['current']['successrate'] = self.successrate
        self.Information['current']['name'] = self.name
        self.Information['current']['id'] = self.id
        self.Information['current']['attentionspan'] = self.attentionspan
        self.Information['current']['wins'] = self.wins
        self.Information['current']['losses'] = self.losses
        self.Information['current']['exchange'] = self.exchange
        self.Information['current']['money'] = self.money # statistical only
        self.Information['current']['plays'] = self.plays
        self.Information['current']['method'] = self.method
        self.Information['current']['game'] = self.game

    def __repr__(self):
        return "<Player| Name: %s - ID: %s - Money: %s - TotalExchange: %s - Wins: %s - Losses: %s>>" % (self.name, self.id, self.money, self.exchange, self.wins, self.losses)
    
    def changemind(self):
        if self.stratpoint < Random(datetime.now()).random() or not self.Information[game.tag].has_key('BettingName'): # If they change their mind on their betting number
            self.Information[game.tag]['BettingName'] = self.game.selection.keys()[int( len(self.selection.keys()) * Random(datetime.now()).random() )]
            if self.Information[game.tag]['BettingName'] != 'straight up':
                self.Information[game.tag]['BettingNumber'] = self.game.selection[self.Information[game.tag]['BettingName']]
            else: # This is if it's a single number
                self.Information[game.tag]['BettingNumber'] = [self.game.selection['straight up'][int( len(self.game.selection['straight up']) * Random(datetime.now()).random() )],]
    
    def reset(self, flags=0):
        '''
            Flags:  What happens
            0/1:    Standard
            2:      Statistics
            4:      Name
            8:      None
            16:     None
            32:     None
            64:     None
            128:    None
            256:    None
            512:    None
            1024:   None
            2048:   None
            4096:   None
            Full:   8191 // Anything more will evaluate all flags
            Any Combination of these will evaluate the respected flags
        '''
        # if any flag
        self.bet = self.Information['originalInfo']['bet']
        self.successrate = self.Information['originalInfo']['successrate']
        self.plays = self.Information['originalInfo']['plays']
        self.attentionspace = self.Information['originalInfo']['attentionspan']
        self.method = self.Information['originalInfo']['method']
        
        if flags > 6: # Currently I do not have anything above 6, so anything higher is useless
            flags = 0
        if (flags - 4) >= 0:
            flags -= 4
            self.name = self.Information['originalInfo']['name']
        if (flags - 2) >= 0:
            flags -= 2
            self.wins = self.Information['originalInfo']['wins']
            self.losses = self.Information['originalInfo']['losses']
            self.exchange = self.Information['originalInfo']['exchange']
        
        self.setCurrent()

    def continuePlaying(self):
        if self.game:
            if self.additionspan < self.rand():
                self.quit() # Quit the game
    
    def quit(self):
        if self.game:
            self.game.playerLeave(self) # Quit the game
        else:
            "/quit Life"
    
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

    def martingale(self):
        if self.Information.has_key('won'):
            if not self.Information['won']:
                self.losses += 1
                self.bet *= 2
            else:
                self.wins += 1
                self.bet = self.Information['starterbet']

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
m = Master()
d = Dice()
r = Roulette()
p = []
for a in range(10):
    p.append(Player(name='%s' % a))
    r.playerJoin(p[a])

round = 1

while r.playercount:
    #print "Round %s" % round
    r.play()
    
    #for player in p:
    #    if player.game:
    #        print "Player %s" % player.name,
    #        if player.Information['won']:
    #            print "won on %s" % (player.Information['Roulette']['Winner'])
    #        else:
    #            print "lost"
    round += 1
    
if False:
    
    class Statistics:
        min = 0
        max = 0
    s = Statistics()
    
    print "Rounds Done %s" % round
    print "\n"
    
    for player in p:
        if player.money > s.max:
            s.max = player.money
        elif player.money < s.min:
            s.min = player.money
        print "Player %s has $%s" % (player.name, player.money)
    
    print "Min: $%s" % s.min
    print "Max: $%s" % s.max
