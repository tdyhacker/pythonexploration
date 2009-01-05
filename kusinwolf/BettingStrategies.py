from random import Random
from datetime import datetime



class Game(object):
    
    def __init__(self, successrate = 0.5, **kw):
        self.info = "release_date(year.month.day)\nversion(year.month)\nmodified(year.month.day)\nUbuntu Style version control"
        self.modified = '0.0.0'
        self.release_date = '0.0.0'
        self.version = '9.1'
        
        self.rand = Random()
        self.rand.seed(datetime.now())
        
        self.successrate = successrate # default is 50% of the time
        
        # Default mode
        self.bet = 10
        self.dice = Dice()
        self.money = 20000
        self.plays = 20
        self.method = 'Martingale'
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
            
        self.numberOfWins = 0
        self.numberOfLosses = 0
        self.totalExchange = 0
        
        if self.method == 'Labouchere' :
            self.Labouchere()
        
        print "Game built, Success Rate at %s%% of the time" % self.successrate
    
    def __repr__(self):
        return "<Game Money: %s - Dice: %s - TotalExchange: %s - Wins: %s - Losses: %s>" % (self.money, self.dice, self.totalExchange, self.numberOfWins, self.numberOfLosses)
    
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
    
    def roll(self, package):
        return (int(self.rand.random() * package.sides) + 1, package)

    def findWinners(self, package):
        if self.method == 'Labouchere':
            print "Die1: %s \tDie2: %s" % (package[0][0], package[1][0])
            win = (package[0][0] == package[1][0])
        else:
            win = (float(package[0]) / package[1].sides) > self.successrate
        return win

    def play(self, **ikw):
        if self.method == 'Martingale':
            for number in range(self.plays):
                for die in range(self.dice.die):
                    if not self.findWinners(self.roll(Dice(1, self.dice.sides))):
                        self.money -= self.bet
                        self.totalExchange -= self.bet
                        self.numberOfLosses += 1
                        self.bet *= 2
                    else:
                        self.money += self.bet
                        self.totalExchange += self.bet
                        self.numberOfWins += 1
                        self.bet = 10
                
        elif self.method == 'Labouchere':
            while self.bettingNumbers: # has numbers
                if len(self.bettingNumbers) > 1:
                    combobet = self.bettingNumbers[0] + self.bettingNumbers[len(self.bettingNumbers) - 1]
                else:
                    combobet = self.bettingNumbers[0]
                if self.findWinners((self.roll(Dice(1, self.dice.sides)), self.roll(Dice(1, self.dice.sides)))):
                    print "Won %s" % (combobet * 35)
                    if len(self.bettingNumbers) > 1:
                        self.bettingNumbers.remove(self.bettingNumbers[0])
                        self.bettingNumbers.remove(self.bettingNumbers[len(self.bettingNumbers) -1])
                    else:
                        self.bettingNumbers.remove(combobet)
                    self.numberOfWins += 1
                    self.money += combobet * 35 # Pay out for a single number winning is 35x the bet
                    self.totalExchange += (combobet * 35)
                else:
                    print "Lost %s" % combobet
                    self.totalExchange -= combobet
                    self.money -= combobet
                    self.numberOfLosses += 1
                    self.bettingNumbers.append(combobet)
                
                #elif self.method == "D'Alembert":
                #    
                #
                #elif self.method == 'Follow the Shoe':
                #    
                #
                #elif self.method == 'Avant Dernier':
                #    
                #
                #elif self.method == 'Regression Modelling':
                #
                
                if self.money <= 0:
                    print "You've gone broke"
                    break
        print self

class Dice(object):
    
    def __init__(self, die = 1, sides = 6, **kw):
        self.info = "release_date(year.month.day)\nversion(year.month)\nmodified(year.month.day)\nUbuntu Style version control"
        self.modified = '0.0.0'
        self.release_date = '0.0.0'
        self.version = '9.1'
        
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

lrolled = None
drolled = None
wlrolled = None
wdrolled = None

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

game = Game(Dice().rand.random(), money=50, plays=30, method='Labouchere')
game.play()
