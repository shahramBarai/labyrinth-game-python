'''
Created on 10.3.2019
@author: barai
'''
from PyQt5 import QtWidgets, QtCore, QtGui
from player_graphics_item import PlayerGraphicsItem
from coordinates import Coordinates

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self, world):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.grid = QtWidgets.QGridLayout(self)
        self.centralWidget().setLayout(self.grid)
        
        self.world = world
        self.square_size = self.world.get_square_size()
        self.flag = 0
        self.isStarted = False
        self.isMazeSolvided = False
        self.game_mode = 0
        
        self.time_interval = 10
        self.time = QtCore.QTime(0, 0, 0)
        
        self.init_window()
        self.init_buttons()
        self.show()
        
        # Creating maze and player
        self.add_labyrinth_world_grid_items()
        self.add_player_graphics_item()
        self.update_player()
        
        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_player)
        self.timer.start(self.time_interval) # Milliseconds
        
    def add_labyrinth_world_grid_items(self):
        #Draw a game zone
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
        endItem = QtWidgets.QGraphicsRectItem(x*self.square_size, y*self.square_size, self.square_size*0.85, self.square_size*0.85)
        endItem.setBrush(QtGui.QColor(250,250,250))
        self.scene.addItem(endItem)
    
    def start_game(self):
        self.isStarted = True
        print(self.nameEdit.text())
        self.start_button.setEnabled(False)
        self.nameEdit.setEnabled(False)
        self.cb.setEnabled(False)
        self.whriteText("Game Starded!")
        
    def end_game(self):
        self.isStarted = False
        self.whriteText("Game Ended!")
        
    def show_solving_way(self):
        a = 101
        b = 249
        c = 101
        for square in self.world.get_stack_list():
            x = square[0]
            y = square[1]
            square = self.world.get_square(x, y)
            square.setColor(a, b, c)
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
        x = self.world.get_stack_list()[-1][0]
        y = self.world.get_stack_list()[-1][1]
        self.world.get_player().set_location(Coordinates(x, y))  # put the player in place before solving
        
    def start_solving_maze(self):
        if self.flag == 1 and self.isStarted:
            self.end_game()
            self.isMazeSolvided = True
            self.world.preper_to_solving()
            self.timer.timeout.disconnect(self.update_player)
            self.time_interval = 10
            self.timer.start(self.time_interval)
            self.timer.timeout.connect(self.start_solving_maze)
        
        if self.isMazeSolvided == True and self.flag == 1 and self.isStarted == False:
            self.flag = self.world.solving_a_maze()
            if self.flag == 0:
                self.show_solving_way()
                self.timer.timeout.disconnect(self.start_solving_maze)
            self.playerItem.update()
            
            
    
    def checkPosition(self):
        player = self.world.get_player().get_location()
        end = self.world.get_endPoint()
        if (player.get_x() == end.get_x()) and (player.get_y() == end.get_y()):
            self.end_game()
    
    def keyPressEvent(self, event):
        if self.isStarted and self.flag == 1:
            key = event.key()
            if key == QtCore.Qt.Key_W:
                self.world.get_player().try_to_move("UP")
            elif key == QtCore.Qt.Key_S:
                self.world.get_player().try_to_move("DOWN")
            elif key == QtCore.Qt.Key_A:
                self.world.get_player().try_to_move("LEFT")
            elif key == QtCore.Qt.Key_D:
                self.world.get_player().try_to_move("RIGHT")
            self.checkPosition()
            
    def keyReleaseEvent(self, event):
        if self.isStarted and self.flag == 1:
            key = event.key()
            if key == QtCore.Qt.Key_Up:
                self.world.get_player().try_to_move("UP")
            elif key == QtCore.Qt.Key_Down:
                self.world.get_player().try_to_move("DOWN")
            elif key == QtCore.Qt.Key_Left:
                self.world.get_player().try_to_move("LEFT")
            elif key == QtCore.Qt.Key_Right:
                self.world.get_player().try_to_move("RIGHT")
            self.checkPosition()
            
    def update_player(self):
        if self.isStarted and self.flag == 0:
            self.flag = self.world.create_maze_randomly()
            if self.flag == 1:
                self.add_end_point()
                self.time_interval = 10
                self.timer.start(self.time_interval)
        if self.isStarted and self.flag == 1:
            self.timerEvent()
        self.playerItem.update()
    
    def timerEvent(self):
        self.time = self.time.addMSecs(self.time_interval)
        self.time_h_lcd.display(self.time.hour())
        self.time_m_lcd.display(self.time.minute())
        self.time_s_lcd.display(self.time.second())
           
    def init_window(self):  
        # Sets up the window.
        self.setMinimumSize(685, 535)
        self.setMaximumSize(685, 535)
        self.setWindowTitle("Labyrinth Game")
        
        ''' Name '''
        self.nameEdit = QtWidgets.QLineEdit()
        self.grid.addWidget(self.nameEdit, 0, 1)
        
        self.timeBox()
        self.gameMode()
        self.console()
        self.score()
        
        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
            
        self.grid.setColumnStretch(0, 8)
        self.grid.setColumnStretch(1, 2)
        self.grid.addWidget(self.view, 0, 0, 8, 1)
    

    def timeBox(self):
        ''' Timer '''
        self.time_h_lcd = QtWidgets.QLCDNumber(2)
        self.time_h_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.time_m_lcd = QtWidgets.QLCDNumber(2)
        self.time_m_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.time_s_lcd = QtWidgets.QLCDNumber(2)
        self.time_s_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        
        lb = QtWidgets.QLabel(":")
        lb2 = QtWidgets.QLabel(":")
        
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.time_h_lcd)
        hbox.addWidget(lb)
        hbox.addWidget(self.time_m_lcd)
        hbox.addWidget(lb2)
        hbox.addWidget(self.time_s_lcd)
        hbox.addStretch(1)
        self.grid.setRowStretch(1, 1)
        self.grid.addLayout(hbox, 1, 1)
        
    def score(self):
        ''' Score '''
        groupBox = QtWidgets.QGroupBox("Score")
        vbox = QtWidgets.QVBoxLayout()
        sl1 = QtWidgets.QLabel("1.")
        sl2 = QtWidgets.QLabel("2.")
        sl3 = QtWidgets.QLabel("3.")
        sl4 = QtWidgets.QLabel("4.")
        sl5 = QtWidgets.QLabel("5.")
        
        vbox.addWidget(sl1)
        vbox.addWidget(sl2)
        vbox.addWidget(sl3)
        vbox.addWidget(sl4)
        vbox.addWidget(sl5)
        vbox.addStretch(1)
        
        groupBox.setLayout(vbox)
        self.grid.addWidget(groupBox, 2, 1)
                  
    def console(self):
        ''' Console '''
        self.textLine = 0
        self.textBox = QtWidgets.QTextBrowser()
        self.textBox.setFont(QtGui.QFont("Carlito"))                                        # Set text style
        self.textBox.setTextColor(QtGui.QColor(255, 255, 255))                              # Set text color 
        self.textBox.setStyleSheet("QTextEdit {background-color:rgba(100, 100, 100, 125)}") # Set background color
        self.whriteText("Welcome!")
        
        self.grid.addWidget(self.textBox, 3, 1)
        self.grid.setRowStretch(3, 6)
        
    def whriteText(self, string):
        self.textLine += 1
        line = str(self.textLine) + ": " + string
        self.textBox.append(line)
        
    def gameMode(self):        
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(["Easy", "Normal", "Hard"])
        self.cb.currentIndexChanged.connect(self.changeGameMode)
        
        self.grid.addWidget(self.cb, 4, 1)
    
    def changeGameMode(self, i):
        self.game_mode = i
        print(i)
        
    def init_buttons(self):
        self.start_button = QtWidgets.QPushButton("Start")
        give_up_button = QtWidgets.QPushButton("Give Up")
        new_game_button = QtWidgets.QPushButton("New Game")
        
        self.start_button.clicked.connect(self.start_game)
        give_up_button.clicked.connect(self.start_solving_maze)
        
        self.grid.addWidget(self.start_button, 5, 1)
        self.grid.addWidget(give_up_button, 6, 1)
        self.grid.addWidget(new_game_button, 7, 1)
