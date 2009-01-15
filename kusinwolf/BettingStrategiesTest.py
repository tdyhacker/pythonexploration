import unittest
from BettingStrategies import *

class TestSequenceFunctions(unittest.TestCase):

    # Hook function designed to be overloaded for each function's test requirements
    def setUp(self):
        self.m = Master()
        self.d = Dice()
        self.r = Roulette()
        self.p = []

    # All test functions must start with the name test* and can be named anything else afterwards
    def testDefaultDice(self):
        self.failUnless(self.d.die == 1)
        self.failUnless(self.d.sides == 6)
    
    def testDefaultPlayer(self):
        p = Player()
        self.failUnless(p.name == 'Bob')

    def testDiceRandomSides(self):
        self.d.randomSides()
        self.failUnless(self.d.sides <= 100 and self.d.sides > 0)
    
    def testDiceRandomDice(self):
        self.d.randomDice()
        self.failUnless(self.d.die <= 100 and self.d.die > 0)
    
    def testDiceRandomDice(self):
        self.d.randomDice()
        self.failUnless(self.d.die <= 100 and self.d.die > 0)
    
    def testGameAddRemove(self):
        p = Player()
        self.r.playerJoin(p)
        c = self.r.playercount
        self.r.playerLeave(p)
        self.failUnless(self.r.playercount < c)

    def testGameJoin(self):
        for a in range(100):
            self.p.append(Player())
            self.r.playerJoin(self.p[a])
        
        self.failUnless(self.r.playercount == 100)
    
    def testGameLeave(self):
        for player in self.p:
            player.game.playerLeave(player)
        
        self.failUnless(self.r.playercount == 0)
    
    def testMasterPlayerID(self):
        self.failUnless(type(self.m._playergetID()) == str)
    
    def testMasterVersion(self):
        self.failUnless(type(self.m._program()) == str)


# This is used for finer ouput on each test
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions) # Simple way of building all the test cases
#asuite = unittest.TestSuite(map(TestSequenceFunctions, ['testshuffle', 'testchoice', 'testsample']))
test = unittest.TextTestRunner(verbosity=2).run(suite)