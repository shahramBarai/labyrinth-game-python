from square import Square
from player import Player
from coordinates import Coordinates

class LabyrinthWorld():
    
    def __init__(self, width, height):
        self.squares = [None] * width
        for x in range(self.get_width()):
            self.squares[x] = [None] * height
            for y in range(self.get_height()):
                self.squares[x][y] = Square()
                
        self.player = Player

        
    def get_width(self):
        return len(self.squares)
    
    def get_height(self):
        return len(self.squares[0])
    
    def get_square(self, x , y):
        '''Returns the square that is located at the given location. If the given coordinates point outside of the world,
        this method returns a square that contains a wall and is not located in any labyrinth world'''
        if 0 <= x < self.get_width() and 0 <= y < self.get_height():
                return self.squares[x][y]
        else: return Square(True) 
        
    
    def get_player(self):
        return self.player
    
    def set_player(self, player):
        '''Parameter player is the player to be added: Player'''
        self.player = player
        
    
    def read_labyrinth_mapFolder(self, path):
        try:
            file = open(path)
        except OSError:
            print("Could not open {}".format(path))
        else:
            y = 0
            for line in file:
                line.rsplit()
                x = 0
                for l in line:
                    if l == "x":
                        self.squares[x][y].set_wall()
                    elif l == "s":
                        self.player.set_location(Coordinates(x, y))
                    x += 1
                y += 1
