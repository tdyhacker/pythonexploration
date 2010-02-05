
def printTable(truth_table):
    for key in truth_table['order']:
        print key, "\t",
    print ""
    
    for item in truth_table['order']:
        print "-------",
    print ""
    
    for row in range(len(truth_table[truth_table['order'][0]])):
        for col in range(len(truth_table['order'])):
            print truth_table[truth_table['order'][col]][row], "\t",
        print ""

def buildTruths(truth_table):
    value = True
    
    # Assign the columns automatically
    for col in truth_table['order']:
        truth_table[col] = []
        truth_table["~%s" % col] = []
        
        while len(truth_table[col]) < pow(2, len(truth_table['order'])):
            for var in range(pow(2, len(truth_table['order']) - (truth_table['order'].index(col) + 1) ) ):
                truth_table[col].append(value)
                truth_table["~%s" % col].append(not value) # Inverses
            value = value ^ True # Similar to an xor operator without writing my own
        
        value = True

def evaluatePart(left, word, right):
    if word == "V":
        return left and right
    elif word == "^":
        return left or right
    elif word == "->":
        return not left or right
    elif word == "<->":
        return not (left ^ right) # not (left xor right)

def evaluateEquation(truth_table):
    equation = truth_table['equation']
    groups = truth_table['equation'].split(" ")
    truth_table[equation] = []
    for row in range(pow(2, len(truth_table['order']))):
        truth_table[equation].append(evaluatePart(truth_table[groups[0]][row], groups[1], truth_table[groups[2]][row]))

truth_table = {}
truth_table['order'] = ['P', 'Q', 'W',]
truth_table['equation'] = "~P -> Q"

# V = or
# ^ = and

buildTruths(truth_table)
evaluateEquation(truth_table)
truth_table['order'].append(truth_table['equation']) # Cheat for printing out :P
printTable(truth_table)
