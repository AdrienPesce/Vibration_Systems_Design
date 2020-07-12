#!/usr/bin/python3.5
import sys
import os
import PyQt5.QtWidgets as qtw 
import matplotlib.pyplot as plt

from vibrations_mainWindow import Main_Window
from vibrations_popupWindows import Popup_Info
from vibrations_computingWindows import Computing_Modes, Computing_Responces, Plot_Matrix

from vibrations_project import Vibration_Project 
from vibrations_elements import Mass, EquivalentMass, Stiffness, StiffnessDiscretized, StiffnessDiscretized_Shaft, Damping, Loading, Shaft

        
def main():
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    _ = Main_Window(rect.width(), rect.height())
    sys.exit(app.exec_())


def save():
    app = qtw.QApplication(sys.argv)
    project = Vibration_Project('test', os.getcwd())
    for i in range(1, 3):
        m = Mass('m{}'.format(i), 20e3, project.shaft1)
        project.add(m)
    k = Stiffness('k1', 18e6, project.shaft1, project.frame, project.listDict['Mass_list'][1])
    project.add(k)
    k = Stiffness('k2', 18e6, project.shaft1, project.listDict['Mass_list'][1], project.listDict['Mass_list'][2])
    project.add(k)
    f = Loading('F1', 20, project.listDict['Mass_list'][1])
    project.add(f)
    project.gen_allMatrix()
    project.print_matix()
    project.solve()
    project.solve_dynamicResponce()
    project.save_project()
    # win = Computing_Modes(project.pulsatingsDict)
    _ = Computing_Responces(project.responcesDict, project.listDict['Mass_list'])
    sys.exit(app.exec_())


def open_project():
    project = Vibration_Project('shaft', os.getcwd())
    project.open_project()
    project.gen_allMatrix()
    project.print_matix()
    project.solve()


def test():
    firstPulsating = []
    for i in range(1, 51):
        project = Vibration_Project('shaft', os.getcwd())
        kDis = StiffnessDiscretized_Shaft('k1', 5e-3, 100e-3, 81e9, 7500, i, project.shaft1) #, mass1=project.frame, mass2=project.frame)
        project.add(kDis)
        project.gen_allMatrix()
        # project.print_matix()
        project.solve()
        firstPulsating.append(project.pulsatingsDict['w2']/2*3.14159265358)

    plt.plot(firstPulsating)
    plt.show()

def mainWindow():
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    ex = Main_Window(rect.width(), rect.height())
    # Show widget
    ex.show()
    sys.exit(app.exec_())


def csv4():
    project = Vibration_Project('csv4', os.getcwd())
    shaft2 = Shaft('shaft2', -2, project.shaft1)
    
    j1 = Mass('j1', 7.62e-4, project.shaft1)
    project.add(j1)
    j2 = Mass('j2', 7.62e-4, project.shaft1)
    project.add(j2)
    j3 = Mass('j3', 7.62e-4/4, project.shaft1)
    j2.addedMass.append(j3)
    j4 = Mass('j4', 7.62e-4, project.shaft1)
    project.add(j4)
    
    k1 = Stiffness('k1', 3.73e3, project.shaft1, project.frame, project.listDict['Mass_list'][1])
    project.add(k1)
    k2 = Stiffness('k2', 3.73e3, project.shaft1, project.listDict['Mass_list'][1], project.listDict['Mass_list'][2])
    project.add(k2)
    k3 = Stiffness('k3', 3.73e3, shaft2, project.listDict['Mass_list'][2], project.listDict['Mass_list'][3])
    project.add(k3)
    
    project.gen_allMatrix()
    project.print_matix()
    project.solve()
    project.save_project()


def popup():
    app = qtw.QApplication(sys.argv)
    # screen = app.primaryScreen()
    # rect = screen.availableGeometry()
    _ = Popup_Info('Solve complete successfully')
    # Show widget
    sys.exit(app.exec_())


def openTable():
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    project = Vibration_Project('project4_simple', os.path.join(os.getcwd(), '../'))
    project.open_table()
    # print('open table')
    project.gen_allMatrix()
    project.save_project()
    # print(project.listMatrix[0].matrix)
    # project.print_matix()
    # print(project.listDict['Mass_list'][1].linked_stiffness[1].name)
    for mass in project.listDict['Mass_list']:
        if mass.name == 'K1.2_0':
            loading = Loading('C_entree', 1, mass)
            project.add(loading)
            break
    project.solve()
    project.solve_dynamicResponce()
    # for mass in project.listDict['Mass_list'][4].linked_stiffness:
    #     print(mass.name)
    # print('solved')
    win1 = Plot_Matrix('All', project.listDict, project.listMatrix, rect.width(), rect.height())
    win1.show()
    win = Computing_Responces(project.responcesDict, project.listDict['Mass_list'])
    win.show()
    _ = Computing_Modes(project.pulsatingsDict)
    sys.exit(app.exec_())


def testShaft():
    project = Vibration_Project('test_shaft', os.getcwd())
    j1 = Mass('j1', 20, project.shaft1)
    project.add(j1)
    j2 = Mass('j2', 20, project.shaft1)
    project.add(j2)
    j3 = EquivalentMass('j3', 20, project.shaft1, j1)
    project.add(j3)
    j4 = EquivalentMass('j4', 20, project.shaft1, j2)
    project.add(j4)
    # k = Stiffness('k1', 30, project.shaft1, j3, j4)
    # project.add(k)
    k1 = StiffnessDiscretized('k1', 60, 60, 2, project.shaft1)
    project.add(k1)
    minMass = project.get_minMass()
    k2 = StiffnessDiscretized('k1', 60, 60, None, project.shaft1, mass1=j3, mass2=None, minMass=minMass)
    project.add(k2)
    # for mass in project.listDict['Mass_list']:
    #     print(mass.name)#, mass.value, mass.mass1.name, mass.mass2.name)
    project.gen_allMatrix()
    project.print_matix()
    

if __name__ == '__main__':
    # app = qtw.QApplication(sys.argv)
    # save()
    # test()
    # open_project()
    # main()
    # popup()
    # mainWindow()
    # csv4()
    # sys.exit(app.exec_())
    openTable()
    # testShaft()