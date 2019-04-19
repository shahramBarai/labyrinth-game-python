from PyQt5 import QtWidgets, QtCore, QtGui

class Square(QtWidgets.QGraphicsRectItem):
    
    def __init__(self, x, y, square_size, right_wall=True, bottom_wall=True):
        super(Square, self).__init__()
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        
        self.x = x
        self.y = y
        self.square_size = square_size
        self.setBrush(QtGui.QColor(200, 230, 200))
        self.setRect(self.x*self.square_size, self.y*self.square_size, self.square_size, self.square_size)
        self.setPen(QtGui.QPen(-1))
        self.squareItem = QtWidgets.QGraphicsPolygonItem(self)
        self.squareItem.setTransformOriginPoint(self.x * self.square_size, self.y * self.square_size)

        self.update()
    
    def is_right_wall(self):
        return self.right_wall
    
    def is_bottom_wall(self):
        return self.bottom_wall
    
    def delete_right_wall(self):
        self.right_wall = False
    def delete_bottom_wall(self):
        self.bottom_wall = False
    
    def setColor(self, a, b, c):
        self.setBrush(QtGui.QColor(a, b, c))
    
    def update(self):
        square = QtGui.QPolygonF()
        if self.right_wall == True:                                   # Right wall
            a = self.x * self.square_size + self.square_size*0.85    # x: Up-left and Bottom-left corner
            b = (self.x + 1) * self.square_size                     # x: Up-right and Bottom-right corner
            c = self.y * self.square_size                           # y: Up-left and Up-right coner
            d = (self.y + 1) * self.square_size                     # y: Bottom-left and Bottom-right coner
            square.append(QtCore.QPointF(b, d))
            square.append(QtCore.QPointF(b, c))
            square.append(QtCore.QPointF(a, c))
            square.append(QtCore.QPointF(a, d))
        if self.bottom_wall == True:                                   # Bottom wall
            a = (self.x + 1) * self.square_size                     # x: Up-right and Bottom-right corner
            b = self.x * self.square_size                           # x: Up-left and Bottom-left corner
            c = self.y * self.square_size + self.square_size*0.85    # y: Up-left and Up-right coner
            d = (self.y + 1) * self.square_size                     # y: Bottom-left and Bottom-right coner
            square.append(QtCore.QPointF(a, c))
            square.append(QtCore.QPointF(b, c))
            square.append(QtCore.QPointF(b, d))
            square.append(QtCore.QPointF(a, d))
        
        
        self.squareItem.setBrush(QtGui.QColor(0, 0, 0))
        self.squareItem.setPolygon(square)