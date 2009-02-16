import threading
import random

class SingleCell(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        # upper percentages - 30% chance to die then 70% chance to live
        self.chanceToDie = 0.05 #random.Random().random()
        self.uniqueID = random.Random().random()
        self.lifecount = 0
        self.alive = True
        self.waitingForInput = False
        self.name = name
        self.info = None
    
    def run(self):
        while self.alive:
            # if alive and chance to die is greater then the random chance, then die
            if self.alive and self.chanceToDie > random.Random().random():
                #print "%s: Oh no, I'm dying x_x" % self.name
                self.alive = False
                self.waitingForInput = False
            else:
                self.lifecount += 1
            
            self.waitingForInput = True
            
            while self.waitingForInput and self.alive:
                continue
            
            print self.name, ":", self.info
            
            while self.info > 0:
                self.info -= 0.0001
            
        print "%s : I lived for %s ticks" % (self.name, self.lifecount)
    
    def lostParent(self):
        self.waitingForInput = False
        self.alive = False
        print self.name, "lost my parent and my way :("
    
    def isWaiting(self):
        return self.waitingForInput
    
    def process(self, info):
        self.waitingForInput = False
        self.info = info + self.uniqueID + 1

## Run a SingleCell instance
#wholelist = []
#
#for names in range(50):
#    wholelist.append(SingleCell("N%s" % names))
#    wholelist[names].start()


class MultiCell(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        
        self.alive = True
        self.name = name
    
    def run(self):
        c1 = SingleCell("c1")
        c2 = SingleCell("c2")
        
        c1.start()
        c2.start()
        
        #while c1.alive and c2.alive: # If one cell dies, the whole cell dies
        while c1.alive or c2.alive: # If both cells die, the whole cell dies
            if c1.isWaiting:
                c1.process(int(random.Random().random() * 10))
            if c2.isWaiting:
                c2.process(int(random.Random().random() * 10))
        
        if c1.alive:
            c1.lostParent()
        if c2.alive:
            c2.lostParent()
        
        print self.name, "has died"


# Run a MultiCell instance
mc = MultiCell("MC1")
mc.start()

# Once everything is done let the programmer know as well
while threading.activeCount() != 1:
    continue

print "I'm done"