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
        
        #Creating Layouts
        self.winBox = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.winBox)
        
        self.gameBox = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QBoxLayout(2)                  #Direction "Top to Botttom"
        self.winBox.addLayout(self.gameBox, 8)
        self.winBox.addLayout(self.box, 2)
        
        self.world = world
        self.square_size = self.world.get_square_size()
        self.flag = 0
        self.isStarted = False
        self.isMazeSolvided = False
        self.game_mode = 0
        
        self.time_interval = 1             # Milliseconds
        self.time = QtCore.QTime(0, 0, 0)
        
        self.init_window()
        self.init_buttons()
        self.start_menu()
        self.show()
        
        self.bob = 0
        # Set a timer to call the update function periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_player)
        self.timer.start(self.time_interval)
        
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
        endItem.setBrush(QtGui.QColor(250, 250, 250))
        self.scene.addItem(endItem)
    
    def start_game(self):
        self.new_game_button.setEnabled(False)
        darkRed = QtCore.Qt.darkRed
        if self.game_mode == 1:
            self.world.create_grid(25, 25, 19)  #Norlam size
            self.square_size = 19
        elif self.game_mode == 2:
            self.world.create_grid(49, 49, 10)  #Big size
            self.square_size = 10
        elif self.game_mode == 3:               #Custom
            error_text = '''Attention!!! The size of the map was entered incorrectly. The width and height (x, y) must be integers and greater than one.'''
            try:
                x = int(self.xl.text())
                y = int(self.yl.text())
                if x <= 1 or y <= 1: 
                    self.whriteText(error_text, darkRed)
                    return
                if x > y:
                    self.square_size = int(500/x)
                    self.world.create_grid(x, y, self.square_size)
                else:
                    self.square_size = int(500/y)
                    self.world.create_grid(x, y, self.square_size)
            except ValueError:
                self.whriteText(error_text, darkRed)
                return
        else: 
            self.world.create_grid(9, 9, 50)    #Small
            self.square_size = 50
        
        if str(self.nameEdit.text()) == "":
            self.whriteText("Write the name", darkRed)
            return
        else: self.world.set_player(str(self.nameEdit.text()))
        
        self.name_l.deleteLater()
        self.nameEdit.deleteLater()
        self.worldSizeGBox.deleteLater()
        self.start_button.deleteLater()
        self.menuBox.deleteLater()
        
        self.isStarted = True
        self.whriteText("Hi {}! Game Started!".format(self.world.get_player().get_name()))
        self.world.get_player().set_location(self.world.get_startPoint())
        
        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.setBackgroundBrush(QtGui.QColor(0, 0, 0))
        self.view.setStyleSheet("border: 0px")
        self.gameBox.addWidget(self.view)
        
        # Creating maze and player
        self.add_labyrinth_world_grid_items()
        self.add_player_graphics_item()
        self.update_player()
    
    def start_menu(self):
        self.new_game_button.setEnabled(False)
        if self.isStarted == False:
            self.menuBox = QtWidgets.QGridLayout()
            self.menuBox.setColumnStretch(0,3)
            self.menuBox.setColumnStretch(1,1)
            self.menuBox.setColumnStretch(2,3)
            self.menuBox.setColumnStretch(3,3)
            self.menuBox.setRowStretch(0,4)
            self.menuBox.setRowStretch(1,1)
            self.menuBox.setRowStretch(2,1)
            self.menuBox.setRowStretch(3,1)
            self.menuBox.setRowStretch(4,1)
            self.menuBox.setRowStretch(5,4)
            
            '''Name'''
            self.name_l = QtWidgets.QLabel("    Name:")
            self.nameEdit = QtWidgets.QLineEdit()
            self.nameEdit.setText(self.world.get_player().get_name())
            self.menuBox.addWidget(self.name_l, 1, 1)
            self.menuBox.addWidget(self.nameEdit, 1, 2)
            
            '''Game mode'''
            self.worldSizeGBox = QtWidgets.QGroupBox("World Size")
            hbox = QtWidgets.QHBoxLayout()
            hbox.addStretch(1)
            cb = QtWidgets.QComboBox()
            cb.addItems(["Small", "Normal", "Big", "Custom"])
            cb.currentIndexChanged.connect(self.changeGameMode)
            hbox.addWidget(cb)
            xt = QtWidgets.QLabel("X:")
            self.xl = QtWidgets.QLineEdit()
            hbox.addWidget(xt)
            hbox.addWidget(self.xl)
            self.xl.setEnabled(False)
            yt = QtWidgets.QLabel("Y:")
            self.yl = QtWidgets.QLineEdit()
            hbox.addWidget(yt)
            hbox.addWidget(self.yl)
            self.yl.setEnabled(False)
            
            cb.setCurrentIndex(self.game_mode)
            self.worldSizeGBox.setLayout(hbox)
            self.menuBox.addWidget(self.worldSizeGBox, 2, 1, 1, 2)
            
            '''Start point'''
            self.startPointGBox = QtWidgets.QGroupBox("Starting point")
            self.menuBox.addWidget(self.startPointGBox, 3, 1)
            
            '''Start button'''
            self.start_button = QtWidgets.QPushButton("Start")
            self.start_button.clicked.connect(self.start_game)
            self.menuBox.addWidget(self.start_button, 4, 1, 1, 2)
            self.gameBox.addLayout(self.menuBox)
    
    def end_game(self):
        if self.isStarted: self.whriteText("Game Ended!")
        self.isStarted = False
        
    def new_game(self):
        self.end_game()
        self.view.deleteLater()
        self.world.deleteWorld()
        
        self.flag = 0
        self.isStarted = False
        self.isMazeSolvided = False
        
        self.time = QtCore.QTime(0, 0, 0)
        
        self.start_menu()
        
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
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.start_solving_maze)
            
        if self.isMazeSolvided == True and self.flag == 1 and self.isStarted == False:
            self.flag = self.world.solving_a_maze()
            if self.flag == 0:
                self.show_solving_way()
                self.timer.timeout.disconnect()
                self.timer.timeout.connect(self.update_player)
            self.playerItem.update()
          
    def checkPosition(self):
        player = self.world.get_player().get_location()
        end = self.world.get_endPoint()
        if (player.get_x() == end.get_x()) and (player.get_y() == end.get_y()):
            self.end_game()
        self.playerItem.update()
    
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
        if self.isStarted:
            if self.flag == 0:
                self.flag = self.world.create_maze_randomly()
                if self.flag == 1:
                    self.add_end_point()
            if self.flag == 1:
                self.timerEvent()
                self.new_game_button.setEnabled(True)
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
        nameEdit = QtWidgets.QLineEdit()
        self.box.addWidget(nameEdit)
        
        self.timeBox()
        self.console()
        self.score()
    
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
                  
    def console(self):
        ''' Console '''
        self.textLine = 0
        self.textBox = QtWidgets.QTextBrowser()
        self.textBox.setFont(QtGui.QFont("Carlito"))                                        # Set text style
        self.textBox.setStyleSheet("QTextEdit {background-color:rgba(100, 100, 100, 250)}") # Set background color
        self.whriteText("Welcome!")
        
        self.box.addWidget(self.textBox, 9)
        
    def whriteText(self, string, color = QtCore.Qt.white):
        self.textBox.setTextColor(color)                                # Set text color 
        self.textLine += 1
        line = str(self.textLine) + ": " + string
        self.textBox.append(line)
        
    def gameMode(self):        
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(["Easy", "Normal", "Hard"])
        self.cb.currentIndexChanged.connect(self.changeGameMode)
        
        self.box.addWidget(self.cb)
    
    def changeGameMode(self, i):
        self.game_mode = i
        if i == 3:
            self.xl.setEnabled(True)
            self.yl.setEnabled(True)
        else:
            self.xl.setEnabled(False)
            self.yl.setEnabled(False)

    def init_buttons(self):
        give_up_button = QtWidgets.QPushButton("Give Up")
        give_up_button.clicked.connect(self.start_solving_maze)
        self.new_game_button = QtWidgets.QPushButton("New Game")
        self.new_game_button.clicked.connect(self.new_game)
        
        
        self.box.addWidget(give_up_button)
        self.box.addWidget(self.new_game_button)
        
