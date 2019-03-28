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
    
    def try_to_move(self, direction):
        x = self.location.get_x()
        y = self.location.get_y()

        if direction == "RIGHT" and self.world.get_square(x,y).is_right_wall() != True:
            x = x + 1
        if direction == "DOWN" and self.world.get_square(x,y).is_bottom_wall() != True:
            y = y + 1
            
        if x != 0 and direction == "LEFT" and self.world.get_square(x-1,y).is_right_wall() != True:
            x = x - 1
        if y != 0 and direction == "UP" and self.world.get_square(x,y-1).is_bottom_wall() != True:
            y = y - 1
        
        self.location = Coordinates(x, y)
        