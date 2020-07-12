
import os
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

from vibrations_project import Vibration_Project 
from vibrations_elements import Mass, EquivalentMass, Stiffness, StiffnessDiscretized, StiffnessDiscretized_Shaft, Damping, Loading, Shaft

from vibrations_computingWindows import Computing_Modes, Computing_Responces, Plot_Matrix
from vibrations_popupWindows import Popup_Dialog_Single, Popup_Dialog_Multi, Popup_Info

from math import pi


# -------------------------------------------------- #
# ---------------- TabsTanslational ---------------- #
# -------------------------------------------------- #
class TabsTanslational(qtw.QTabWidget):
    def __init__(self, projectDir, width, height, parent = None):
        super(TabsTanslational, self).__init__(parent)
        self.title = 'Vibrations Project'
        self.left, self.top = 0, 0
        self.recWidth, self.recHeight = width, height
        self.width, self.height = 400, 100
        
        self.projectName = os.path.basename(projectDir)
        self.projectFolder = os.path.dirname(projectDir)

        self.project = Vibration_Project(self.projectName, self.projectFolder)
        self.massList = []
        self.stiffnessList = []
        self.dampingList = []
        self.loadingList = []

        self.createTabs()
        self.show()
        

    def createTabs(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create the tabs     
        self.createTabMass()
        self.createTabStiffness()
        self.createTabDamping()
        self.createTabLoading()
        self.createTabComputing()


    def get_float(self, string):
        # print(string)
        if '/' in string:
            splitSting = string.split('/')
            result = self.get_float(splitSting[0])
            for i in range(1, len(splitSting)):
                result = result / self.get_float(splitSting[i])
        
        elif '*' in string:
            splitSting = string.split('*')
            result = self.get_float(splitSting[0])
            for i in range(1, len(splitSting)):
                result = result * self.get_float(splitSting[i])
        
        elif '-' in string:
            splitSting = string.split('-')
            if len(splitSting) == 2 and splitSting[0].endswith('e'):
                result = float(splitSting[0]+'-'+splitSting[1])
            else:
                newSplitSting = []
                for j in range(0, len(splitSting)-1):
                    if splitSting[j].endswith('e'):
                        print('endswith')
                        newSplitSting.append(splitSting[j]+'-'+splitSting[j+1])
                        j += 1
                    else:
                        newSplitSting.append(splitSting[j])
                newSplitSting.append(splitSting[-1])
                result = self.get_float(newSplitSting[0])
                for i in range(1, len(newSplitSting)):
                    result = result - self.get_float(newSplitSting[i])
            
        elif '+' in string:
            splitSting = string.split('+')
            if len(splitSting) == 2 and splitSting[0].endswith('e'):
                result = float(splitSting[0]+'+'+splitSting[1])
            else:
                newSplitSting = []
                for j in range(0, len(splitSting)-1):
                    if splitSting[j].endswith('e'):
                        print('endswith')
                        newSplitSting.append(splitSting[j]+'+'+splitSting[j+1])
                        j += 1
                    else:
                        newSplitSting.append(splitSting[j])
                newSplitSting.append(splitSting[-1])
                result = self.get_float(newSplitSting[0])
                for i in range(1, len(newSplitSting)):
                    result = result + self.get_float(newSplitSting[i])

        elif string == '':
            result = 0
            
        else:
            result = float(string)
        return result


    def save(self):
        self.project.save_project()


    def saveAs(self, filename):
        pass


    def open(self):
        self.project.open_project()


    def importElements(self, fileName):
        self.project.file_table = fileName
        self.project.open_table()


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
        self.addMassCombo.addItems(['Mass', 'Equivelent Mass'])
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
        self.addTab(self.tabMass, 'Mass')


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



    # ----------------------------------------------- #
    # ---------------- Stiffness tab ---------------- #
    # ----------------------------------------------- #
    def createTabStiffness(self):
        # Creat the Stiffness widget
        self.tabStiffness = qtw.QWidget()

        buttonAddStiffness = qtw.QPushButton('Add', self.tabStiffness)
        buttonAddStiffness.clicked.connect(self.add_stiffness)
        buttonAddStiffness.move(10, 10)

        buttonAddMultiStiffness = qtw.QPushButton('Add Multi', self.tabStiffness)
        buttonAddMultiStiffness.clicked.connect(self.addMulti_stiffness)
        buttonAddMultiStiffness.move(100, 10)

        self.addStiffnessCombo = qtw.QComboBox(self.tabStiffness)
        self.addStiffnessCombo.addItems(['Stiffness', 'StiffnessDiscretized', 'StiffnessDiscretized Shaft'])
        self.addStiffnessCombo.move(190, 10)
       
        buttonEditStiffness = qtw.QPushButton('Edit', self.tabStiffness)
        buttonEditStiffness.clicked.connect(self.edit_stiffness)
        buttonEditStiffness.move(10, 48)

        self.editStiffnessCombo = qtw.QComboBox(self.tabStiffness)
        self.editStiffnessCombo.move(100, 48)

        buttonRemoveStiffness = qtw.QPushButton('Remove', self.tabStiffness)
        buttonRemoveStiffness.clicked.connect(self.remove_stiffness)
        buttonRemoveStiffness.move(10, 86)

        self.removeStiffnessCombo = qtw.QComboBox(self.tabStiffness)
        self.removeStiffnessCombo.move(100, 86)

        # Add the widget to the tabs
        self.addTab(self.tabStiffness, 'Stiffness')


    def add_stiffness(self):
        pass


    def addMulti_stiffness(self):
        typeStiffness = self.addStiffnessCombo.currentText()
        if typeStiffness == 'Stiffness':
            self.addStiffnessWindow = Popup_Dialog_Multi('Add Stiffness', 'Add', recWidth=self.recWidth, recHeight=self.recHeight)
            self.addStiffnessWindow.add_lineEdit('Name')
            self.addStiffnessWindow.add_lineEdit('K', valueUnit='N.rad')
            # shaftNameList = []
            # for shaft in self.project.listDict['Shaft_list']:
            #     shaftNameList.append(shaft.name)
            # self.addStiffnessWindow.add_comboBox('Shaft', shaftNameList)
            mass1NameList = []
            for mass in self.project.listDict['Mass_list']:
                mass1NameList.append(mass.name)
            self.addStiffnessWindow.add_comboBox('Mass1', mass1NameList)
            mass2NameList = []
            for mass in self.project.listDict['Mass_list']:
                mass2NameList.append(mass.name)
            self.addStiffnessWindow.add_comboBox('Mass2', mass2NameList)
            self.addStiffnessWindow.exec_()

            valueDict = self.addStiffnessWindow.get_value()
            for i in range(0, len(valueDict['Name'])):
                name = valueDict['Name'][i]
                value = self.get_float(valueDict['K'][i])
                mass1 = self.project.listDict['Mass_list'][valueDict['Mass1'][i]]
                mass2 = self.project.listDict['Mass_list'][valueDict['Mass2'][i]]
                if mass1.shaft == mass2.shaft:
                    shaft = mass1.shaft
                    newStiffness = Stiffness(name, value, shaft, mass1, mass2)
                    self.project.add(newStiffness)
                else:
                    text = '{} and {} are not in the same shaft'.format(mass1.name, mass2.name)
                    Popup_Info(text, recWidth=self.recWidth, recHeight=self.recHeight)
        
        elif typeStiffness == 'StiffnessDiscretized':
            pass
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
                for i in range(0, len(valueDict['Name'])):
                    newMass = EquivalentMass(valueDict['Name'][i], self.get_float(valueDict['I'][i]), self.project.listDict['Shaft_list'][valueDict['Shaft'][i]], self.project.listDict['Mass_list'][valueDict['Mass'][i]])
                    self.project.add(newMass)


    def edit_stiffness(self):
        pass


    def remove_stiffness(self):
        pass



    # --------------------------------------------- #
    # ---------------- Damping tab ---------------- #
    # --------------------------------------------- #
    def createTabDamping(self):
        # Create the Damping time widget
        self.tabDamping = qtw.QWidget()

        buttonAddDamping = qtw.QPushButton('Add', self.tabDamping)
        buttonAddDamping.clicked.connect(self.add_damping)
        buttonAddDamping.move(10, 10)

        buttonEditDamping = qtw.QPushButton('Edit', self.tabDamping)
        buttonEditDamping.clicked.connect(self.edit_damping)
        buttonEditDamping.move(10, 48)

        buttonRemoveDamping = qtw.QPushButton('Remove', self.tabDamping)
        buttonRemoveDamping.clicked.connect(self.remove_damping)
        buttonRemoveDamping.move(10, 86)

        # Add the widget to the tabs
        self.addTab(self.tabDamping, 'Damping')
        

    def add_damping(self):
        pass


    def edit_damping(self):
        pass


    def remove_damping(self):
        pass


    # --------------------------------------------- #
    # ---------------- Loading tab ---------------- #
    # --------------------------------------------- #
    def createTabLoading(self):
        # Create the Loading time widget
        self.tabLoading = qtw.QWidget()

        buttonAddLoading = qtw.QPushButton('Add', self.tabLoading)
        buttonAddLoading.clicked.connect(self.add_loading)
        buttonAddLoading.move(10, 10)

        buttonEditLoading = qtw.QPushButton('Edit', self.tabLoading)
        buttonEditLoading.clicked.connect(self.edit_loading)
        buttonEditLoading.move(10, 48)

        buttonRemoveLoading = qtw.QPushButton('Remove', self.tabLoading)
        buttonRemoveLoading.clicked.connect(self.remove_loading)
        buttonRemoveLoading.move(10, 86)

        # Add the widget to the tabs
        self.addTab(self.tabLoading, 'Loading')
        

    def add_loading(self):
        pass


    def edit_loading(self):
        pass


    def remove_loading(self):
        pass


    # ----------------------------------------------- #
    # ---------------- Computing tab ---------------- #
    # ----------------------------------------------- #
    def createTabComputing(self):
        # Create table
        self.tabComputing = qtw.QWidget()

        buttonGenMatrix = qtw.QPushButton('Generate Matrix', self.tabComputing)
        buttonGenMatrix.clicked.connect(self.genMatrix)
        buttonGenMatrix.move(10, 10)

        self.comboGenMatrix = qtw.QComboBox(self.tabComputing)
        self.comboGenMatrix.addItems(['All', 'Mass', 'Stiffness', 'Damping', 'Loading'])
        self.comboGenMatrix.move(130, 10)

        buttonShowMatrix = qtw.QPushButton('Show Matrix', self.tabComputing)
        buttonShowMatrix.clicked.connect(self.showMatrix)
        buttonShowMatrix.move(10, 48)

        buttonShowLitteralMatrix = qtw.QPushButton('Show Litteral Matrix', self.tabComputing)
        buttonShowLitteralMatrix.clicked.connect(self.showLitteralMatrix)
        buttonShowLitteralMatrix.move(110, 48)
                
        self.comboShowMatrix = qtw.QComboBox(self.tabComputing)
        self.comboShowMatrix.addItems(['All', 'Mass', 'Stiffness', 'Damping', 'Loading'])
        self.comboShowMatrix.move(260, 48)

        buttonSolveModes = qtw.QPushButton('Solve Modes', self.tabComputing)
        buttonSolveModes.clicked.connect(self.solveModes)
        buttonSolveModes.move(10, 86)
        
        buttonPlotModes = qtw.QPushButton('Plot Modes', self.tabComputing)
        buttonPlotModes.clicked.connect(self.plotModes)
        buttonPlotModes.move(115, 86)

        buttonSolveResponces = qtw.QPushButton('Solve Responce', self.tabComputing)
        buttonSolveResponces.clicked.connect(self.solve_dynamicResponce)
        buttonSolveResponces.move(205, 86)
        
        buttonPlotResponces = qtw.QPushButton('Plot Responce', self.tabComputing)
        buttonPlotResponces.clicked.connect(self.plotResponces)
        buttonPlotResponces.move(325, 86)

        # Add the table to the tabs
        self.addTab(self.tabComputing, 'Computing')


    def genMatrix(self):
        matrix2gen = self.comboGenMatrix.currentText()
        if matrix2gen == 'All':
            self.project.gen_allMatrix()
            self.infoWindow = Popup_Info('All matrix generated', recWidth=self.recWidth, recHeight=self.recHeight)
        elif matrix2gen == 'Mass':
            self.project.massMatrix.gen(self.project.listDict['Mass_list'])
            self.infoWindow = Popup_Info('Mass matrix generated', recWidth=self.recWidth, recHeight=self.recHeight)
        elif matrix2gen == 'Stiffness':
            self.project.stiffnessMatrix.gen(self.project.listDict['Mass_list'])
            self.infoWindow = Popup_Info('Stiffness matrix generated', recWidth=self.recWidth, recHeight=self.recHeight)
        elif matrix2gen == 'Damping':
            self.project.dampingMatrix.gen(self.project.listDict['Mass_list'])
            self.infoWindow = Popup_Info('Damping matrix generated', recWidth=self.recWidth, recHeight=self.recHeight)
        elif matrix2gen == 'Loading':
            self.project.loadingMatrix.gen(self.project.listDict['Mass_list'])
            self.infoWindow = Popup_Info('Loading matrix generated', recWidth=self.recWidth, recHeight=self.recHeight)
        else:
            print('Undefined value')
            self.infoWindow = Popup_Info('Undefined value to generate matrix', recWidth=self.recWidth, recHeight=self.recHeight)


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

    
    def showPulsatings(self):
        i = 1
        while 'w{}'.format(i) in self.project.pulsatingsDict.keys():
            print('w{} = {} rad/s'.format(i, self.project.pulsatingsDict['w{}'.format(i)]))
            print('f{} = {} Hz'.format(i, self.project.pulsatingsDict['w{}'.format(i)]/(2*pi)))
            print('mode{}'.format(i))
            print(self.project.pulsatingsDict['mode{}'.format(i)])
            print('')
            i += 1


    def solveModes(self):
        self.project.solve()
        self.infoWindow = Popup_Info('Modes solved', recWidth=self.recWidth, recHeight=self.recHeight)
         

    def plotModes(self):
        # app = qtw.QApplication(sys.argv)
        self.wModes = Computing_Modes(self.project.pulsatingsDict)
        self.wModes.show()
        print('end')


    def solve_dynamicResponce(self):
        self.project.solve_dynamicResponce()
        self.infoWindow = Popup_Info('Responces solved', recWidth=self.recWidth, recHeight=self.recHeight)


    def plotResponces(self):
        # app = qtw.QApplication(sys.argv)
        self.wResponces = Computing_Responces(self.project.responcesDict, self.project.listDict['Mass_list'])
        self.wResponces.show()
        print('end')
