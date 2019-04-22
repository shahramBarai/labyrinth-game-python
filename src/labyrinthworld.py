from square import Square
from player import Player
from coordinates import Coordinates
import random

class LabyrinthWorld():
    
    def __init__(self, width=0, height=0, square_size=0):
        self.create_grid(width, height, square_size)
        self.start_point = Coordinates(0, 0)
        self.player = Player("", self)
        self.directions = [(1,0),(0,1),(-1,0),(0,-1)] # [right, down, left, up]
        self.visited = []
        self.stack = []
        self.the_longest_way = []
        self.player_path = []
        self.end_point = None
        self.flag = 0
        self.endTime = (0, 0, 0)
    
    def create_grid(self, width, height, sq_size):
        self.square_size = sq_size
        self.squares = [None] * width
        for x in range(width):
            self.squares[x] = [None] * height
            for y in range(height):
                self.squares[x][y] = Square(x, y, self.square_size)
        
    def get_width(self): return len(self.squares)
    
    def get_height(self): return len(self.squares[0])
    
    def get_square_size(self): return self.square_size

    def get_square(self, x , y):
        '''Returns the square that is located at the given location.'''
        if 0 <= x < self.get_width() and 0 <= y < self.get_height():
                return self.squares[x][y]
        else: return None
        
    def get_player(self): return self.player
    
    def get_startPoint(self): return self.start_point
    
    def get_endPoint(self): return self.end_point
    
    def get_stack_list(self): return self.stack
    
    def get_player_path(self): return self.player_path
    
    def set_startPoint(self, x, y):
        self.start_point = Coordinates(x, y)
        self.player.set_location(Coordinates(x, y))
        self.player_path.append((x, y))
        self.get_square(x, y).setColor(250,250,250)
    
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
    
    def set_player(self, name): self.player.set_name(name)
    
    def set_endTime(self, time): self.endTime = time
    
    def get_endTime(self): return self.endTime
    
    def write_maze_to_file(self):
        fileName = "maze.txt"
        try:
            file = open(fileName, "w")
        except OSError:
            return False
        else:
            info = "{}:{}:{}:{}".format(self.player.get_name(), self.get_width(), self.get_height(), self.square_size)
            for t in self.endTime:
                info = info + ":" + str(t)
            info += "\n"
            file.write(info)
            for y in range(self.get_height()):
                line = ""
                for x in range(self.get_width()):
                    sq_t = ""
                    sq = self.get_square(x, y)
                    if sq.is_bottom_wall(): sq_t = sq_t + "_"
                    else: sq_t = sq_t + " "
                    if self.start_point.get_x() == x and self.start_point.get_y() == y: #add start point position
                        sq_t = sq_t + "s"
                    elif self.player.get_location().get_x() == x and self.player.get_location().get_y() == y: #add player position
                        sq_t = sq_t + "o"
                    elif self.end_point.get_x() == x and self.end_point.get_y() == y:   #add end point position
                        sq_t = sq_t + "e"
                    elif sq.getColor() != (200, 230, 200): sq_t = sq_t + "x"
                    else: sq_t = sq_t + " "
                    if sq.is_right_wall(): sq_t = sq_t + "|"
                    else: sq_t = sq_t + " "
                    line = line + sq_t
                file.write(line + "\n")
            file.close()
            
        return True
    
    def read_maze_from_file(self):
        fileName = "maze.txt"
        try:
            file = open(fileName, "r")
            info_line = file.readline()
            info_line = info_line.rstrip()
            info = info_line.split(":")
            self.player.set_name(info[0])
            self.create_grid(int(info[1]), int(info[2]), int(info[3]))
            time = (int(info[4]), int(info[5]), int(info[6]))
            self.set_endTime(time)

            y = 0
            for line in file:
                line = line.rstrip()
                count = 0
                x = 0
                for l in line:
                    if count == 0:
                        sq = Square(x, y, self.square_size)
                        sq.delete_bottom_wall()
                    elif count == 1:
                        if l == "s": self.set_startPoint(x, y)
                        elif l == "o": self.player.set_location(Coordinates(x, y))
                        elif l == "x": sq.setColor(200, 200 , 200, 200)
                        elif l == "e": self.end_point = Coordinates(x, y)
                    elif count == 2: 
                        sq.delete_right_wall()
                    if count >= 2: 
                        x += 1
                        count = 0
                    else: count += 1
                y += 1
            file.close()
        except OSError:
            return False
        except ValueError:
            file.close()
            return False
        return True
    def create_maze_randomly(self, show_generation, is_ready=False):
        while True:
            x = self.player.get_location().get_x()
            y = self.player.get_location().get_y()
            
            if ((x,y) not in self.visited): self.visited.append((x,y))
            if ((x,y) not in self.stack): self.stack.append((x,y))        
            
            if len(self.visited) == (self.get_height()*self.get_width()):
                self.player.set_location(self.start_point)
                self.set_endPoint()
                self.stack = self.the_longest_way.copy()
                is_ready = True
                break
            
            while True:
                squares_around = []
                for direction in self.directions:
                    a = x + direction[0]
                    b = y + direction[1]
                    if (0 <= a < self.get_width()) and (0 <= b < self.get_height()):
                        if (a,b) not in self.visited: squares_around.append(direction)
                
                if len(squares_around) != 0:
                    i = random.choice(squares_around)
                    square = self.squares[x][y]
                    if i == self.directions[0]:                 # going Righ
                        square.delete_right_wall()
                        x = x + 1
                    elif i == self.directions[1]:               # going Down
                        square.delete_bottom_wall()
                        y = y + 1
                    elif i == self.directions[2]:               # going Felft
                        x = x - 1
                        self.squares[x][y].delete_right_wall()
                    elif i == self.directions[3]:               # going Up
                        y = y - 1
                        self.squares[x][y].delete_bottom_wall()
                    break
                else:
                    if len(self.stack) <= 1:
                        is_ready = True
                        break
                    if len(self.stack) > len(self.the_longest_way):
                        self.the_longest_way = self.stack.copy()
                    self.stack.pop(-1)
                    x = self.stack[-1][0]
                    y = self.stack[-1][1]
            
            self.player.set_location(Coordinates(x,y))
            if show_generation:
                break
        return is_ready
    
    def preper_to_solving(self):
        x = self.player.get_location().get_x()
        y = self.player.get_location().get_y()
        self.stack = []
        self.visited = []
        if ((x,y) in self.the_longest_way) and Coordinates(x,y) != self.end_point:
            self.flag = 1
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
            return True
        
        if self.flag == 1:
            x = self.the_longest_way[-1][0]
            y = self.the_longest_way[-1][1]            
            self.the_longest_way.pop(-1)
        else:
            
            x = self.player.get_location().get_x()
            y = self.player.get_location().get_y()
            
            if Coordinates(x,y) == self.end_point: return True
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
                        return True
                    self.stack.pop(-1)
                    x = self.stack[-1][0]
                    y = self.stack[-1][1]
                
            if (x,y) in self.the_longest_way:
                self.flag = 1
                self.the_longest_way.reverse()
                while True:
                    if self.the_longest_way[-1] == (x,y):
                        break
                    self.the_longest_way.pop(-1)
                self.stack.reverse()
                self.stack = self.the_longest_way + self.stack
        
        self.player.set_location(Coordinates(x,y))
        return False

    def deleteWorld(self):
        self.visited = []
        self.stack = []
        self.the_longest_way = []
        self.player_path = []
        self.end_point = None
        self.flag = 0
        self.endTime = (0, 0, 0)