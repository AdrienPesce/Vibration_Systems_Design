
import os
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from vibrations_project import Vibration_Project 
from vibrations_elements import Mass, EquivalentMass, Stiffness, StiffnessDiscretized, StiffnessDiscretized_Shaft, Damping, Loading, Shaft

from vibrations_computingWindows import Computing_Modes
from vibrations_popupWindows import Popup_Dialog_Single, Popup_Dialog_Multi, Popup_Dialog_Remove, Popup_Info

from math import pi

from vibrations_tabsTranslational import TabsTanslational


# ------------------------------------------------ #
# ---------------- TabsRotational ---------------- #
# ------------------------------------------------ #
class TabsRotational(TabsTanslational):
    def __init__(self, projectDir, width, height, parent = None):
        super(TabsRotational, self).__init__(projectDir, width, height, parent = None)
        self.shaftList = []


    def createTabs(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create the tabs
        self.createTabShaft()        
        self.createTabMass()
        self.createTabStiffness()
        self.createTabDamping()
        self.createTabLoading()
        self.createTabComputing()


    # ------------------------------------------- #
    # ---------------- Shaft tab ---------------- #
    # ------------------------------------------- #
    def createTabShaft(self):
        # Creat the Shaft widget
        self.tabShaft = qtw.QWidget()
        
        buttonAddShaft = qtw.QPushButton('Add', self.tabShaft)
        buttonAddShaft.clicked.connect(self.add_shaft)
        buttonAddShaft.move(10, 10)

        buttonAddMultiShaft = qtw.QPushButton('Add Multi', self.tabShaft)
        buttonAddMultiShaft.clicked.connect(self.add_shaft)
        buttonAddMultiShaft.move(100, 10)

        buttonEditShaft = qtw.QPushButton('Edit', self.tabShaft)
        buttonEditShaft.clicked.connect(self.edit_shaft)
        buttonEditShaft.move(10, 48)

        self.editShaftCombo = qtw.QComboBox(self.tabShaft)
        self.editShaftCombo.move(100, 48)

        buttonRemoveShaft = qtw.QPushButton('Remove', self.tabShaft)
        buttonRemoveShaft.clicked.connect(self.remove_shaft)
        buttonRemoveShaft.move(10, 86)

        self.removeShaftCombo = qtw.QComboBox(self.tabShaft)
        self.removeShaftCombo.move(100, 86)

        # Add the widget to the tabs
        self.addTab(self.tabShaft, 'Shaft')


    def add_shaft(self):
        self.addShaftWindow = Popup_Dialog_Single('Add Shaft', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
        self.addShaftWindow.add_lineEdit('Name')
        self.addShaftWindow.add_lineEdit('Ratio')
        shaftNameList = []
        for shaft in self.project.listDict['Shaft_list']:
            shaftNameList.append(shaft.name)
        self.addShaftWindow.add_comboBox('Shaft', shaftNameList)
        self.addShaftWindow.exec_()

        valueDict = self.addShaftWindow.get_value()
        if valueDict != 'None':
            newShaft = Shaft(valueDict['Name'], self.get_float(valueDict['Ratio']), self.project.listDict['Shaft_list'][valueDict['Shaft']])
            self.project.add(newShaft)
            self.shaftList.append(newShaft)
            self.editShaftCombo.addItem(newShaft.name)
            self.removeShaftCombo.addItem(newShaft.name)


    def addMulti_shaft(self):
        pass


    def edit_shaft(self):
        pass


    def remove_shaft(self):
        pass



    # ------------------------------------------ #
    # ---------------- Mass tab ---------------- #
    # ------------------------------------------ #
    def createTabMass(self):
        # Creat the Mass widget
        self.tabMass = qtw.QWidget()
 
        buttonAddMass = qtw.QPushButton('Add', self.tabMass)
        buttonAddMass.clicked.connect(self.add_mass)
        buttonAddMass.move(10, 10)
 
        buttonAddMultiMass = qtw.QPushButton('Add Multi', self.tabMass)
        buttonAddMultiMass.clicked.connect(self.addMulti_mass)
        buttonAddMultiMass.move(100, 10)

        self.addMassCombo = qtw.QComboBox(self.tabMass)
        self.addMassCombo.addItems(['Inertia', 'Equivalent Inertia'])
        self.addMassCombo.move(190, 10)
       
        buttonEditMass = qtw.QPushButton('Edit', self.tabMass)
        buttonEditMass.clicked.connect(self.edit_mass)
        buttonEditMass.move(10, 48)

        self.editMassCombo = qtw.QComboBox(self.tabMass)
        self.editMassCombo.move(100, 48)

        buttonRemoveMass = qtw.QPushButton('Remove', self.tabMass)
        buttonRemoveMass.clicked.connect(self.remove_mass)
        buttonRemoveMass.move(10, 86)

        self.removeMassCombo = qtw.QComboBox(self.tabMass)
        self.removeMassCombo.move(100, 86)

        # Add the widget to the tabs
        self.addTab(self.tabMass, 'Inertia')


    def add_mass(self):
        typeMass = self.addMassCombo.currentText()
        if typeMass == 'Inertia':
            self.addMassWindow = Popup_Dialog_Single('Add Inertia', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
            self.addMassWindow.add_lineEdit('Name')
            self.addMassWindow.add_lineEdit('I', valueUnit='kg.m2')
            shaftNameList = []
            for shaft in self.project.listDict['Shaft_list']:
                shaftNameList.append(shaft.name)
            self.addMassWindow.add_comboBox('Shaft', shaftNameList)
            self.addMassWindow.exec_()

            valueDict = self.addMassWindow.get_value()
            if valueDict != 'None':
                newMass = Mass(valueDict['Name'], self.get_float(valueDict['I']), self.project.listDict['Shaft_list'][valueDict['Shaft']])
                self.project.add(newMass)
                self.massList.append(newMass)
                self.editMassCombo.addItem(valueDict['Name'])
                self.removeMassCombo.addItem(valueDict['Name'])
        
        elif typeMass == 'Equivalent Inertia':
            if len(self.project.listDict['Mass_list']) == 1:
                self.errorWindow = Popup_Info('No Inertia to add an Equivalent Inertia', recWidth=self.recWidth, recHeight=self.recHeight)
            else:
                self.addMassWindow = Popup_Dialog_Single('Add Equivalent Inertia', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
                self.addMassWindow.add_lineEdit('Name')
                self.addMassWindow.add_lineEdit('I', valueUnit='kg.m2')
                shaftNameList = []
                for shaft in self.project.listDict['Shaft_list']:
                    shaftNameList.append(shaft.name)
                self.addMassWindow.add_comboBox('Shaft', shaftNameList)
                massNameList = []
                for i in range(1, len(self.project.listDict['Mass_list'])):
                    massNameList.append(self.project.listDict['Mass_list'][i].name)
                self.addMassWindow.add_comboBox('Mass', massNameList)
                self.addMassWindow.exec_()

                valueDict = self.addMassWindow.get_value()
                if valueDict != 'None':
                    newMass = EquivalentMass(valueDict['Name'], self.get_float(valueDict['I']), self.project.listDict['Shaft_list'][valueDict['Shaft']], 
                                            self.project.listDict['Mass_list'][valueDict['Mass']+1])
                    self.project.add(newMass)
                    self.massList.append(newMass)
                    self.editMassCombo.addItem(valueDict['Name'])
                    self.removeMassCombo.addItem(valueDict['Name'])
        

    def addMulti_mass(self):
        typeMass = self.addMassCombo.currentText()
        if typeMass == 'Inertia':
            self.addMassWindow = Popup_Dialog_Multi('Add Inertia', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
            self.addMassWindow.add_lineEdit('Name')
            self.addMassWindow.add_lineEdit('I', valueUnit='kg.m2')
            shaftNameList = []
            for shaft in self.project.listDict['Shaft_list']:
                shaftNameList.append(shaft.name)
            self.addMassWindow.add_comboBox('Shaft', shaftNameList)
            self.addMassWindow.exec_()

            valueDict = self.addMassWindow.get_value()
            if valueDict != 'None':
                for i in range(0, len(valueDict['Name'])):
                    newMass = Mass(valueDict['Name'][i], self.get_float(valueDict['I'][i]), self.project.listDict['Shaft_list'][valueDict['Shaft'][i]])
                    self.project.add(newMass)
                    self.massList.append(newMass)
                    self.editMassCombo.addItem(valueDict['Name'][i])
                    self.removeMassCombo.addItem(valueDict['Name'][i])
        
        elif typeMass == 'Equivalent Inertia':
            if len(self.project.listDict['Mass_list']) == 1:
                self.errorWindow = Popup_Info('No Inertia to add an Equivalent Inertia', recWidth=self.recWidth, recHeight=self.recHeight)
            else:
                self.addMassWindow = Popup_Dialog_Multi('Add Equivalent Inertia', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
                self.addMassWindow.add_lineEdit('Name')
                self.addMassWindow.add_lineEdit('I', valueUnit='kg.m2')
                shaftNameList = []
                for shaft in self.project.listDict['Shaft_list']:
                    shaftNameList.append(shaft.name)
                self.addMassWindow.add_comboBox('Shaft', shaftNameList)
                massNameList = []
                for i in range(1, len(self.project.listDict['Mass_list'])):
                    massNameList.append(self.project.listDict['Mass_list'][i].name)
                self.addMassWindow.add_comboBox('Mass', massNameList)
                self.addMassWindow.exec_()

                valueDict = self.addMassWindow.get_value()
                if valueDict != 'None':
                    for i in range(0, len(valueDict['Name'])):
                        newMass = EquivalentMass(valueDict['Name'][i], self.get_float(valueDict['I'][i]), self.project.listDict['Shaft_list'][valueDict['Shaft'][i]], 
                                                self.project.listDict['Mass_list'][valueDict['Mass'][i]+1])
                        self.project.add(newMass)
                        self.massList.append(newMass)
                        self.editMassCombo.addItem(valueDict['Name'][i])
                        self.removeMassCombo.addItem(valueDict['Name'][i])


    def edit_mass(self):
        pass


    def remove_mass(self):
        # create a list atribute masslist
        indexMass = self.removeMassCombo.currentIndex()
        if indexMass >= 0:
            mass = self.massList[indexMass]
            if type(mass) == Mass:
                popIndex = 1
                for i in range(0, indexMass):
                    if type(self.massList[i]) == Mass:
                        popIndex += 1

                self.project.listDict['Mass_list'].pop(popIndex)
            elif type(mass) == EquivalentMass:
                popIndex = 0
                for i in range(0, indexMass):
                    if type(self.massList[i]) == EquivalentMass:
                        popIndex += 1

                for addedMass in mass.equivalentMass.addedMass:
                    if addedMass == mass:
                        mass.equivalentMass.addedMass.pop(mass.equivalentMass.addedMass.index(mass))
                        break
                self.project.listDict['EquivalentMass_list'].pop(popIndex)
                        
            self.editMassCombo.removeItem(indexMass)
            self.removeMassCombo.removeItem(indexMass)

