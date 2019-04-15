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
        self.the_longest_way = []
        self.start_point = Coordinates(0,0)
        self.end_point = None
        
        self.flag = 0
        
    def get_width(self):
        return len(self.squares)
    
    def get_height(self):
        return len(self.squares[0])
    
    def get_square_size(self):
        return self.square_size
    
    def get_startPoint(self):
        return self.start_point
    
    def set_endPoint(self):
        if len(self.stack) > len(self.the_longest_way):
            self.the_longest_way = self.stack.copy()
            
        if len(self.the_longest_way) == 0:
            x = self.visited[-1][0]
            y = self.visited[-1][1]
        else:
            x = self.the_longest_way[-1][0]
            y = self.the_longest_way[-1][1]
        self.end_point = Coordinates(x, y)
        
    def get_endPoint(self):
        return self.end_point
    
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
        
    '''   need to change
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
    '''
    
    def create_maze_randomly(self):
        x = self.player.get_location().get_x()
        y = self.player.get_location().get_y()
        
        if ((x,y) not in self.visited): self.visited.append((x,y))
        if ((x,y) not in self.stack): self.stack.append((x,y))        
        
        if len(self.visited) == (self.get_height()*self.get_width()):
            self.player.set_location(self.start_point)
            self.set_endPoint()
            return 1
        
        while True:
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
                break
            else:
                if len(self.stack) <= 1:
                    return 1
                if len(self.stack) > len(self.the_longest_way):
                    self.the_longest_way = self.stack.copy()
                self.stack.pop(-1)
                x = self.stack[-1][0]
                y = self.stack[-1][1]
        
        self.player.set_location(Coordinates(x,y))
        return 0
    
    def preper_to_solving(self):
        x = self.player.get_location().get_x()
        y = self.player.get_location().get_y()
        self.stack = []
        self.visited = []
        if (x,y) in self.the_longest_way:
            self.flag = 1
            self.the_longest_way.pop(-1)
            self.the_longest_way.reverse()
            while True:
                if self.the_longest_way[-1] == (x,y):
                    break
                self.the_longest_way.pop(-1)
            self.stack = self.the_longest_way.copy()
        else: 
            self.flag = 0
        
    
    def solving_a_maze(self):
        if len(self.the_longest_way) == 0:
            return 0
        
        if self.flag == 1:
            x = self.the_longest_way[-1][0]
            y = self.the_longest_way[-1][1]            
            self.the_longest_way.pop(-1)
        else:
            
            x = self.player.get_location().get_x()
            y = self.player.get_location().get_y()
            
            if ((x,y) not in self.visited): self.visited.append((x,y))
            if ((x,y) not in self.stack): self.stack.append((x,y)) 

            while True:
                squares_around = []
                if (self.squares[x][y].is_right_wall() != True) and ((x+1, y) not in self.visited):
                    squares_around.append((x+1, y))
                if (self.squares[x][y].is_bottom_wall() != True) and ((x, y+1) not in self.visited):
                    squares_around.append((x, y+1))
                if (self.squares[x-1][y].is_right_wall() != True) and ((x-1, y) not in self.visited):
                    squares_around.append((x-1, y))
                if (self.squares[x][y-1].is_bottom_wall() != True) and ((x, y-1) not in self.visited):
                    squares_around.append((x, y-1))

                if len(squares_around) != 0:
                    i = random.choice(squares_around)
                    x = i[0]
                    y = i[1]
                    break
                else:
                    if len(self.stack) <= 1:
                        return 0
                    self.stack.pop(-1)
                    x = self.stack[-1][0]
                    y = self.stack[-1][1]
                
            if (x,y) in self.the_longest_way:
                self.flag = 1
                self.the_longest_way.pop(-1)
                self.the_longest_way.reverse()
                while True:
                    if self.the_longest_way[-1] == (x,y):
                        break
                    self.the_longest_way.pop(-1)
                self.stack = self.stack + self.the_longest_way
        
        self.player.set_location(Coordinates(x,y))
        return 1







































