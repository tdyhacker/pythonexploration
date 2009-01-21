import math

class Branch:
    def __init__(self, left, right, value):
        ''' left and right should be Branch objects, value should be a Fraction object '''
        self.left = left # 0 Higher value
        self.right = right # 1 Lower value
        self.value = value # sum of left and right
    
    def __repr__(self):
        return "(0) %s -> %s <- %s (1)" % (self.left, self.value, self.right)
    
    def __cmp__(self, right):
        return cmp(self.value, right.value)
    
    def __add__(self, right):
        return self.value + right.value

class Fraction:
    def __init__(self, n, d, w = 0):
        ''' Pass in ints to be evalutated '''
        if (n / d) >= 1 and n != d:
            w += (n / d)
            n %= d
        self.numerator = float(n)
        self.denominator = float(d)
        self.whole = w
        self.reduce()
        
    def __repr__(self):
        return "<Fraction - %s + (%s/%s)>" % (int(self.whole), int(self.numerator), int(self.denominator))
    
    def __add__(self, right):
        w = self.whole + right.whole
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
        return (self.numerator / self.denominator) + self.whole
    
    def reduce(self):
        div = 2
        while div <= self.numerator:
            if (self.numerator % div == 0) and (self.denominator % div == 0):
                div = 2
                self.numerator /= div
                self.denominator /= div
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

def findsmallest(tempnodes, trees):
    ''' finds the smallest and next smallest objects and returns them in highest to lowest order '''
    smallest = tempnodes[0]
    nsmallest = tempnodes[0]
    tsmallest = trees[0]
    tnsmallest = trees[0]
    for node in tempnodes:
        if smallest[1] > node[1]:
            nsmallest = smallest
            smallest = node
        elif nsmallest[1] > node[1]:
            nsmallest = node
    for branches in trees:
        if smallest > branches.value
    return (nsmallest, smallest)

freq = [('n',14),('sp',13),('a',12.1),('i',10.7),('o',9.9),('s',7.3),('e',6.4),('u',6.0),('c',5.5),('d',4.1),('y',3.8),('t',3.6),('b',2.2),('m',0.8),('r',0.4),('stx',0.15),('etx',0.05)]
nodes = [(node[0], findFraction(node[1]))for node in freq]
trees = []

tempnodes = nodes[:] # makes a perfect copy
t = findsmallest(tempnodes, trees)

value = t[0][1] + t[1][1] # will always be a Fraction object

trees.append(Branch(t[0], t[1], value))
tempnodes.remove(t[0])
tempnodes.remove(t[1])