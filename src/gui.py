'''
Created on 10.3.2019
@author: barai
'''
from PyQt5 import QtWidgets, QtCore, QtGui
from player_graphics_item import PlayerGraphicsItem

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self, world):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.grid = QtWidgets.QGridLayout(self)
        self.centralWidget().setLayout(self.grid)
        self.world = world
        self.square_size = self.world.get_square_size()

        self.game_started = 0
        self.solving_maze = 0
        
        self.init_window()
        self.init_buttons()

        self.add_labyrinth_world_grid_items()
        self.add_player_graphics_item()
        self.update_player()
        
        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_player)
        self.timer.start(1) # Milliseconds
    
    def add_labyrinth_world_grid_items(self):
        #Draw a game zone
        mapzoneItem = QtWidgets.QGraphicsRectItem(0, 0, self.square_size*self.world.get_width(), self.square_size*self.world.get_height())
        mapzoneItem.setBrush(QtGui.QColor(200, 230, 200))
        self.scene.addItem(mapzoneItem)
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                # Draw the walls
                squareItem = self.world.get_square(x, y)
                self.scene.addItem(squareItem)
    
    def add_player_graphics_item(self):
        self.playerItem = PlayerGraphicsItem(self.world.get_player(), self.square_size)
        self.playerItem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.scene.addItem(self.playerItem)
        
    def add_end_point(self):
        x = self.world.get_endPoint().get_x()
        y = self.world.get_endPoint().get_y()
        endItem = QtWidgets.QGraphicsRectItem(x*self.square_size, y*self.square_size, self.square_size*0.9, self.square_size*0.9)
        endItem.setBrush(QtGui.QColor(250,250,250))
        self.scene.addItem(endItem)
    
    def show_solving_way(self):
        a = 101
        b = 249
        c = 101
        for square in self.world.get_stack_list():
            x = square[0]
            y = square[1]
            squareItem = QtWidgets.QGraphicsRectItem(x*self.square_size, y*self.square_size, self.square_size*0.9, self.square_size*0.9)
            squareItem.setBrush(QtGui.QColor(a, b, c))
            self.scene.addItem(squareItem)
            if 100 < a < 250:
                a = a + 2
            elif 100 < b < 250:
                b = b - 2
            elif 100 < c < 250:
                c = c + 2
            else:
                a = 101
                b = 249
                c = 101
    
    def start_solving_maze(self):
        if self.game_started != 0 and self.world.get_endPoint() != None:
            self.game_started = 0
            self.solving_maze = 1
            self.world.preper_to_solving()
    
    def keyPressEvent(self, event):
        if self.game_started == 1:
            key = event.key()
            if key == QtCore.Qt.Key_W:
                self.world.get_player().try_to_move("UP")
            elif key == QtCore.Qt.Key_S:
                self.world.get_player().try_to_move("DOWN")
            elif key == QtCore.Qt.Key_A:
                self.world.get_player().try_to_move("LEFT")
            elif key == QtCore.Qt.Key_D:
                self.world.get_player().try_to_move("RIGHT")
            
    def keyReleaseEvent(self, event):
        if self.game_started == 1:
            key = event.key()
            if key == QtCore.Qt.Key_Up:
                self.world.get_player().try_to_move("UP")
            elif key == QtCore.Qt.Key_Down:
                self.world.get_player().try_to_move("DOWN")
            elif key == QtCore.Qt.Key_Left:
                self.world.get_player().try_to_move("LEFT")
            elif key == QtCore.Qt.Key_Right:
                self.world.get_player().try_to_move("RIGHT")
         
    def init_buttons(self):
        self.new_game_button = QtWidgets.QPushButton("New Game")
        self.give_up_button = QtWidgets.QPushButton("Give Up")
        self.give_up_button.clicked.connect(self.start_solving_maze)
          
        self.grid.addWidget(self.give_up_button, 5, 1)
        self.grid.addWidget(self.new_game_button, 6, 1)
        
    def update_player(self):
        if self.game_started == 0 and self.world.get_endPoint() == None:
            self.game_started = self.world.create_maze_randomly()
            if self.game_started == 1:
                self.add_end_point()
        if self.solving_maze == 1:
            self.solving_maze = self.world.solving_a_maze()
            if self.solving_maze == 0:
                self.show_solving_way()
                
            
        self.playerItem.update()
           
    def init_window(self):  
        # Sets up the window.
        self.setMinimumSize(680, 540)
        self.setMaximumSize(680, 540)
        self.setWindowTitle("Labyrinth Game")
        self.show()
        
        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
        self.view.show()
            
        self.grid.setColumnStretch(0, 8)
        self.grid.setColumnStretch(1, 2)
        self.grid.addWidget(self.view, 0, 0, 7, 1)
  