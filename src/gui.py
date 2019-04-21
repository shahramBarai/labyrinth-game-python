'''
Created on 10.3.2019
@author: barai
'''
from PyQt5 import QtWidgets, QtCore, QtGui
from player_graphics_item import PlayerGraphicsItem
from coordinates import Coordinates
from startmenu import StartMenu

class GUI(QtWidgets.QMainWindow):
    
    def __init__(self, world):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        
        #Creating Layouts
        self.winBox = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.winBox)
        
        self.gameBox = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QBoxLayout(2)                  #Direction "Top to Botttom"
        self.winBox.addLayout(self.gameBox, 8)
        self.winBox.addLayout(self.box, 2)
        
        self.world = world
        self.player = self.world.get_player()
        self.square_size = self.world.get_square_size()
        
        self.isStarted = False
        self.isMazeSolvided = False
        self.maze_is_ready = False
        self.time_interval = 1             # Milliseconds
        self.time = QtCore.QTime(0, 0, 0)
        self.length = 0                     # Start and end length
        self.player_steps = 0               # Player steps
        
        self.init_window()
        self.start_menu = StartMenu()
        self.gameBox.addLayout(self.start_menu.get_menuLayout())
        self.show()
        
        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_player)
        self.timer.start(self.time_interval)
        
    def add_labyrinth_world_grid_items(self):               #Draw a game zone
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                squareItem = self.world.get_square(x, y)    # Draw the walls
                self.scene.addItem(squareItem)
    
    def add_player_graphics_item(self):
        self.playerItem = PlayerGraphicsItem(self.player, self.square_size)
        self.playerItem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.scene.addItem(self.playerItem)
        
    def add_end_point(self):
        x = self.world.get_endPoint().get_x()
        y = self.world.get_endPoint().get_y()
        #endItem = QtWidgets.QGraphicsRectItem(x*self.square_size, y*self.square_size, self.square_size*0.85, self.square_size*0.85)
        self.world.get_square(x, y).setColor(0, 100, 0)
        #self.scene.addItem(endItem)
    
    def star_game(self):
        if self.game_button.text() == "Start": 
            self.create_game_field()
            if self.isStarted:
                self.game_button.setEnabled(False)
        elif self.game_button.text() == "New Game":
            self.give_up_button.setEnabled(False)
            self.create_menu_field()
    
    def create_menu_field(self):
        if self.isStarted: self.message_window()
        self.end_game()
        self.scene.deleteLater()
        self.view.deleteLater()
        self.world.deleteWorld()
        
        self.maze_is_ready = False
        self.isMazeSolvided = False
        self.time = QtCore.QTime(0, 0, 0)
        
        self.start_menu.create_menu()
        self.start_menu.set_name(self.player.get_name())
        self.gameBox.addLayout(self.start_menu.get_menuLayout())
        self.game_button.setText("Start")
            
    def create_game_field(self):
        self.darkRed = QtCore.Qt.darkRed
        error_text1 = '''Attention!!! The size of the map was entered incorrectly. The width and height (x, y) must be integers and greater than one.'''
        
        name = self.start_menu.get_name()
        if name != "": self.world.set_player(name)  
        else: 
            self.writeText("Write the name", self.darkRed)
            return

        size = self.start_menu.get_gameSize()
        if size != None:
            x = size[0]
            y = size[1]
            self.square_size = size[2]
            self.world.create_grid(x, y, self.square_size)
            i = self.start_menu.get_startPoint()                        # Set start position
            if i == 0: self.world.set_startPoint(0, 0)                  # Left_Up
            elif i == 1: self.world.set_startPoint(x-1, 0)              # Right_Up
            elif i == 2: self.world.set_startPoint(0, y-1)              # Left_Bottom
            elif i == 3: self.world.set_startPoint(x-1 , y-1)           # Right_Bottom
            elif i == 4: self.world.set_startPoint(int(x/2), int(y/2))  # Middle"
        else:
            self.writeText(error_text1, self.darkRed)
            return
        
        self.game_button.setText("New Game")
        self.isStarted = True
        self.start_menu.delete()
        self.writeText("Hi {}! Game Started!".format(self.player.get_name()))
        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
        self.view.setStyleSheet("border: 0px")
        self.gameBox.addWidget(self.view)
        # Creating world grid items and player graphic item
        self.add_labyrinth_world_grid_items()
        self.add_player_graphics_item()
        # Generate maze
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(self.generete_maze)
    
    def generete_maze(self):
        self.maze_is_ready = self.world.create_maze_randomly(self.start_menu.get_show_flag())
        if self.maze_is_ready:
            self.add_end_point()
            self.game_button.setEnabled(True)
            self.give_up_button.setEnabled(True)
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.update_player)
            
    def end_game(self):
        self.writeText("Game Ended!")
        self.give_up_button.setEnabled(False)
        self.isStarted = False
        
    def show_player_paht(self):
        for square in self.world.get_player_path():
            if square != self.world.get_player_path()[0]:
                x = square[0]
                y = square[1]
                square = self.world.get_square(x, y)
                square.setColor(200, 200 , 200, 200)
    
    def show_solving_way(self):
        x_end = self.world.get_endPoint().get_x()
        y_end = self.world.get_endPoint().get_y()
        if self.start_menu.get_tail_flag() == False: self.show_player_paht()
        for sq in self.world.get_stack_list():
            square = self.world.get_square(sq[0], sq[1])
            if (sq[0], sq[1]) != (x_end, y_end):                # Do not paint endpoint
                square.setColor(250, 250, 250)
        x = self.world.get_stack_list()[-1][0]
        y = self.world.get_stack_list()[-1][1]
        self.player.set_location(Coordinates(x, y))             # Put the player in place before solving
        
    def start_solving_maze(self):
        if self.maze_is_ready and self.isStarted:
            self.end_game()
            self.game_button.setEnabled(False)                  # Disabled "New Game" button
            self.world.preper_to_solving()
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.start_solving_maze)
            
        if self.maze_is_ready and self.isStarted == False:
            self.isMazeSolvided = self.world.solving_a_maze()   # Solving maze
            if self.isMazeSolvided:
                self.show_solving_way()                         # Show the way
                self.timer.timeout.disconnect()                 
                self.timer.timeout.connect(self.update_player)
                self.game_button.setEnabled(True)               # Enabled "New Game" button
            self.playerItem.update()
          
    def keyPressEvent(self, event):
        if self.isStarted and self.maze_is_ready == 1:
            key = event.key()
            if key == QtCore.Qt.Key_W or key == QtCore.Qt.Key_Up:
                self.player.try_to_move("UP")
            elif key == QtCore.Qt.Key_S or key == QtCore.Qt.Key_Down:
                self.player.try_to_move("DOWN")
            elif key == QtCore.Qt.Key_A or key == QtCore.Qt.Key_Left:
                self.player.try_to_move("LEFT")
            elif key == QtCore.Qt.Key_D or key == QtCore.Qt.Key_Right:
                self.player.try_to_move("RIGHT")
            self.checkPosition()

    def checkPosition(self):
        path = self.world.get_player_path()
        start = self.world.get_startPoint()
        end = self.world.get_endPoint()
        player = self.player.get_location()
        x = player.get_x()
        y = player.get_y()
        
        if self.start_menu.get_tail_flag() and (x, y) != (start.get_x(), start.get_y()):
            if ((x, y) in path) and ((x, y) != path[-1]):
                self.world.get_square(x, y).setColor(200, 200 , 200, 150)
            else:
                self.world.get_square(x, y).setColor(200, 200 , 200, 200)   
        if (x, y) not in path: path.append((x, y))
        self.world.get_square(x, y).update()
                
        if (x == end.get_x()) and (y == end.get_y()):
            self.end_game()
            self.show_solving_way()
        self.playerItem.update()
    
    def update_player(self):
        if self.isStarted and self.maze_is_ready:
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
        self.timeBox()
        self.console()
        self.score()
        self.init_buttons()
    
    def timeBox(self):
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
        self.box.addLayout(hbox, 1)
        
    def score(self):
        ''' Score '''
        scoreGBox = QtWidgets.QGroupBox("Score")
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
        
        scoreGBox.setLayout(vbox)
        self.box.addWidget(scoreGBox)
        
    def get_score(self, x):
        '''score = (100% * (start and end length) * time.s) / (player steps)'''
        pass
                  
    def console(self):
        self.textLine = 0
        self.textBox = QtWidgets.QTextBrowser()
        self.textBox.setFont(QtGui.QFont("Carlito"))                                        # Set text style
        self.textBox.setStyleSheet("QTextEdit {background-color:rgba(100, 100, 100, 250)}") # Set background color
        self.writeText("Welcome!")
        
        self.box.addWidget(self.textBox, 9)
        
    def writeText(self, string, color = QtCore.Qt.white):
        self.textBox.setTextColor(color)                                # Set text color
        self.textLine += 1
        line = str(self.textLine) + ": " + string
        self.textBox.append(line)

    def init_buttons(self):
        self.give_up_button = QtWidgets.QPushButton("Give Up")
        self.give_up_button.setEnabled(False)
        self.give_up_button.clicked.connect(self.start_solving_maze)
        self.game_button = QtWidgets.QPushButton("Start")
        self.game_button.clicked.connect(self.star_game)
        
        self.box.addWidget(self.give_up_button)
        self.box.addWidget(self.game_button)
            
    def safe_maze_to_file(self):
        time = (self.time.hour(), self.time.minute(), self.time.second())
        self.world.set_endTime(time)
        if self.world.write_maze_to_file():
            self.writeText("The maze has been saved!")
        else: self.writeText("Error! Something went wrong. We can not save the maze!")
        
    def message_window(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Message Window!")
        msg.setText("Do you want to save the maze?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg.buttonClicked.connect(self.message_button)
        msg.exec_()
    
    def message_button(self, i):
        if i.text() == "&Yes": self.safe_maze_to_file()