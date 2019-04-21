from PyQt5 import QtWidgets, QtCore

class StartMenu():
    def __init__(self):
        self.game_mode = 0
        self.game_start_point = 0
        self.tail_flag = False
        self.show_flag = True
        self.openM_flag = False
        self.x = ""
        self.y = ""
        self.create_menu()
    
    def create_menu(self):
        self.menuBox = QtWidgets.QGridLayout()
        self.menuBox.setColumnStretch(0,3)
        self.menuBox.setColumnStretch(1,1)
        self.menuBox.setColumnStretch(2,1)
        self.menuBox.setColumnStretch(3,2)
        self.menuBox.setColumnStretch(4,3)
        self.menuBox.setRowStretch(0,4)
        self.menuBox.setRowStretch(1,1)
        self.menuBox.setRowStretch(2,1)
        self.menuBox.setRowStretch(3,1)
        self.menuBox.setRowStretch(4,1)
        self.menuBox.setRowStretch(5,4)
        
        self.name()
        self.gameSize()
        self.startPoint()
        self.tools()
        self.saveMazeTools()
    
    def name(self):
        self.name_l = QtWidgets.QLabel("    Name:")
        self.nameEdit = QtWidgets.QLineEdit()
        self.menuBox.addWidget(self.name_l, 1, 1)
        self.menuBox.addWidget(self.nameEdit, 1, 2, 1, 2)
    
    def set_name(self, name):
        self.nameEdit.setText(name)    
    
    def get_name(self):
        return str(self.nameEdit.text())
    
    def gameSize(self):
        self.worldSizeGBox = QtWidgets.QGroupBox("World Size")
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        cb = QtWidgets.QComboBox()
        cb.addItems(["Small", "Normal", "Big", "Custom"])
        cb.setCurrentIndex(self.game_mode)
        cb.currentIndexChanged.connect(self.changeGameSize)
        hbox.addWidget(cb)
        xt = QtWidgets.QLabel("X:")
        self.xl = QtWidgets.QLineEdit()
        self.xl.setText(str(self.x))
        hbox.addWidget(xt)
        hbox.addWidget(self.xl)
        if self.game_mode != 3: self.xl.setEnabled(False)
        yt = QtWidgets.QLabel("Y:")
        self.yl = QtWidgets.QLineEdit()
        self.yl.setText(str(self.y))
        hbox.addWidget(yt)
        hbox.addWidget(self.yl)
        if self.game_mode != 3: self.yl.setEnabled(False)
        
        self.worldSizeGBox.setLayout(hbox)
        self.menuBox.addWidget(self.worldSizeGBox, 2, 1, 1, 3)
    
    def changeGameSize(self, i):
        self.game_mode = i
        if i == 3:
            self.xl.setEnabled(True)
            self.yl.setEnabled(True)
        else:
            self.xl.setEnabled(False)
            self.yl.setEnabled(False)
            
    def get_gameSize(self):
        if self.game_mode == 0: return (9, 9, 50)       #Small
        elif self.game_mode == 1: return (25, 25, 19)   #Norlam size
        elif self.game_mode == 2: return (49, 49, 10)   #Big size
        elif self.game_mode == 3:                       #Custom
            try:
                self.x = int(self.xl.text())
                self.y = int(self.yl.text())
                if self.x <= 1 or self.y <= 1: return None
                if self.x > self.y: return (self.x, self.y, int(500/self.x))
                else: return (self.x, self.y, int(500/self.y))
            except ValueError: return None
    
    def startPoint(self):
        self.startPointGBox = QtWidgets.QGroupBox("Starting point")
        vbox = QtWidgets.QVBoxLayout()
        cb = QtWidgets.QComboBox()
        cb.addItems(["Left_Up","Right_Up","Left_Bottom","Right_Bottom", "Middle"])
        cb.setCurrentIndex(self.game_start_point)
        cb.currentIndexChanged.connect(self.changeGameStartPoint)
        vbox.addWidget(cb)
        self.startPointGBox.setLayout(vbox)
        self.menuBox.addWidget(self.startPointGBox, 3, 1, 1, 2)
        
    def changeGameStartPoint(self, i):
        self.game_start_point = i
        
    def get_startPoint(self):
        return self.game_start_point
    
    def tools(self):
        self.toolGBox = QtWidgets.QGroupBox("Show")
        grid = QtWidgets.QGridLayout()
        tail = QtWidgets.QCheckBox("Tail")
        tail.setChecked(self.tail_flag)
        tail.stateChanged.connect(self.changeTailStatus)
        show = QtWidgets.QCheckBox("Generation")
        show.setChecked(self.show_flag)
        show.stateChanged.connect(self.changeShowStatus)
        
        grid.addWidget(show, 0, 0)
        grid.addWidget(tail, 1, 0)
        
        self.toolGBox.setLayout(grid)
        self.menuBox.addWidget(self.toolGBox, 3, 3)
    
    def get_tail_flag(self): return self.tail_flag
    def get_show_flag(self): return self.show_flag
        
    def changeTailStatus(self, state):
        if state == QtCore.Qt.Checked: self.tail_flag = True
        else: self.tail_flag = False
    
    def changeShowStatus(self, state):
        if state == QtCore.Qt.Checked: self.show_flag = True
        else: self.show_flag = False
    
    def saveMazeTools(self):
        self.openCheckBox = QtWidgets.QCheckBox("Open saved maze!")
        self.openCheckBox.stateChanged.connect(self.changeOpenCBStatus)
        self.openButton = QtWidgets.QPushButton("Open")
        self.openButton.setEnabled(self.openM_flag)
        
        self.menuBox.addWidget(self.openCheckBox, 4, 1, 1, 2)
        self.menuBox.addWidget(self.openButton, 4, 3)
    
    def changeOpenCBStatus(self, state):
        if state == QtCore.Qt.Checked: self.openM_flag = True
        else: self.openM_flag = False
        self.name_l.setEnabled(not self.openM_flag)
        self.nameEdit.setEnabled(not self.openM_flag)
        self.worldSizeGBox.setEnabled(not self.openM_flag)
        self.startPointGBox.setEnabled(not self.openM_flag)
        self.toolGBox.setEnabled(not self.openM_flag)
        self.openButton.setEnabled(self.openM_flag)
    
    def get_openM_flag(self): return self.openM_flag
        
    def get_menuLayout(self):
        return self.menuBox
    
    def delete(self):
        self.name_l.deleteLater()
        self.nameEdit.deleteLater()
        self.worldSizeGBox.deleteLater()
        self.startPointGBox.deleteLater()
        self.toolGBox.deleteLater()
        self.openCheckBox.deleteLater()
        self.openButton.deleteLater()
        self.menuBox.deleteLater()
















        