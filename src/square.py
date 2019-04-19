from PyQt5 import QtWidgets, QtCore, QtGui

class Square(QtWidgets.QGraphicsRectItem):
    
    def __init__(self, x, y, square_size, right_wall=True, bottom_wall=True):
        super(Square, self).__init__()
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        
        self.x = x
        self.y = y
        self.square_size = square_size
        
        self.wt = 0.85                                      #Wall thickness
        self.alfa = (self.x + self.wt) * self.square_size   #Constant
        self.betta = (self.y + self.wt) * self.square_size  #Constant
        
        self.setBrush(QtGui.QColor(200, 230, 200))
        self.setRect(self.x*self.square_size, self.y*self.square_size, self.square_size, self.square_size)
        self.setPen(QtGui.QPen(-1))
        self.wallItem = QtWidgets.QGraphicsPolygonItem(self)
        self.wallItem.setTransformOriginPoint(self.x * self.square_size, self.y * self.square_size)
        self.wallItem.setBrush(QtGui.QColor(0, 0, 0))
        self.create_column()
        
        self.update()
    
    def create_column(self):
        c = (1 - self.wt) * self.square_size
        columnItem = QtWidgets.QGraphicsRectItem(self.alfa, self.betta, c, c, self)
        columnItem.setBrush(QtGui.QColor(0, 0, 0))
        

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
        if self.right_wall:                                         # Right wall
            a = (self.x + 1) * self.square_size                     # x: Up-right and Bottom-right corner
            b = self.y * self.square_size                           # y: Up-left and Up-right coner
            square.append(QtCore.QPointF(self.alfa, self.betta))    #Bottom-left coner
            square.append(QtCore.QPointF(a, self.betta))            #Bottom-right corner
            square.append(QtCore.QPointF(a, b))                     #Up-right coner
            square.append(QtCore.QPointF(self.alfa, b))             #Up-left corner
            square.append(QtCore.QPointF(self.alfa, self.betta))    #Bottom-left coner
            
        if self.bottom_wall:                                    # Bottom wall
            a = (self.y + 1) * self.square_size                     # y: Bottom-left and Bottom-right coner
            b = self.x * self.square_size                           # x: Up-left and Bottom-left corner
            square.append(QtCore.QPointF(self.alfa, self.betta))    #Up-right coner
            square.append(QtCore.QPointF(self.alfa, a))             #Bottom-right coner
            square.append(QtCore.QPointF(b, a))                     #Bottom-left coner
            square.append(QtCore.QPointF(b, self.betta))            #Up-left corner
            square.append(QtCore.QPointF(self.alfa, self.betta))    #Up-right coner
            
        self.wallItem.setPolygon(square)