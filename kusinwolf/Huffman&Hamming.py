import math

DEBUG = 0

class Branch:
    def __init__(self, left, right, value):
        ''' left and right should be Branch objects, value should be a Fraction object '''
        self.left = left # 0 Higher value
        self.right = right # 1 Lower value
        self.value = value # sum of left and right
    
    def __repr__(self):
        return " %s (0) -> %s <- (1) %s " % (self.left, self.value.eval(), self.right)
    
    def __cmp__(self, right):
        return self.value.__cmp__(right.value)
    
    def __add__(self, right):
        return self.value + right.value

    def traverse(self, num):
        if num == 0:
            return self.left
        elif num == 1:
            return self.right
        else:
            return "Error, 0 or 1 only"

class Node:
    def __init__(self, name, value):
        ''' name is a string/char, value is a Fraction object '''
        self.name = name
        self.value = value
        self.code = None

    def __repr__(self):
        return "|%s -> %.2f|" % (self.name, self.value.eval())

    def __cmp__(self, right):
        return self.value.__cmp__(right.value)

    def __add__(self, right):
        return self.value + right.value

class Fraction:
    def __init__(self, n, d, w = 0):
        ''' Pass in ints to be evalutated '''
        if (n / d) >= 1 and n != d:
            w += (n / d)
            n %= d
        self.numerator = int(n)
        self.denominator = int(d)
        self.whole = int(w)
        self.reduce()
        
    def __repr__(self):
        return "<Fraction - %.2f)>" % ((float(self.numerator) / self.denominator) + self.whole)
    
    def __add__(self, right):
        w = int(self.whole + right.whole)
        if not self.denominator == right.denominator:
            n = (self.numerator * right.denominator) + (self.denominator * right.numerator)
            d = (self.denominator * right.denominator) 
        else:
            n = self.numerator + right.numerator
            d = self.denominator
        return Fraction(n,d,w)
    
    def __cmp__(self, right):
        if self.whole != right.whole:
            return cmp(self.whole, right.whole)
        elif self.denominator == right.denominator:
            return cmp(self.numerator, right.numerator)
        else:
            return cmp((self.numerator * right.denominator), (self.denominator * right.numerator))
    
    def eval(self):
        if not self.denominator == 0:
            return (float(self.numerator) / float(self.denominator)) + self.whole
        else:
            return 0
    
    def reduce(self):
        div = 2
        while div <= self.numerator:
            if (self.numerator % div == 0) and (self.denominator % div == 0):
                self.numerator /= div
                self.denominator /= div
                dev = 2
            else:
                div += 1
        if self.numerator == self.denominator:
            self.whole += 1
            self.numerator = 0
            self.denominator = 1
    
def findFraction(num):
    num = float(num)
    w = 0
    if num >= 1:
        w += math.floor(num)
    if num >= 1 and (num % int(math.floor(num))) == 0:
        return Fraction(0,1,w)
    else:
        find = Fraction(0,1,w)
        while find.eval() != num:
            if find.eval() > num:
                find.denominator += 1
            elif find.eval() < num:
                find.numerator += 1
        return find

def findsmallest(nodes, tree):
    ''' finds the smallest and next smallest objects and returns them in highest to lowest order '''
    def findLowerASCII(node):
        chart = {}
        chart['A'] = chart['a'] = 65
        chart['B'] = chart['b'] = 66
        chart['C'] = chart['c'] = 67
        chart['D'] = chart['d'] = 68
        chart['E'] = chart['e'] = 69
        chart['F'] = chart['f'] = 70
        chart['G'] = chart['g'] = 71
        chart['H'] = chart['h'] = 72
        chart['I'] = chart['i'] = 73
        chart['J'] = chart['j'] = 74
        chart['K'] = chart['k'] = 75
        chart['L'] = chart['l'] = 76
        chart['M'] = chart['m'] = 77
        chart['N'] = chart['n'] = 78
        chart['O'] = chart['o'] = 79
        chart['P'] = chart['p'] = 80
        chart['Q'] = chart['q'] = 81
        chart['R'] = chart['r'] = 82
        chart['S'] = chart['s'] = 83
        chart['T'] = chart['t'] = 84
        chart['U'] = chart['u'] = 85
        chart['V'] = chart['v'] = 86
        chart['W'] = chart['w'] = 87
        chart['X'] = chart['x'] = 88
        chart['Y'] = chart['y'] = 89
        chart['Z'] = chart['z'] = 90
        chart['SP'] = chart['sp'] = 32
        chart['STX'] = chart['stx'] = 2
        chart['ETX'] = chart['etx'] = 3
        
        while isinstance(node, Branch):
            node = node.left
        
        return chart[node.name]
    
    # Nodes will always get the highest values (0)
    smallest = None
    nsmallest = None
    # Tree's will always get the lowest values (1)
    tsmallest = None
    tnsmallest = None
    for node in nodes:
        if smallest:
            if smallest > node:
                nsmallest = smallest
                smallest = node
            elif not nsmallest or nsmallest > node: # incase of none value, this takes the lead
                nsmallest = node
            elif smallest == node:
                l = findLowerASCII(smallest)
                r = findLowerASCII(node)
                if l > r:
                    nsmallest = smallest
                    smallest = node
                elif l < r:
                    if nsmallest == node:
                        l = findLowerASCII(nsmallest)
                        r = findLowerASCII(node)
                        if l > r:
                            nsmallest = node
                    elif nsmallest > node:
                        nsmallest = node
            elif nsmallest == node:
                l = findLowerASCII(nsmallest)
                r = findLowerASCII(node)
                if l > r:
                    nsmallest = node
        else:
            smallest = node
    for branches in tree:
        if tsmallest:
            if tsmallest > branches:
                tnsmallest = tsmallest
                tsmallest = branches
            elif not tnsmallest or tnsmallest > branches: # incase of none value, this takes the lead
                tnsmallest = branches
            elif tsmallest == branches:
                l = findLowerASCII(tsmallest)
                r = findLowerASCII(branches)
                if l > r:
                    tnsmallest = tsmallest
                    tsmallest = branches
                elif l < r:
                    if tnsmallest == branches:
                        l = findLowerASCII(tnsmallest)
                        r = findLowerASCII(branches)
                        if l > r:
                            tnsmallest = branches
                    elif tnsmallest > branches:
                        tnsmallest = branches
            elif tnsmallest == branches:
                l = findLowerASCII(tnsmallest)
                r = findLowerASCII(branches)
                if l > r:
                    tnsmallest = branches
        else:
            tsmallest = branches
    if tree and nodes: # if cross comparing the two groups
        # If the nodes are the same values and the lower branch is the same value, the higher branch is not
        if smallest and nsmallest and tsmallest and tnsmallest: # 2 nodes, 2 branches
            if smallest > tsmallest:
                if nsmallest > tnsmallest:
                    smallest = tsmallest
                    nsmallest = tnsmallest
                elif nsmallest == tnsmallest:
                    l = findLowerASCII(nsmallest)
                    r = findLowerASCII(tnsmallest)
                    if l > r:
                        nsmallest = tnsmallest
                else:
                    nsmallest = smallest
                    smallest = tsmallest
            elif smallest == tsmallest:
                if smallest >= tnsmallest:
                    smallest = tsmallest
                    nsmallest = tnsmallest
                else:
                    nsmallest = smallest
                    smallest = tsmallest
            elif nsmallest > tsmallest:
                nsmallest = tsmallest
            elif nsmallest == tsmallest:
                l = findLowerASCII(nsmallest)
                r = findLowerASCII(tsmallest)
                if l > r:
                    nsmallest = tsmallest
            # Rules for Tripel and Quad?
        elif smallest and nsmallest and tsmallest: # 2 nodes, 1 branch
            if smallest > tsmallest:
                nsmallest = smallest
                smallest = tsmallest
            elif smallest == tsmallest:
                l = findLowerASCII(smallest)
                r = findLowerASCII(tsmallest)
                if l > r:
                    nsmallest = smallest
                    smallest = tsmallest
                else:
                    if nsmallest > tsmallest:
                        nsmallest = tsmallest
                    elif nsmallest == tsmallest:
                        l = findLowerASCII(nsmallest)
                        r = findLowerASCII(tsmallest)
                        if l > r:
                            nsmallest = tsmallest
        elif smallest and tsmallest and tnsmallest: # 1 node, 2 branches
            if smallest > tsmallest:
                if smallest > tnsmallest:
                    smallest = tsmallest
                    nsmallest = tnsmallest
                elif smallest == tnsmallest:
                    l = findLowerASCII(smallest)
                    r = findLowerASCII(tnsmallest)
                    if l > r:
                        nsmallest = tnsmallest
                    else:
                        nsmallest = smallest
                else:
                    nsmallest = smallest
                    smallest = tsmallest
            elif smallest == tsmallest:
                l = findLowerASCII(smallest)
                r = findLowerASCII(tsmallest)
                if l > r:
                    l = findLowerASCII(smallest)
                    r = findLowerASCII(tnsmallest)
                    if l > r:
                        nsmallest = tnsmallest
                        smallest = tsmallest
                    else:
                        nsmallest = smallest
                        smallest = tsmallest
                else:
                    smallest = smallest
                    nsmallest = tsmallest
            else:
                nsmallest = tsmallest
        elif smallest and tsmallest: # 1 node, 1 branch
            if smallest > tsmallest:
                nsmallest = smallest
                smallest = tsmallest
            elif smallest == tsmallest:
                l = findLowerASCII(smallest)
                r = findLowerASCII(tsmallest)
                if l > r:
                    nsmallest = smallest
                    smallest = tsmallest
                else:
                    nsmallest = tsmallest
            else:
                nsmallest = tsmallest
    elif tree and not nodes: # if the nodes group is empty
        smallest = tsmallest
        nsmallest = tnsmallest
    # else and finally return the grouping in highest to lowest

    return (nsmallest, smallest)

def removeNode(lst, rnode):
    ''' Removes a node with similar name as the compare node and returns a list '''
    temp = []
    for node in lst:
        if node.name != rnode.name:
            temp.append(node)
    return temp

def removeBranch(lst, rbranch):
    ''' Removes a branch with similar 0 branch as the compare branch and returns a list '''
    temp = [] # Temp list
    node = rbranch.left # Comparing Branch
    cnode = None # Find removing Branch
    while not isinstance(node, Node):
        node = node.left # Go up the 0 branch of the subtree
    for branch in lst:
        cnode = branch.left
        while not isinstance(cnode, Node):
            cnode = cnode.left
        if cnode != node:
            temp.append(branch)
        #else:
        #   remove the branch
    return temp

if False: # Files and Database
    freq = [('n',14),('sp',13),('a',12.1),('i',10.7),('o',9.9),('s',7.3),('e',6.4),('u',6.0),('c',5.5),('d',4.1),('y',3.8),('t',3.6),('b',2.2),('m',0.8),('r',0.4),('stx',0.15),('etx',0.05)]
elif False: # Computer Arch
    freq = [('A',12.3),
            ('E',7.6),
            ('I',5.2),
            ('O',9.1),
            ('U',3.5),
            ('B',5.1),
            ('C',2.1),
            ('N',6.7),
            ('P',5.9),
            ('S',12.3),
            ('T',12.4),
            ('sp',17.5),
            ('etx',0.1),
            ('stx',0.2)]
elif True: # STX, LOL_PWNSAUCE,ETX
    freq = [('A',7.2),
            ('E',2),
            ('I',4),
            ('O',8.1),
            ('U',7.6),
            ('L',4),
            ('P',5),
            ('W',6),
            ('N',8),
            ('Z',9),
            ('T',10),
            ('R',4.5),
            ('S',3.2),
            ('V',2.7),
            ('C',4.3),
            ('sp',11.4),
            ('stx',1),
            ('etx',2)]
elif False:
    freq = [('A',7.9),
            ('E',4.6),
            ('I',8.2),
            ('O',5.3),
            ('U',2.4),
            ('S',6.5),
            ('C',4.8),
            ('L',11.3),
            ('T',1.7),
            ('K',6.8),
            ('Y',3.1),
            ('P',9.2),
            ('H',7.6),
            ('G',2.9),
            ('N',3.5),
            ('sp',13.7),
            ('stx',0.2),
            ('etx',0.3)]

nodes = [Node(node[0], findFraction(node[1]))for node in freq]
tree = []
temp = []
t = None

tempnodes = nodes[:] # makes a perfect copy

while True:
#def g():
    t = findsmallest(tempnodes, tree)
    value = t[0] + t[1] # will always be a Fraction object
    if DEBUG:
        print t
    
    #while (t[0] not in tree) or (t[0] not in tempnodes)
    if not tree or tree[0].value != Fraction(0,1,100):
        if isinstance(t[0], Node):
            tempnodes = removeNode(tempnodes, t[0])
        else:
            tree = removeBranch(tree, t[0])
        
        if isinstance(t[1], Node):
            tempnodes = removeNode(tempnodes, t[1])
        else:
            tree = removeBranch(tree, t[1])
            
    tree.append(Branch(t[0], t[1], value))
    temp.append(Branch(t[0], t[1], value))
    
#    print t
    if not tempnodes and len(tree) == 1:
        break # Do While

code = []

def trans(node):
    print "Left:",
    if isinstance(node.left, Node):
        code.append('0')
        node.code = code
        print node.left,
        print node.code
        code.pop()
    else:
        print node.left.value
    print "Value: %s" % node.value
    
    print "right:",
    if isinstance(node.right, Node):
        code.append('1')
        node.code = code
        print node.right,
        print node.code
        code.pop()
    else:
        print node.right.value
    
    if not isinstance(node.right, Node):
        print "->"
        code.append('1')
        trans(node.right)
    else:
        node.code = code
    if not isinstance(node.left, Node):
        print "<-"
        code.append('0')
        trans(node.left)
    else:
        node.code = code
    if code:
        code.pop()

#def getMessage(code):
    # inverse code and go in reverse

trans(tree[0])
