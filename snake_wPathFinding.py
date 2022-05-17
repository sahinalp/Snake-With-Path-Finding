import numpy as np
import random
import time

from PyQt5.QtWidgets import*
from PyQt5.QtCore import pyqtSlot,QObject
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore,QtTest
from PyQt5.QtGui import QImage, QKeySequence,QPixmap,QPainter

from PyQt5.Qt import Qt

#%% Ui

class loadui(QMainWindow):  
    
    def __init__(self):
        super().__init__()
        loadUi("snake.ui",self)
        self.setWindowTitle("Snake")
        self.k=10
        self.l=20
        self.length=3
        self.snakeLengthx=[self.k,self.k+1,self.k+2]
        self.snakeLengthy=[self.l,self.l,self.l]
        self.foodGenerator()
        self.BoardUpdate()

    def TheSnakeUpdate(self):
        self.thesnake=[]
        for i in range(self.length):
            self.thesnake.append([self.snakeLengthx[i],self.snakeLengthy[i]])
    def BoardUpdate(self):
        self.board=[]
        self.board=np.zeros((43,31),dtype=np.int16)
        self.TheSnakeUpdate()
        for i in range(43):
            for j in range(31):
                if [i,j] in self.thesnake:
                    if i==self.snakeLengthx[0] and j==self.snakeLengthy[0]:
                        #head of the snake
                        self.board[i][j]=2
                    else:
                        #body of the snake
                        self.board[i][j]=1
                elif i==self.x and j==self.y:
                    #food
                    self.board[i][j]=3
    def foodGenerator(self):
        self.TheSnakeUpdate()
        while True:
            self.x=random.randint(0, 42)
            self.y=random.randint(0, 30)
            if [self.x,self.y] not in self.thesnake:
                break
    def snake(self):
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView_backGround.setScene(scene)
        
        side = 20
        self.thesnake=[]
        if -1 in self.snakeLengthx:
            for i in range(len(self.snakeLengthx)):
                if self.snakeLengthx[i]==-1:
                    self.snakeLengthx[i]=42
        if 43 in self.snakeLengthx:
            for i in range(len(self.snakeLengthx)):
                if self.snakeLengthx[i]==43:
                    self.snakeLengthx[i]=0
        if -1 in self.snakeLengthy:
            for i in range(len(self.snakeLengthy)):
                if self.snakeLengthy[i]==-1:
                    self.snakeLengthy[i]=30
        if 31 in self.snakeLengthy:
            for i in range(len(self.snakeLengthy)):
                if self.snakeLengthy[i]==31:
                    self.snakeLengthy[i]=0
        self.TheSnakeUpdate()
        
        if [self.snakeLengthx[0],self.snakeLengthy[0]] in self.thesnake[1:len(self.thesnake)-1] and [self.snakeLengthx[0],self.snakeLengthy[0]] in self.thesnake[2]:
            txt="Score "+str(int(self.Score.value()))+"     "
            QMessageBox.warning(self, "Game Over", txt)
            self.k=10
            self.l=20
            self.length=3
            self.Score.display(0)
            self.snakeLengthx=[self.k+2,self.k+1,self.k]
            self.snakeLengthy=[self.l,self.l,self.l]
            self.snake()
        
        if self.thesnake[0]==[self.x,self.y]:
            val=1+self.Score.value()
            self.Score.display(val)
            self.length+=1
            self.snakeLengthx.append(self.snakeLengthx[-1])
            self.snakeLengthy.append(self.snakeLengthy[-1])

            self.foodGenerator()
            self.TheSnakeUpdate()

        for i in range(43):
            for j in range(31):

                if [i,j] in self.thesnake:
                    rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(i*20, j*20, 20, 20))
                    
                    rect_item.setBrush(QtCore.Qt.green)
                    scene.addItem(rect_item) 
                elif [i,j]==[self.x,self.y]:
                    rect_item = QtWidgets.QGraphicsRectItem(QtCore.QRectF(i*20, j*20, 20, 20))
                    
                    rect_item.setBrush(QtCore.Qt.red)
                    scene.addItem(rect_item) 
                else:
                    pen = QtGui.QPen(QtCore.Qt.black)
                    r = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                    scene.addRect(r, pen)        
    def keyPressEvent(self, event):
        self.Movement()            
    def updateLength(self,d):
        old_snakeLengthx=[]
        old_snakeLengthy=[]
        for i in range(self.length):
            old_snakeLengthx.append(self.snakeLengthx[i])
            old_snakeLengthy.append(self.snakeLengthy[i])
        
        self.snakeLengthx=[]
        self.snakeLengthy=[]
        if d=="d":
            self.snakeLengthx.append(old_snakeLengthx[0]+1)
            self.snakeLengthy.append(old_snakeLengthy[0])
            for i in range(self.length-1):
                self.snakeLengthx.append(old_snakeLengthx[i])
                self.snakeLengthy.append(old_snakeLengthy[i])
        elif d=="a":
            self.snakeLengthx.append(old_snakeLengthx[0]-1)
            self.snakeLengthy.append(old_snakeLengthy[0])
            for i in range(self.length-1):
                self.snakeLengthx.append(old_snakeLengthx[i])
                self.snakeLengthy.append(old_snakeLengthy[i])
        elif d=="s":
            self.snakeLengthx.append(old_snakeLengthx[0])
            self.snakeLengthy.append(old_snakeLengthy[0]+1)
            for i in range(self.length-1):
                self.snakeLengthx.append(old_snakeLengthx[i])
                self.snakeLengthy.append(old_snakeLengthy[i])
        elif d=="w":
            self.snakeLengthx.append(old_snakeLengthx[0])
            self.snakeLengthy.append(old_snakeLengthy[0]-1)
            
            for i in range(self.length-1):
                self.snakeLengthx.append(old_snakeLengthx[i])
                self.snakeLengthy.append(old_snakeLengthy[i])
        self.BoardUpdate()        
    def Movement(self):
        global roadList
        global directions
        global directionx
        global directiony
        while True:
            #Path Finding Algorithm
            self.endfinded=False
            start=[self.snakeLengthx[0],self.snakeLengthy[0]]
            end=[self.x,self.y]
            visited=[]
            roads=[]
            visited.append(start)
            roads.append(start)
            
            def neighbour(start,visited,end):
                road=[]  
                if abs(self.snakeLengthy[0]-self.y)>abs(self.snakeLengthx[0]-self.x):
                    directions=["a","d","w","s"]
                    directionx=[-1,1,0,0]
                    directiony=[0,0,-1,1]
                else:
                    directions=["w","s","a","d"]
                    directionx=[0,0,-1,1]
                    directiony=[-1,1,0,0]                          
                for i in range(4):
                    x=start[0]+directionx[i]
                    y=start[1]+directiony[i]
                    
                    if x==end[0] and y==end[1]:
                        self.endfinded=True
                        road.append([directionx[i],directiony[i]])
                        visited.append([x,y])
                        roadList.append(directions[i])
                        break
                    if x<0 or x>42 or y<0 or y>30:
                        continue
                    if [x,y] in visited:
                        continue
                    if self.board[x,y]==1:
                        continue
                    road.append([directionx[i],directiony[i]])
                    visited.append([x,y])
                    roadList.append(directions[i])
                return road
            path=[]
            thepath=[]
            k=""
            while True:
                roadList=[]
                if roads==[]:
                    path.append(k)
                    thepath.append(path[-1])
                    self.endfinded=False
                    break
                if self.endfinded:
                    thepath.append(path[-1])
                    self.endfinded=False
                if path!=[]:
                    k=path.pop(0)
                x=roads.pop(0)
                for a,b in neighbour(x, visited, end):
                    roads.append([x[0]+a,x[1]+b])
                for i in roadList:
                    path.append(k+i)            
            
            path=[]
            path.append(thepath[0])
            for i in range(len(thepath)):
                if i==0:
                    continue
                if len(thepath[i])>len(path[0]) and self.length>50 and i!=len(thepath)-1 and len(path[0])>3:
                    path=[]
                    path.append(thepath[i])
                elif len(thepath[i])<len(path[0]) and self.length<50:
                    path=[]
                    path.append(thepath[i])

            for i in range(1+round((len(path[-1]))/self.length)):
                self.updateLength(path[-1][i])
                self.snake()
                self.speed=self.horizontalSlider_speed.value()
                QtTest.QTest.qWait(self.speed-100)
                    

app = QApplication([])
window = loadui()
window.show()
app.exec_()