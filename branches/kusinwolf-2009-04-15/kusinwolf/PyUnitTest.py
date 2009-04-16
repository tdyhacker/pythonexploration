#!/usr/bin/env python

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    # Hook function designed to be overloaded for each function's test requirements
    def setUp(self):
        self.seq = range(10)

    # All test functions must start with the name test* and can be named anything else afterwards
    def testshuffle(self): # Random test 1
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10)) # Raised to check for an expected result

    def testchoice(self): # Random test 2
        element = random.choice(self.seq)
        self.assert_(element in self.seq) # Raised to verify a condition

    def testsample(self): # Random test 3
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq) # Raised to verify a condition

def buildsuite():
    '''
        If a specific order is required, or a pair of functions that need to be tested together
    '''
    tests = ['testshuffle', 'testchoice', 'testsample']

    return unittest.TestSuite(map(TestSequenceFunctions,
                                  ['testshuffle', 'testchoice', 'testsample']
                                 )
                             )


#if __name__ == '__main__':
#    unittest.main()

# This is used for finer ouput on each test
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions) # Simple way of building all the test cases
asuite = buildsuite()
unittest.TextTestRunner(verbosity=2).run(suite)

