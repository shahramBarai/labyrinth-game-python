from square import Square
from player import Player
from coordinates import Coordinates
import random

class LabyrinthWorld():
    
    def __init__(self, width, height, square_size):
        self.square_size = square_size
        self.squares = [None] * width
        for x in range(self.get_width()):
            self.squares[x] = [None] * height
            for y in range(self.get_height()):
                self.squares[x][y] = Square(x, y, self.square_size)
                
        self.player = Player
        self.directions = [(1,0),(0,1),(-1,0),(0,-1)] # [right, down, left, up]
        self.visited = []
        self.stack = []

        
    def get_width(self):
        return len(self.squares)
    
    def get_height(self):
        return len(self.squares[0])
    
    def get_square_size(self):
        return self.square_size
    
    def get_square(self, x , y):
        '''Returns the square that is located at the given location. If the given coordinates point outside of the world,
        this method returns a square that contains a wall and is not located in any labyrinth world'''
        if 0 <= x < self.get_width() and 0 <= y < self.get_height():
                return self.squares[x][y]
        else: return Square(True) 
        
    def get_stack_list(self):
        return self.stack
    
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
    
    def create_maze_randomly(self):
        x = self.player.get_location().get_x()
        y = self.player.get_location().get_y()
        k = True
        
        if len(self.visited) == (self.get_height()*self.get_width())-1:
            return 1
        
        if ((x,y) not in self.visited): self.visited.append((x,y))
        if ((x,y) not in self.stack): self.stack.append((x,y))
        
        while k:
            squares_around = []
            for direction in self.directions:
                a = x + direction[0]
                b = y + direction[1]
                if (0 <= a < self.get_width()) and (0 <= b < self.get_height()):
                    if (a,b) not in self.visited: squares_around.append(direction)
            
            if len(squares_around) != 0:
                i = random.choice(squares_around)
                '''
                print("visit: ",self.visited)
                print("stack: ", self.stack)
                print("squares_around: ", squares_around)
                print("x:", x," y:", y)
                print("random:", i)
                '''
                square = self.squares[x][y]
                if i == self.directions[0]:                 # going Righ
                    square.delete_right_wall()
                    square.update()
                    x = x + 1
                elif i == self.directions[1]:               # going Down
                    square.delete_bottom_wall()
                    square.update()
                    y = y + 1
                elif i == self.directions[2]:               # going Felft
                    x = x - 1
                    self.squares[x][y].delete_right_wall()
                    self.squares[x][y].update()
                elif i == self.directions[3]:               # going Up
                    y = y - 1
                    self.squares[x][y].delete_bottom_wall()
                    self.squares[x][y].update()
                k = False
            else:
                if len(self.stack) == 0:
                    return 1
                self.stack.pop(-1)
                x = self.stack[-1][0]
                y = self.stack[-1][1]
        
        self.player.set_location(Coordinates(x,y))
        return 0
                
                
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        