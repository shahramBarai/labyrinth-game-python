'''
Created on 15.3.2019

@author: barai
'''
from coordinates import Coordinates

class Player():
    
    def __init__(self, name, world):
        
        self.name = name
        self.world = world
        self.location = None
        
    def set_location(self, location):
        '''Parameter location is the player location: Coordinates'''
        self.location = location
        
    def get_location(self):
        return self.location
    
    def try_to_move(self, a, b):
        x = self.location.get_x() + a
        y = self.location.get_y() + b
        if self.world.get_square(x,y).is_wall_square() != True:
            self.location = Coordinates(x, y)
        