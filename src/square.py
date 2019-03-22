class Square():
    
    def __init__(self, is_wall=False):
        self.is_wall = is_wall
         
    def is_wall_square(self):
        return self.is_wall
    
    def set_wall(self):
        self.is_wall = True
            