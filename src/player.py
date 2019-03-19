'''
Created on 15.3.2019

@author: barai
'''
from coordinates import Coordinates
from square import Square

class Player():
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = None
        self.location = None
        
    def set_location(self, location):
        '''Parameter location is the player location: Coordinates'''
        self.location = location
        
    def get_location(self):
        return self.location
    
    def set_world(self, world):
        self.world = world
    
    def move_up(self):
        self.location = Coordinates(self.location.get_x(), self.get_location().get_y() - 1)
        
    def move_down(self):
        self.location = Coordinates(self.location.get_x(), self.get_location().get_y() + 1)
        print("Pressed down!")