#!/usr/bin/python3.5

# ----------------------------------------------------------------
#       Import all the libraries for exactra functions      
# ----------------------------------------------------------------
# General Libraries for operating system parameters
import sys
import os
# General Libraries for Graphical User Interfaces
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

# Custom libraries for Graphical User Interfaces (see files vibrations_tabsTranslational.py, vibrations_tabsRotational.py, vibrations_popupWindows.py)
from vibrations_tabsTranslational import TabsTanslational
from vibrations_tabsRotational import TabsRotational
from vibrations_popupWindows import Popup_Dialog_Single
# Custom librarie for project management (see file vibrations_project.py)
from vibrations_project import Vibration_Project 
# Custom librarie for vibration elements (see file vibrations_elements.py)
from vibrations_elements import Mass, Stiffness, StiffnessDiscretized, Shaft, Damping, Loading



# ----------------------------------------------------------------
#       Object : Main_Window 
# ----------------------------------------------------------------
class Main_Window(qtw.QMainWindow):
    def __init__(self, width, height):
        """
        Method : __init__
        
        Description : 
        
        Parameters :
            - [int] width : Number of pixels in the width of the screen
            - [int] height : Number of pixels in the height of the screen
        
        Returns : None
        """
        super(Main_Window, self).__init__()
        self.title = 'Vibration Project'
        self.recWidth, self.recHeight = width, height
        self.setGeometry((width-460)/2,(height-180)/2,460,180)
        self.fullMenu = False
        self.create_menu()
        # self.tabs = TabsTanslational(width, height)
        # self.setCentralWidget(self.tabs)
        # Show widget


    def create_menu(self):
        menu = self.menuBar()
        self.fileMenu = menu.addMenu('&File')

        newAction = qtw.QAction("New project", self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.new_project)
        self.fileMenu.addAction(newAction)

        openAction = qtw.QAction("Open project", self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openProject)
        self.fileMenu.addAction(openAction)


    def add_save2Menu(self):
        if not self.fullMenu:
            importAction = qtw.QAction("Import elements", self)
            importAction.setShortcut('Ctrl+I')
            importAction.triggered.connect(self.importElements)
            self.fileMenu.addAction(importAction)

            saveAction = qtw.QAction("Save project", self)
            saveAction.setShortcut('Ctrl+S')
            saveAction.triggered.connect(self.saveProject)
            self.fileMenu.addAction(saveAction)

            saveAsAction = qtw.QAction("Save project as", self)
            saveAsAction.setShortcut('Ctrl+Shift+S')
            saveAsAction.triggered.connect(self.saveAsProject)
            self.fileMenu.addAction(saveAsAction)

            self.fullMenu = True


    def new_project(self):
        # print('New Project')
        self.win = Popup_Dialog_Single('New project type', 'Ok', recWidth=self.recWidth, recHeight=self.recHeight)
        self.win.add_comboBox('Problem Type', ['Tanslational', 'Rotational'])
        self.win.exec_()
        problemType = self.win.get_value()
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getSaveFileName(self,"Enter new project name","","All Files (*);;Coma Seperated Virgule Files (*.csv);;Vibration Project Files (*_project.csv)", options=options)
        if fileName:
            if problemType['Problem Type'] == 0:
                self.add_save2Menu()
                self.tabs = TabsTanslational(fileName, self.recWidth, self.recHeight)
                self.setCentralWidget(self.tabs)
            elif problemType['Problem Type'] == 1:
                self.add_save2Menu()
                self.tabs = TabsRotational(fileName, self.recWidth, self.recHeight)
                self.setCentralWidget(self.tabs)
    

    def openProject(self):
        # print('Open Project')
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getOpenFileName(self,"Select project to open", "","Vibration Project Files (*_project.csv)", options=options)
        
        if fileName:
            self.add_save2Menu()
            self.tabs = TabsRotational(fileName, self.recWidth, self.recHeight)
            self.setCentralWidget(self.tabs)
            self.tabs.open()


    def importElements(self):
        # print('Open Project')
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getOpenFileName(self,"Select elements to import", "","Vibration Elements Files (*_elements.csv)", options=options)
        
        if fileName:
            self.tabs.importElements(fileName)


    def saveProject(self):
        self.tabs.save()


    def saveAsProject(self):
        # print('New Project')
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.DontUseNativeDialog
        fileName, _ = qtw.QFileDialog.getSaveFileName(self,"Enter name to save as","","All Files (*);;Coma Seperated Virgule Files (*.csv);;Vibration Project Files (*_project.csv)", options=options)
        
        if fileName:
            self.tabs.saveAs(fileName)

# Slider : http://johnnado.com/pyqt-qtest-example/
# scrollbar
# matplotlib : https://pythonspot.com/pyqt5-matplotlib/