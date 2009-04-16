import os, sys
import pygame
from pygame import *
from pygame.locals import *
from Character import *

# Look into Panda 3D
# Look into PyOpenGL
# http://showmedo.com/videos/video?name=1510000&fromSeriesID=151

# Just the Engine mechanics

class Physics(object):
    def __init__(self):
        # On foot
        self.forwardgroundspeed = 45 # pxl a second
        self.backwardgroundspeed = 35 # pxl a second
        self.groundturnspeed = 0.8 # radians a second
        
        # In helicoptor
        self.forwardairspeed = 120 # pxl a second
        self.backwardairspeed = 45 # pxl a second
        self.airturnspeed = 0.4 # radians a second
        
        # In Small boat
        self.forwardwaterspeed = 80 # pxl a second
        self.backwardwaterspeed = 25 # pxl a second
        self.waterturnspeed = 0.5 # radians a second
        
        self.screenx = 800
        self.screeny = 600

class Engine(object):
    def __init__(self):
        """this function is called when the program starts.
           it initializes everything it needs, then runs in
           a loop until the function returns."""
        
        # Starting Physics Engine
        self.physics = Physics()
        
        #Initialize Everything
        pygame.init()
        self.screen = pygame.display.set_mode((self.physics.screenx, self.physics.screeny))
        pygame.display.set_caption("The Test of all Tests!")
        pygame.mouse.set_visible(1)
    
        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))
        
        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        
        #Prepare Game Objects
        self.clock = pygame.time.Clock()
        self.pointer = Character()
        pointer_draw = pygame.draw.circle(self.screen, (0,0,0), self.pointer.getPosition(0,0), 15)
        
        self.heldkeys = {}
    
    def mainloop(self):
        #Main Loop
        while 1:
            # Clean up the background
            self.background.fill((250, 250, 250))
            
            for event in self.heldkeys.itervalues():
                event() # run the method
            
            #Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.heldkeys[event.key] = self.ON_K_DOWN
                    elif  event.key == K_UP:
                        self.heldkeys[event.key] = self.ON_K_UP
                    elif event.key == K_LEFT:
                        self.heldkeys[event.key] = self.ON_K_LEFT
                    elif event.key == K_RIGHT:
                        self.heldkeys[event.key] = self.ON_K_RIGHT
                
                elif event.type == KEYUP:
                    if self.heldkeys.has_key(event.key):
                        self.heldkeys.pop(event.key)
            
            #Draw Everything
            pygame.display.flip()
    
    def ON_K_DOWN(self):
        self.pointer.position[1] += 2
        self.screen.blit(self.background, (0, 0))
        pointer_draw = pygame.draw.circle(self.screen, (0,0,0), self.pointer.getPosition(0,0), 15)
    
    def ON_K_UP(self):
        self.pointer.position[1] -= 2
        self.screen.blit(self.background, (0, 0))
        pointer_draw = pygame.draw.circle(self.screen, (0,0,0), self.pointer.getPosition(0,0), 15)
    
    def ON_K_LEFT(self):
        self.pointer.position[0] -= 2
        self.screen.blit(self.background, (0, 0))
        pointer_draw = pygame.draw.circle(self.screen, (0,0,0), self.pointer.getPosition(0,0), 15)
    
    def ON_K_RIGHT(self):
        self.pointer.position[0] += 2
        self.screen.blit(self.background, (0, 0))
        pointer_draw = pygame.draw.circle(self.screen, (0,0,0), self.pointer.getPosition(0,0), 15)