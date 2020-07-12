
import os
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from vibrations_project import Vibration_Project 
from vibrations_elements import Mass, EquivalentMass, Stiffness, StiffnessDiscretized, StiffnessDiscretized_Shaft, Damping, Loading, Shaft

from vibrations_computingWindows import Computing_Modes, Computing_Responces, Plot_Matrix
from vibrations_popupWindows import Popup_Dialog_Single, Popup_Dialog_Multi, Popup_Info

# from math import pi


# -------------------------------------------------- #
# ---------------- ResultsWindows ---------------- #
# -------------------------------------------------- #
class ResultsWindows(qtw.QWidget):
    def __init__(self, width, height):
        super(ResultsWindows, self).__init__()
        self.title = 'Mixer Project'
        self.recWidth, self.recHeight = width, height
        self.width, self.height = 260, 138
        self.left, self.top = int((width - self.width)/2), int((height - self.height)/2)
            
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getOpenFileName(self,"Select elements to import", "","Vibration Project Files (*_elements.csv)", options=options)
        
        if fileName:
            self.projectName = os.path.basename(fileName)
            self.projectFolder = os.path.dirname(fileName)

            self.project = Vibration_Project(self.projectName, self.projectFolder)
            self.project.open_table()
            self.project.solve()
            self.project.solve_dynamicResponce()
            # self.project.save_project()

            self.createTabComputing()
            self.show()

        else:
            buttonClose = qtw.QPushButton('Quit', self)
            buttonClose.clicked.connect(self.close)
            buttonClose.move(90, 50)
            self.show()


    def createTabComputing(self):
        buttonShowMatrix = qtw.QPushButton('Show Matrix', self)
        buttonShowMatrix.clicked.connect(self.showMatrix)
        buttonShowMatrix.move(35, 10)

        buttonShowLitteralMatrix = qtw.QPushButton('Show Litteral Matrix', self)
        buttonShowLitteralMatrix.clicked.connect(self.showLitteralMatrix)
        buttonShowLitteralMatrix.move(10, 48)
                
        self.comboShowMatrix = qtw.QComboBox(self)
        self.comboShowMatrix.addItems(['All', 'Mass', 'Stiffness', 'Damping', 'Loading'])
        self.comboShowMatrix.move(160, 29)
        
        buttonPlotModes = qtw.QPushButton('Plot Modes', self)
        buttonPlotModes.clicked.connect(self.plotModes)
        buttonPlotModes.move(10, 100)
        
        buttonPlotResponces = qtw.QPushButton('Plot Responce', self)
        buttonPlotResponces.clicked.connect(self.plotResponces)
        buttonPlotResponces.move(110, 100)


    def showMatrix(self):
        matrix2plot = self.comboShowMatrix.currentText()
        listDict = self.project.listDict
        listMatrix = self.project.listMatrix
        width, height = self.recWidth, self.recHeight
        self.showMatrixWindow = Plot_Matrix(matrix2plot, listDict, listMatrix, width, height)


    def showLitteralMatrix(self):
        matrix2plot = self.comboShowMatrix.currentText()
        listDict = self.project.listDict
        listMatrix = self.project.listLitteralMatrix
        width, height = self.recWidth, self.recHeight
        self.showMatrixWindow = Plot_Matrix(matrix2plot, listDict, listMatrix, width, height)


    def plotModes(self):
        self.wModes = Computing_Modes(self.project.pulsatingsDict)
        self.wModes.show()


    def plotResponces(self):
        self.wResponces = Computing_Responces(self.project.responcesDict, self.project.listDict['Mass_list'])
        self.wResponces.show()
