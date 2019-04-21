from PyQt5 import QtWidgets, QtGui, QtCore

class PlayerGraphicsItem(QtWidgets.QGraphicsRectItem):
    
    def __init__(self, player, square_size):
        # Call init of the parent object
        super(PlayerGraphicsItem, self).__init__()
        self.player = player
        self.square_size = square_size
        
        # Set player color red
        self.setBrush(QtGui.QColor(200,0,0))
        self.update()
    
    def update(self):
        #Update the coordinates of this item to match the attached player.
        x = self.player.get_location().get_x()
        y = self.player.get_location().get_y()
        playerItem = QtCore.QRectF(x * self.square_size, y * self.square_size, self.square_size*0.85, self.square_size*0.85)
        self.setRect(playerItem)