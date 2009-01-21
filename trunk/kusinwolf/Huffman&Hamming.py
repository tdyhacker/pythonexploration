import math

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

    def __repr__(self):
        return "|%s -> %s|" % (self.name, self.value.eval())

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
        return "<Fraction - %s + (%s/%s)>" % (self.whole, self.numerator, self.denominator)
    
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
        return (float(self.numerator) / float(self.denominator)) + self.whole
    
    def reduce(self):
        div = 2
        while div <= self.numerator:
            if (self.numerator % div == 0) and (self.denominator % div == 0):
                self.numerator /= div
                self.denominator /= div
                dev = 2
            else:
                div += 1
    
def findFraction(num):
    num = float(num)
    w = 0
    if num >= 1:
        w += math.floor(num)
    if num >= 1 and (num % int(math.floor(num))) == 0:
        return Fraction(0,1,w)
    else:
        find = Fraction(1,1,w)
        while find.eval() != num:
            if find.eval() > num:
                find.denominator += 1
            elif find.eval() < num:
                find.numerator += 1
        return find

def findsmallest(nodes, tree):
    ''' finds the smallest and next smallest objects and returns them in highest to lowest order '''
    # Nodes will always get the highest values (0)
    if nodes:
        smallest = nodes[0]
        nsmallest = nodes[0]
    if tree:
        # Tree's will always get the lowest values (1)
        tsmallest = tree[0]
        tnsmallest = tree[0]
    for node in nodes:
        if smallest > node:
            nsmallest = smallest
            smallest = node
        elif nsmallest > node:
            nsmallest = node
    for branches in tree:
        if tsmallest == tnsmallest and tsmallest < branches:
            tnsmallest = branches
        if tsmallest > branches:
            tnsmallest = tsmallest
            tsmallest = branches
        elif tnsmallest > branches:
            tnsmallest = branches
    if tree and nodes:
        if not tsmallest == tnsmallest and not smallest == nsmallest:
            if nsmallest > tsmallest:
                smallest = tsmallest
                nsmallest = tnsmallest
            elif smallest < tsmallest and nsmallest > tsmallest:
                nsmallest = tsmallest
        elif smallest == nsmallest:
            nsmallest = tsmallest
        else:
            if nsmallest > tsmallest:
                nsmallest = smallest
                smallest = tsmallest
            elif smallest < tsmallest and nsmallest > tsmallest:
                nsmallest = tsmallest
    elif tree and not nodes:
        smallest = tsmallest
        nsmallest = tnsmallest
    return (nsmallest, smallest)

freq = [('n',14),('sp',13),('a',12.1),('i',10.7),('o',9.9),('s',7.3),('e',6.4),('u',6.0),('c',5.5),('d',4.1),('y',3.8),('t',3.6),('b',2.2),('m',0.8),('r',0.4),('stx',0.15),('etx',0.05)]
nodes = [Node(node[0], findFraction(node[1]))for node in freq]
tree = []

tempnodes = nodes[:] # makes a perfect copy

while True:
    t = findsmallest(tempnodes, tree)
    value = t[0] + t[1] # will always be a Fraction object
    tree.append(Branch(t[0], t[1], value))
    if t[0] != t[1]:
        if isinstance(t[0], Node):
            tempnodes.remove(t[0])
        else:
            tree.remove(t[0])
        if isinstance(t[1], Node):
            tempnodes.remove(t[1])
        else:
            tree.remove(t[1])
    else:
        if isinstance(t[0], Node):
            tempnodes.remove(t[0])
        else:
            tree.remove(t[0])

    if not tempnodes and len(tree) == 1:
        break # Do While

def t(node):
    if not isinstance(node, Node):
        t(node.right)
        t(node.left)
    print node.value
