'''
Created on 10.3.2019
@author: barai
'''
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self, world, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.grid = QtWidgets.QGridLayout(self)
        self.centralWidget().setLayout(self.grid)
        self.world = world
        self.square_size = square_size
        
        self.init_window()
        self.init_buttons()
        self.show()
        
    def init_window(self):  # Sets up the window.
        self.setMinimumSize(680, 540)
        self.setMaximumSize(680, 540)
        self.setWindowTitle("Labyrinth Game")
        
        self.scene = QtWidgets.QGraphicsScene()
        self.add_labyrinth_world_grid_items()
        
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
            
        self.grid.setColumnStretch(0, 8)
        self.grid.setColumnStretch(1, 2)
        self.grid.addWidget(self.view, 0, 0, 7, 1)
        
        self.show()

         
    def init_buttons(self):
        self.new_game_button = QtWidgets.QPushButton("New Game")
        self.give_up_button = QtWidgets.QPushButton("Give Up")
            
        self.grid.addWidget(self.give_up_button, 5, 1)
        self.grid.addWidget(self.new_game_button, 6, 1)
        
    def add_labyrinth_world_grid_items(self):
        for y in range(self.world.get_height()):
            for x in range(self.world.get_width()):
                SquareItem = QtWidgets.QGraphicsRectItem(x * self.square_size, y * self.square_size, self.square_size, self.square_size)
                if self.world.get_square(x, y).is_wall_square():
                    SquareItem.setBrush(QBrush(Qt.black))
                self.scene.addItem(SquareItem)

        
      
        