from square import Square

class LabyrinthWorld():
    
    def __init__(self, width, height):
        self.squares = [None] * width
        for x in range(self.get_width()):
            self.squares[x] = [None] * height
            for y in range(self.get_height()):
                self.squares[x][y] = Square()

        
    def get_width(self):
        return len(self.squares)
    
    def get_height(self):
        return len(self.squares[0])
    
    def get_square(self, x , y):
        return self.squares[x][y]
    
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
                    x += 1
                y += 1      
                        