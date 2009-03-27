import threading
import time
from random import Random

class Server(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.score = 0
        self.players = 0
        self.playerlimit = 32
        self.whom = []
        self.CANCONNECT = False
        self.timealive = 0
        self.killall = False
        self.connections_over_time = {}
        self.ban_list = {}
    
    def __repr__(self):
        return "<Score = %d>" % self.score
    
    def run(self):
        while not self.killall:
            self.heartbeat()
            
        print "Shutting down server"
        
        for player in self.whom:
            self.playerLeave(player)
    
    def playerJoin(self, player):
        # Race condition happening here
        self.CANCONNECT = False
        
        if player not in self.connections_over_time:
            self.connections_over_time[player] = 1
        else:
            self.connections_over_time[player] += 1
        
        if self.connections_over_time[player] > 5:
            self.ban_list[player] = 5
            print "Player", player, "has been banned for flooding"
        
        if player in self.ban_list:
            print "Player", player, "was previously banned"
            player.alive = False # kill that player, muwhahah
            self.ban_list[player] += 5
        else:
            self.players += 1
            self.score -= 15
            self.whom.append(player)
            
            player.timeplayed = 0
            player.connected = True
        
        if self.players >= self.playerlimit:
            self.CANCONNECT = False
        else:
            self.CANCONNECT = True
        
        return self
    
    def playerLeave(self, player):
        self.players -= 1
        try:
            self.whom.remove(player)
        except:
            print player.name, " was not found in the list of connected players"
        
        player.connected = False
        
        if not self.CANCONNECT and not self.killall and self.players < self.playerlimit:
            self.CANCONNECT = True
    
    def heartbeat(self):
        self.timealive += 1
        for player in self.whom:
            player.timeplayed += 1
            
            if player.timeplayed <= 45:
                self.score += 1
            
            player.continuePlaying()
        
        temp_dict = self.ban_list.copy()
        for player in temp_dict:
            if self.ban_list[player] > 0:
                self.ban_list[player] -= 1
            if self.ban_list[player] == 0:
                self.ban_list.pop(player) # remove them from the ban list only after their time is up
                # if their time goes into negative it is a perminate ban
        
        temp_dict = self.connections_over_time.copy()
        for player in temp_dict:
            if self.connections_over_time[player] > 0:
                self.connections_over_time[player] -= 1
            else:
                self.connections_over_time.pop(player)

myserver = Server()
players = []

class Player(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        # So long as there is this many people on they'll stay on
        self.PreferedPlayerSize = int(Random().random() * 32) + 1 # Minus up to 4 players for tollerance
        self.AllowedTimeToPlay = int(Random().random() * 60.0) + 1
        self.timeplayed = 0
        self.server = myserver
        self.connected = False
        self.alive = True # Murder the process? :)
        self.name = name
    
    def __repr__(self):
        return "<Player %s Prefers %d players for a max time of %d and is alive(%s) and connected (%s)>" % (self.name, self.PreferedPlayerSize, self.AllowedTimeToPlay, self.alive, self.connected)
    
    def run(self):
        while self.alive:
            if self.server.killall:
                self.alive = False
            else:
                self.heartbeat()
    
    def heartbeat(self):
        if not self.connected:
            if self.server.CANCONNECT:
                if self.PreferedPlayerSize <= 10:
                    self.server.playerJoin(self)
                elif self.server.players >= (self.PreferedPlayerSize - int(Random().random() * 4)):
                    self.server.playerJoin(self)
                elif self.name == "Griefer":
                    self.server.playerJoin(self)
        elif self.name == "Griefer":
            self.server.playerLeave(self)

    def continuePlaying(self):
        if self.server.players < (self.PreferedPlayerSize - int(Random().random() * 4)) or self.timeplayed >= self.AllowedTimeToPlay:
            self.server.playerLeave(self)
            self.AllowedTimeToPlay = int(Random().random() * 60.0) + 1

for x in range(31):
    players.append(Player(x))
    players[x].start()

# Designed to try and ruin games
players.append(Player("Griefer"))
players[31].start()

myserver.start()
myserver.CANCONNECT = True
