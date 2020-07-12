#!/usr/bin/python3.5

import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import numpy as np
from math import pi

# ------------------------------------------------------- #
# ---------------- Class Computing_Modes ---------------- #
# ------------------------------------------------------- #  
class Computing_Modes(qtw.QWidget):
    def __init__(self, pulsatingsDict):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'Vibrations modes'
        self.width = 800
        self.height =800
        self.pulsatingsDict = pulsatingsDict
        if self.pulsatingsDict != {}:
            self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.maxIndexW = len(self.pulsatingsDict['mode1'])
        self.indexW = 1

        l = qtw.QGridLayout(self)

        # Create canvas to plot the values
        self.figure = plt.figure(figsize=(15,5))    
        self.canvas = FigureCanvas(self.figure)   
        l.addWidget(self.canvas, 2,0,8,92)

        # Create the slider to select pulsating
        self.slider = qtw.QSlider(qtc.Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(self.maxIndexW)
        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.updateIndexW)
        l.addWidget(self.slider, 0,1,1,90)

        # Create the labels for the min and max pulsating index
        minValueLabel = qtw.QLabel('Min w = 1', self)
        maxValueLabel = qtw.QLabel('Max w = {}'.format(self.maxIndexW), self)
        l.addWidget(minValueLabel, 0,0,1,1)  
        l.addWidget(maxValueLabel, 0,91,1,1)  

        # Create the buttons to go to the previous and the next pulsating
        buttonDecrease = qtw.QPushButton('Previous w', self)
        buttonDecrease.clicked.connect(self.decrease)
        buttonIncrease = qtw.QPushButton('Next w', self)
        buttonIncrease.clicked.connect(self.increase)
        l.addWidget(buttonDecrease, 1,43,1,1)  
        l.addWidget(buttonIncrease, 1,44,1,1)  

        # Create the labels to display the value of the curent pulsating
        curentPulsatingLabel = qtw.QLabel('Curent w :', self)
        self.pulsatingLabel = qtw.QLabel('w1 = {:.5E} rad/s; '.format(self.pulsatingsDict['w1']), self)
        self.frequencyLabel = qtw.QLabel('f1 = {:.5E} Hz'.format(self.pulsatingsDict['w1']/(2*pi)), self)
        l.addWidget(curentPulsatingLabel, 1,45,1,1)  
        l.addWidget(self.pulsatingLabel, 1,47,1,1)  
        l.addWidget(self.frequencyLabel, 1,48,1,1) 

        # Create the Line edit to enter the wanted pulsating
        self.curentPulsatin = qtw.QLineEdit('1', self)
        self.curentPulsatin.returnPressed.connect(self.readLineEdit)
        l.addWidget(self.curentPulsatin, 1,46,1,1)  
        
        self.compute_initial_figure()
        self.show()


    def updateIndexW(self, value):
        self.indexW = value
        self.plot()
        self.pulsatingLabel.setText('w{} = {:.5E} rad/s; '.format(self.indexW, self.pulsatingsDict['w{}'.format(self.indexW)]))
        self.frequencyLabel.setText('f{} = {:.5E} Hz'.format(self.indexW, self.pulsatingsDict['w{}'.format(self.indexW)]/(2*pi)))
        self.curentPulsatin.setText(str(self.indexW))

    
    def decrease(self):
        if self.indexW > 1:
            self.indexW -= 1
            self.slider.setValue(self.indexW)

    
    def increase(self):
        if self.indexW < self.maxIndexW:
            self.indexW += 1
            self.slider.setValue(self.indexW)

    def readLineEdit(self):
        value = int(self.curentPulsatin.text())
        if value >= 1 and value <= self.maxIndexW:
            self.indexW = value
            self.slider.setValue(self.indexW)


    def compute_initial_figure(self):
        axes = self.figure.add_subplot(111)
        t = self.pulsatingsDict['mode1']
        self.s = np.array([i for i in range(1, self.maxIndexW+1)])
        axes.set_ylabel('Amplitude')
        axes.set_xlabel('Degrees of freedom')
        axes.plot(self.s, t)
        self.canvas.draw()
        #axes.set_ylim(top=self.ylim_top.text(),bottom=self.ylim_bottom.text()) 


    def plot(self):
        plt.cla()
        axes=self.figure.add_subplot(111)
        axes.set_ylabel('Amplitude')
        axes.set_xlabel('Degrees of freedom')
        t = self.pulsatingsDict['mode{}'.format(self.indexW)]
        axes.plot(self.s, t)
        # axes.set_ylim(top=self.ylim_top.text(),bottom=self.ylim_bottom.text()) 
        self.canvas.draw()



# ----------------------------------------------------------- #
# ---------------- Class Computing_Responces ---------------- #
# ----------------------------------------------------------- #  
class Computing_Responces(qtw.QWidget):
    def __init__(self, responcesDict, massList):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'Vibrations responces'
        self.width = 800
        self.height = 800
        self.responcesDict = responcesDict
        self.massList = massList
        if self.responcesDict != {}:
            self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.maxIndexM = len(self.massList)-1
        self.indexM = 1

        l = qtw.QGridLayout(self)

        # Create canvas to plot the values
        self.figure = plt.figure(figsize=(15,5))    
        self.canvas = FigureCanvas(self.figure)   
        l.addWidget(self.canvas, 2,0,8,92)

        # Create the slider to select pulsating
        self.slider = qtw.QSlider(qtc.Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(self.maxIndexM)
        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.updateindexM)
        l.addWidget(self.slider, 0,1,1,90)

        # Create the labels for the min and max pulsating index
        minValueLabel = qtw.QLabel('Min index = 1', self)
        maxValueLabel = qtw.QLabel('Max index = {}'.format(self.maxIndexM), self)
        l.addWidget(minValueLabel, 0,0,1,1)  
        l.addWidget(maxValueLabel, 0,91,1,1)  

        # Create the buttons to go to the previous and the next pulsating
        buttonDecrease = qtw.QPushButton('Previous mass', self)
        buttonDecrease.clicked.connect(self.decrease)
        buttonIncrease = qtw.QPushButton('Next mass', self)
        buttonIncrease.clicked.connect(self.increase)
        l.addWidget(buttonDecrease, 1,43,1,1)  
        l.addWidget(buttonIncrease, 1,44,1,1)  

        # Create the labels to display the value of the curent pulsating
        self.curentPulsatingLabel = qtw.QLabel('Curent mass : {}'.format(self.massList[1].name), self)
        l.addWidget(self.curentPulsatingLabel, 1,45,1,1)  
        

        self.compute_initial_figure()
        self.show()


    def updateindexM(self, value):
        self.indexM = value
        self.plot()
        self.curentPulsatingLabel.setText('Curent mass : {}'.format(self.massList[self.indexM].name))
        
    
    def decrease(self):
        if self.indexM > 1:
            self.indexM -= 1
            self.slider.setValue(self.indexM)

    
    def increase(self):
        if self.indexM < self.maxIndexM:
            self.indexM += 1
            self.slider.setValue(self.indexM)


    def compute_initial_figure(self):
        axes = self.figure.add_subplot(111)
        axes.set_yscale('log')
        axes.set_ylabel('Responce [rad]')
        axes.set_xlabel('Pulsating [rad/s]')
        x = self.responcesDict['w']
        y = self.responcesDict[self.massList[1].name]
        # self.s = np.array([i for i in range(1, self.maxIndexM+1)])
        axes.plot(x, y)
        self.canvas.draw()
        #axes.set_ylim(top=self.ylim_top.text(),bottom=self.ylim_bottom.text()) 


    def plot(self):
        self.figure.clf()
        axes = self.figure.add_subplot(111)
        axes.set_yscale('log')
        axes.set_ylabel('Responce [rad]')
        axes.set_xlabel('Pulsating [rad/s]')
        x = self.responcesDict['w']
        y = self.responcesDict[self.massList[self.indexM].name]
        axes.plot(x, y)
        # axes.set_ylim(top=self.ylim_top.text(),bottom=self.ylim_bottom.text()) 
        self.canvas.draw()



# --------------------------------------------------- #
# ---------------- Class Plot_Matrix ---------------- #
# --------------------------------------------------- #  
class Plot_Matrix(qtw.QTabWidget):
    def __init__(self, matrix2plot, listDict, listMatrix, width, height):
        super().__init__()
        self.title = 'Plot Matrix'
        self.left, self.top = 0, 0
        self.width, self.height = width, height
        self.listMatrix = listMatrix
        self.massListName = []
        for i in range(1, len(listDict['Mass_list'])):
            self.massListName.append(listDict['Mass_list'][i].name)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        if matrix2plot == 'All' or matrix2plot == 'Mass':
            self.plot_mass()
        if matrix2plot == 'All' or matrix2plot == 'Stiffness':
            self.plot_stiffness()
        if matrix2plot == 'All' or matrix2plot == 'Damping':
            self.plot_damping()
        if matrix2plot == 'All' or matrix2plot == 'Loading':
            self.plot_loading()

        self.show()


    def plot_mass(self):
        massMatrix = self.listMatrix[0]
        if massMatrix != []:
            dim = len(massMatrix.matrix[0])
            # Create table
            self.tabMassMatrix = qtw.QTableWidget()
            # Add the table to the tabs
            self.addTab(self.tabMassMatrix,'Mass Matrix')
            # Set the number of rows and columns
            self.tabMassMatrix.setRowCount(dim)
            self.tabMassMatrix.setColumnCount(dim)
            # Set the columns headers
            self.tabMassMatrix.setHorizontalHeaderLabels(self.massListName)
            self.tabMassMatrix.setVerticalHeaderLabels(self.massListName)
            # Set columns policy
            self.tabMassMatrix.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            
            for i in range(0, dim):
                for j in range(0, dim):
                    item = qtw.QTableWidgetItem(str(massMatrix.matrix[i][j]))
                    item.setTextAlignment(qtc.Qt.AlignCenter)
                    self.tabMassMatrix.setItem(i,j,item)


    def plot_stiffness(self):
        stiffnessMatrix = self.listMatrix[1]
        if stiffnessMatrix != []:
            dim = len(stiffnessMatrix.matrix[0])
            # Create table
            self.tabStiffnessMatrix = qtw.QTableWidget()
            # Add the table to the tabs
            self.addTab(self.tabStiffnessMatrix,'Stiffness Matrix')
            # Set the number of rows and columns
            self.tabStiffnessMatrix.setRowCount(dim)
            self.tabStiffnessMatrix.setColumnCount(dim)
            # Set the columns headers
            self.tabStiffnessMatrix.setHorizontalHeaderLabels(self.massListName)
            self.tabStiffnessMatrix.setVerticalHeaderLabels(self.massListName)
            # Set columns policy
            self.tabStiffnessMatrix.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            
            for i in range(0, dim):
                for j in range(0, dim):
                    item = qtw.QTableWidgetItem(str(stiffnessMatrix.matrix[i][j]))
                    item.setTextAlignment(qtc.Qt.AlignCenter)
                    self.tabStiffnessMatrix.setItem(i,j,item)


    def plot_damping(self):
        damingMatrix = self.listMatrix[2]
        if damingMatrix != []:
            dim = len(damingMatrix.matrix[0])
            # Create table
            self.tabDampingMatrix = qtw.QTableWidget()
            # Add the table to the tabs
            self.addTab(self.tabDampingMatrix,'Damping Matrix')
            # Set the number of rows and columns
            self.tabDampingMatrix.setRowCount(dim)
            self.tabDampingMatrix.setColumnCount(dim)
            # Set the columns headers
            self.tabDampingMatrix.setHorizontalHeaderLabels(self.massListName)
            self.tabDampingMatrix.setVerticalHeaderLabels(self.massListName)
            # Set columns policy
            self.tabDampingMatrix.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            
            for i in range(0, dim):
                for j in range(0, dim):
                    item = qtw.QTableWidgetItem(str(damingMatrix.matrix[i][j]))
                    item.setTextAlignment(qtc.Qt.AlignCenter)
                    self.tabDampingMatrix.setItem(i,j,item)


    def plot_loading(self):
        loadingMatrix = self.listMatrix[3]
        if loadingMatrix != []:
            dim = len(loadingMatrix.matrix)
            # Create table
            self.tabLoadingMatrix = qtw.QTableWidget()
            # Add the table to the tabs
            self.addTab(self.tabLoadingMatrix,'Loading Matrix')
            # Set the number of rows and columns
            self.tabLoadingMatrix.setRowCount(dim)
            self.tabLoadingMatrix.setColumnCount(1)
            # Set the columns headers
            self.tabLoadingMatrix.setHorizontalHeaderLabels(self.massListName)
            self.tabLoadingMatrix.setVerticalHeaderLabels(self.massListName)
            # Set columns policy
            self.tabLoadingMatrix.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            
            for i in range(0, dim):
                item = qtw.QTableWidgetItem(str(loadingMatrix.matrix[i]))
                item.setTextAlignment(qtc.Qt.AlignCenter)
                self.tabLoadingMatrix.setItem(i-1,1,item)
