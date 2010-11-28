import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from routing.lib.base import BaseController, render

from visual import *
from random import randrange, seed
from datetime import datetime
from routing.model.Database import DB

log = logging.getLogger(__name__)

class PresentationController(BaseController):
    def __before__(self):
        db = DB()
        db.create_DB()
    
    def index(self):
        """seed(datetime)""" """Removed because it stopped randomizing"""
        swidth = .50
        
        """Nodes"""
        num3=randrange(1,5)
        A=sphere(radius=1, pos=(-20, 0, 0), color=color.red)
        """radarA=sphere(radius=radical, pos=A.pos, color=color.red, opacity=(0.33))"""
        label(pos=A.pos+vector(0,2,0), text='A', height=10)
        
        Z=sphere(radius=1, pos=(25, 0, 0), color=color.red)
        label(pos=Z.pos+vector(0,2,0), text='(%i,0)' % num3, height=10)
        label(pos=Z.pos+vector(0,3,0), text='Z', height=10)
        """Z and A are not randomly generated so that they may stay as a constant"""    
        basicnode_list = ["B","C","D","E","F","G","H","I","J","K","L"]
        node = 1
        node_list = [A]
        x = 0
        
        """This is the creator for the nodes and their labels"""
        for letter in basicnode_list:
            node=sphere(radius=1, pos=(randrange(-19,24), randrange(-10,10), randrange(-20,20)), color=color.blue)
            """radar=sphere(radius=radical, pos=node.pos, color=(1,1,0.5), opacity=(0.33))"""
            num1=randrange(1,5)
            num2=randrange(1,5)
            label(pos=node.pos+vector(0,2,0), text='(%i,%i)' % (num1, num2), height=10)
            label(pos=node.pos+vector(0,3,0), text=letter, height=10)
            node_list.append(node)
        
        radical = 20
        node_distance_array = []
        node_list.append(Z)
        location = 0
        
        """This creates the vectors (arrows between the nodes)"""
        for value in node_list: 
        
            if value == Z:
                break;
            arrow_creator = arrow(pos=node_list[x].pos, axis=node_list[x+1].pos-node_list[x].pos, shaftwidth=swidth, fixedwidth = True, opacity=0)
            node_distance_array.append(arrow_creator.length)
            del arrow_creator
            x=x+1
        """node_distance_array.append((node_list[x].pos-node_list[x+1].pos)) <-- original way i was doing it, the hard way lol"""
        
        firstnum=0
        secondnum=1
        
        while firstnum!=len(node_list):
            for nodeschecker in node_list:
                if secondnum == len(node_list):
                    break;
                goober = arrow(pos=node_list[firstnum].pos, axis=node_list[secondnum].pos-node_list[firstnum].pos, shaftwidth=swidth, fixedwidth = True, opacity=0)
                if goober.length <= radical:
                    print goober.length
                    temp=randrange(1,5)
                    temp2=randrange(1,5)
                    arrow(pos=node_list[firstnum].pos, axis=node_list[secondnum].pos-node_list[firstnum].pos, shaftwidth=swidth, fixedwidth = True)
                    label(pos=(node_list[firstnum].pos+node_list[secondnum].pos)/2, text='(%i,%i)' % (temp, temp2), height=10, color=(1,1,0))
                del goober
                secondnum=secondnum+1
            firstnum=firstnum+1
            secondnum=firstnum+1'
