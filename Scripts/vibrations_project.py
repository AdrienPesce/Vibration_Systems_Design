# ----------------------------------------------------------------
#       Import all the libraries for exactra functions      
# ----------------------------------------------------------------
# General Libraries for operating system parameters
import os
import re
# General Librarie for matrix management and operation
import numpy as np 
from numpy import linalg as LA # LA to find eigen values and vectors
# General Librarie for math operations
from math import pi
import cmath

import matplotlib as mpl
import matplotlib.pyplot as plt

# Custom librarie for vibration elements (see file vibrations_elements.py)
from vibrations_elements import Mass, Inertia_Cylinder, EquivalentMass, EquivalentInertia_Cylinder, Stiffness, Stiffness_Cylinder, StiffnessDiscretized, StiffnessDiscretized_Shaft, Damping, Loading, Shaft
# Custom librarie for vibration matrix (see file vibrations_matrix.py)
from vibrations_matrix import Matrix_Mass, LitteralMatrix_Mass, Matrix_Stiffness, LitteralMatrix_Stiffness, Matrix_Loading, LitteralMatrix_Loading
# Custom libraries for Graphical User Interfaces (see file vibrations_popupWindows.py)
# from vibrations_popupWindows import Popup_Info



# ----------------------------------------------------------------
#       Object : Vibration_Project
# ----------------------------------------------------------------
class Vibration_Project:
    def __init__(self, name, directory):
        os.chdir(directory)
        
        self.name = name
        rxTable = re.compile(r'(?P<name>.+)_elements\.csv')
        rxProject = re.compile(r'(?P<name>.+)_project\.csv')
        rxMatrix = re.compile(r'(?P<name>.+)_matrix\.csv')
        rxResults = re.compile(r'(?P<name>.+)_results\.csv')
        rxExtention = re.compile(r'(?P<name>.+)\..+')
        for rx in [rxTable, rxProject, rxMatrix, rxResults, rxExtention]:
            if rx.search(self.name):
                self.name = rx.search(self.name).group('name')
                # print(self.name)
        
        self.file_table = '{}_elements.csv'.format(self.name)
        self.file_projet = '{}_project.csv'.format(self.name)
        self.file_matrix = '{}_matrix.csv'.format(self.name)
        self.file_results = '{}_results.csv'.format(self.name)

        self.massMatrix = Matrix_Mass()
        self.stiffnessMatrix = Matrix_Stiffness('stiffness')
        self.dampingMatrix = Matrix_Stiffness('damping')
        self.loadingMatrix = Matrix_Loading()
        self.listMatrix = [self.massMatrix, self.stiffnessMatrix, self.dampingMatrix, self.loadingMatrix]

        self.massLitteralMatrix = LitteralMatrix_Mass()
        self.stiffnessLitteralMatrix = LitteralMatrix_Stiffness('stiffness')
        self.dampingLitteralMatrix = LitteralMatrix_Stiffness('damping')
        self.loadingLitteralMatrix = LitteralMatrix_Loading()
        self.listLitteralMatrix = [self.massLitteralMatrix, self.stiffnessLitteralMatrix, self.dampingLitteralMatrix, self.loadingLitteralMatrix]

        self.shaft1 = Shaft('shaft1', 1)
        self.frame = Mass('frame', 0, self.shaft1)
        
        self.listDict = {}
        self.listDict['Shaft_list'] = [self.shaft1]
        self.listDict['Mass_list'] = [self.frame]
        self.listDict['EquivalentMass_list'] = []
        self.listDict['Stiffness_list'] = []
        self.listDict['StiffnessDiscretized_list'] = []
        self.listDict['Damping_list'] = [] 
        self.listDict['Loading_list'] = []

        self.pulsatingsDict = {}

        self.globalDamping = 0


    def add(self, element):
        if type(element) == Shaft:
            self.listDict['Shaft_list'].append(element)
        elif type(element) in [Mass, Inertia_Cylinder]:
            self.listDict['Mass_list'].append(element)
        elif type(element) in [EquivalentMass, EquivalentInertia_Cylinder]:
            self.listDict['EquivalentMass_list'].append(element)
        elif type(element) in [Stiffness, Stiffness_Cylinder]:
            self.listDict['Stiffness_list'].append(element)
        elif type(element) == Damping:
            self.listDict['Damping_list'].append(element)
        elif type(element) == Loading:
            self.listDict['Loading_list'].append(element)
        elif type(element) in [StiffnessDiscretized, StiffnessDiscretized_Shaft]:
            self.listDict['StiffnessDiscretized_list'].append(element)
            massList, equivalentMassList, stiffnessList = element.get_lists()
            for mass in massList:
                self.listDict['Mass_list'].append(mass)
            for equivalentMass in equivalentMassList:
                self.listDict['EquivalentMass_list'].append(equivalentMass)
            for stiffness in stiffnessList:
                self.listDict['Stiffness_list'].append(stiffness)


    def get_minMass(self):
        if len(self.listDict['Mass_list']) == 1:
            minMass = None
        else:
            minMass = self.listDict['Mass_list'][1].value
            # print(self.listDict['Mass_list'][1].name, self.listDict['Mass_list'][1].value)
            for i in range(2, len(self.listDict['Mass_list'])):
                if type(self.listDict['Mass_list'][i]) in [Mass, Inertia_Cylinder] and self.listDict['Mass_list'][i].value / ((self.listDict['Mass_list'][i].shaft.ratio)**2) < minMass:
                    minMass = self.listDict['Mass_list'][i].value / ((self.listDict['Mass_list'][i].shaft.ratio)**2)
                    # print(self.listDict['Mass_list'][i].name, self.listDict['Mass_list'][i].value)
        
        return minMass


    def gen_allMatrix(self):
        for matrix in self.listMatrix + self.listLitteralMatrix:
            matrix.gen(self.listDict['Mass_list'])
            # print(matrix.name)
            if self.globalDamping > 0:
                if matrix.name == 'Damping_matrix':
                    matrix.add_globalDamping(self.globalDamping, self.stiffnessMatrix.matrix)
                elif matrix.name == 'Damping_litteralMatrix':
                    matrix.add_globalDamping(self.stiffnessLitteralMatrix.matrix)


    def solve(self):
        self.gen_allMatrix()
        M = np.matrix(self.massMatrix.matrix)
        # print(M)
        K = np.matrix(self.stiffnessMatrix.matrix)
        Minv = M.getI()
        
        A = np.matmul(Minv, K)
        wSquare, v = LA.eig(A)

        pulsatings = []
        modes = []
        for i in range(0, len(wSquare)):
            if wSquare[i] > 0:
                pulsatings.append(wSquare[i]**0.5)
            else:
                pulsatings.append(0)
            mode = []
            for j in range(0, len(wSquare)):
                mode.append(v.item((j, i)))
            modes.append(mode)

        resultsFile = open(self.file_results, 'w')
        resultsFile.write('n;w [rad/s];f [hz];mode\n')

        j = 1
        while len(pulsatings) > 0:
            indexMin = 0
            for i in range(1, len(pulsatings)):
                if pulsatings[i] < pulsatings[indexMin]:
                    indexMin = i

            c = 0
            while modes[indexMin][c] == 0:
                c += 1
            coeff = 1/modes[indexMin][c]
            for k in range(0, len(modes[indexMin])):
                modes[indexMin][k] = modes[indexMin][k] * coeff
                
            self.pulsatingsDict['w{}'.format(j)] = pulsatings[indexMin]
            self.pulsatingsDict['mode{}'.format(j)] = modes[indexMin]

            resultsFile.write('{};{};{};{}\n'.format(j, pulsatings[indexMin], pulsatings[indexMin]/(2*pi), str(modes[indexMin])[1:-1].replace(',', ';')))
            
            pulsatings.pop(indexMin)
            modes.pop(indexMin)
            j += 1

        resultsFile.close()

        # self.w = Popup_Info('Solve complete successfully')


    def solve_dynamicResponce(self):
        self.gen_allMatrix()
        M = np.matrix(self.massMatrix.matrix)
        K = np.matrix(self.stiffnessMatrix.matrix)
        Kp = np.matrix(self.dampingMatrix.matrix)
        F = np.matrix(self.loadingMatrix.matrix).getT()

        i = 0
        while 'w{}'.format(i+1) in self.pulsatingsDict:
            i += 1

        wMin = 1
        wMax = int(self.pulsatingsDict['w{}'.format(i)] * 1.1) + 1
        # print(wMax)
        step = int(wMax*0.001)
        
        self.responcesDict = {}
        for i in range(1, len(self.listDict['Mass_list'])):
            self.responcesDict[self.listDict['Mass_list'][i].name] = []

        # print(self.responcesDict)

        self.responcesDict['w'] = range(wMin, wMax, step)

        for w in range(wMin, wMax, step):
            B = (K - w**2*M) + Kp*1j
            # print(B)
            X = np.matmul(LA.inv(B), F)
            # if w == wMin:
            #     print(w*Kp)
            #     print(np.matmul(LA.inv(B), B))
            
            for i in range(1, len(self.listDict['Mass_list'])):
                # print(X)
                # print(X.item(i-1, 0))
                normXi = abs(X.item(i-1, 0))
                if normXi < 10e-100:
                    normXi = 10e-100
                self.responcesDict[self.listDict['Mass_list'][i].name].append(normXi)

        # print(self.responcesDict)


    def print_matix(self):
        for matrix in self.listMatrix:
            matrix.print()
        

    def open_project(self):
        rxBegin = re.compile(r'begin (?P<name>.+) :')
        rxEnd = re.compile(r'end')
        rxDict = re.compile(r'(?P<key>\S+) = (?P<value>.+)')
        rxNew = re.compile(r'new elem')
        fileProject = open(self.file_projet, 'r')
        lines = fileProject.readlines()
        fileProject.close()
        i = 0
        while i < len(lines):
            foundBegin = rxBegin.search(lines[i])
            if foundBegin:
                nameList = foundBegin.group('name')
                i += 1
                # print(nameList)
                while not rxEnd.search(lines[i]):
                    dictClass = {}
                    while not rxNew.search(lines[i]) and not rxEnd.search(lines[i+1]):
                        foundDict = rxDict.search(lines[i])
                        if foundDict:
                            key = foundDict.group('key')
                            value = foundDict.group('value')
                            dictClass[key] = value
                        i += 1
                    if dictClass != {}:
                        # print(dictClass)
                        if nameList == 'Mass_list' and dictClass['name'] != 'frame':
                            mass = Mass(None, None, None)
                            mass.read(dictClass)
                            self.listDict['Mass_list'].append(mass)
                        elif nameList == 'Stiffness_list':
                            stiffness = Stiffness(None, None, None, None, None)
                            stiffness.read(dictClass, self.listDict['Mass_list'])
                            self.listDict['Stiffness_list'].append(stiffness)
                        elif nameList == 'Damping_list':
                            damping = Damping(None, None, None, None, None)
                            damping.read(dictClass, self.listDict['Mass_list'])
                            self.listDict['Damping_list'].append(damping)
                        elif nameList == 'Loading_list':
                            loading = Loading(None, None, None)
                            loading.read(dictClass, self.listDict['Mass_list'])
                            self.listDict['Loading_list'].append(loading)
                        elif nameList == 'StiffnessDiscretized_list':
                            stiffnessDiscretized = StiffnessDiscretized(None, None, None, None, None)
                            stiffnessDiscretized.read(dictClass, self.listDict['Mass_list'], self.listDict['Stiffness_list'])
                            self.listDict['StiffnessDiscretized_list'].append(stiffnessDiscretized)
                    i += 1
            i += 1


    def open_table(self):
        rxBegin = re.compile(r'begin (?P<name>.[^;]+)')
        rxEnd = re.compile(r'end')
        fileProject = open(self.file_table, 'r', encoding='utf8')
        lines = fileProject.readlines()
        fileProject.close()
        i = 0
        while i < len(lines):
            foundBegin = rxBegin.search(lines[i])
            if foundBegin:
                nameList = foundBegin.group('name')
                i += 2
                # print(nameList)
                while not rxEnd.search(lines[i]):
                    while not rxEnd.search(lines[i+1]):
                        args = lines[i][:-1].split(';')
                        if nameList.lower() == 'shaft':
                            name = args [0]
                            ratio = float(args[1].replace(',', '.'))
                            for shaft in self.listDict['Shaft_list']:
                                if shaft.name.lower() == args[2].lower():
                                    connectedShaft = shaft
                                    break
                            newShaft = Shaft(name, ratio, connectedShaft=connectedShaft)
                            self.add(newShaft)
                        
                        elif nameList.lower() == 'inertia_cylinder':
                            name = args [0]
                            d = float(args[1].replace(',', '.'))
                            l = float(args[2].replace(',', '.'))
                            rho = float(args[3].replace(',', '.'))
                            for shaft in self.listDict['Shaft_list']:
                                if shaft.name.lower() == args[4].lower():
                                    selfShaft = shaft
                                    break
                            newInertia_Cylinder = Inertia_Cylinder(name, d, l, rho, selfShaft)
                            self.add(newInertia_Cylinder)
                        
                        elif nameList.lower() == 'equivalentinertia_cylinder':
                            name = args [0]
                            d = float(args[1].replace(',', '.'))
                            l = float(args[2].replace(',', '.'))
                            rho = float(args[3].replace(',', '.'))
                            for shaft in self.listDict['Shaft_list']:
                                if shaft.name.lower() == args[4].lower():
                                    selfShaft = shaft
                                    break
                            for mass in self.listDict['Mass_list']:
                                if mass.name.lower() == args[5].lower():
                                    selfMass = mass
                                    break
                            newEquivalentInertia_Cylinder = EquivalentInertia_Cylinder(name, d, l, rho, shaft, selfMass)
                            self.add(newEquivalentInertia_Cylinder)

                        elif nameList.lower() == 'stiffness':
                            # print("stiffness")
                            name = args [0]
                            value = float(args[1].replace(',', '.'))
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list']:
                                if inertia.name.lower() == args[2].lower():
                                    inertia1 = inertia
                                    break
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list']:
                                if inertia.name.lower() == args[3].lower():
                                    inertia2 = inertia
                                    break
                            # print('inertia1', inertia1.name, 'inertia2', inertia2.name)
                            newStiffness = Stiffness(name, value, inertia1.shaft, inertia1, inertia2)
                            self.add(newStiffness)                        

                        elif nameList.lower() == 'stiffness_cylinder':
                            name = args [0]
                            d = float(args[1].replace(',', '.'))
                            l = float(args[2].replace(',', '.'))
                            g = float(args[3].replace(',', '.'))
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list']:
                                if inertia.name.lower() == args[4].lower():
                                    inertia1 = inertia
                                    break
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list']:
                                if inertia.name.lower() == args[5].lower():
                                    inertia2 = inertia
                                    break
                            # print('inertia1', inertia1.name, 'inertia2', inertia2.name)
                            newStiffness_Cylinder = Stiffness_Cylinder(name, d, l, g, inertia1.shaft, inertia1, inertia2)
                            self.add(newStiffness_Cylinder)
                        
                        elif nameList.lower() == 'stiffnessdiscretized_shaft':
                            name = args [0]
                            d = float(args[1].replace(',', '.'))
                            l = float(args[2].replace(',', '.')) #+1
                            g = float(args[3].replace(',', '.'))
                            rho = float(args[4].replace(',', '.'))
                            nbDiscretization = int(args[5].replace(',', '.')) if args[5] != '' else None
                            minMass = None
                            if not nbDiscretization:
                                minMass = self.get_minMass()
                            for shaft in self.listDict['Shaft_list']:
                                if shaft.name.lower() == args[6].lower():
                                    selfShaft = shaft
                                    break
                            inertia1 = None
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list'] + self.listDict['StiffnessDiscretized_list']:
                                if inertia.name.lower() == args[7].lower():
                                    inertia1 = inertia
                                    break
                            inertia2 = None
                            for inertia in self.listDict['Mass_list'] + self.listDict['EquivalentMass_list'] + self.listDict['StiffnessDiscretized_list']:
                                if inertia.name.lower() == args[8].lower():
                                    inertia2 = inertia
                                    break
                            # if inertia1 and inertia2:    
                            #     print(inertia1.name, inertia2.name)    
                            # elif inertia1:    
                            #     print(inertia1.name, inertia2)
                            # elif inertia2:    
                            #     print(inertia1, inertia2.name)
                            # else:
                            #     print(inertia1, inertia2)
                            newStiffnessDiscretized_Shaft = StiffnessDiscretized_Shaft(name, d, l, g, rho, nbDiscretization, selfShaft, mass1=inertia1, mass2=inertia2, minMass=minMass)
                            self.add(newStiffnessDiscretized_Shaft)

                        elif nameList.lower() == 'global_damping':
                            value = float(args[0].replace(',', '.'))
                            self.globalDamping = value

                        elif nameList.lower() == 'loading':
                            name = args [0]
                            value = float(args[1].replace(',', '.'))
                            for mass in self.listDict['Mass_list']:
                                if mass.name.lower() == args[2].lower():
                                    selfMass = mass
                                    break
                            newLoading = Loading(name, value, mass)
                            self.add(newLoading)
                        
                        i += 1
                    i += 1
            i += 1


    def save_project(self):
        fileMatrix = open(self.file_matrix, 'w')
        for matrix in self.listMatrix + self.listLitteralMatrix:
            matrix.save(fileMatrix, self.listDict['Mass_list'][1:])
        fileMatrix.close()

        fileProject = open(self.file_projet, 'w')
        listTypes = [Mass, Stiffness, Damping, Loading]
        listName = ['Mass_list', 'Stiffness_list', 'Damping_list', 'Loading_list', 'StiffnessDiscretized_list']
        for name in listName:
            fileProject.write('begin {} :\n'.format(name))
            for elem in self.listDict[name]:
                fileProject.write('    new elem\n')
                for k, v in elem.__dict__.items():
                    if type(v) in listTypes:
                        fileProject.write('        {} = {}\n'.format(k, v.name))
                    elif type(v) == list:
                        newV = []
                        for value in v:
                            if type(value) in listTypes:
                                newV.append(value.name)
                            else:
                                newV.append(value)
                        fileProject.write('        {} = {}\n'.format(k, newV))
                    else:
                        fileProject.write('        {} = {}\n'.format(k, v))
                fileProject.write('\n')
            fileProject.write('end\n\n')
        fileProject.close()
        
        for shaft in self.listDict['Shaft_list']:
            figure = plt.figure(figsize=(10,5)) 
            axes = figure.add_subplot(111)
            axes.set_yscale('log')
            axes.set_ylabel('Responce [rad]')
            axes.set_xlabel('Pulsating [rad/s]')
            for mass in self.listDict['Mass_list'][1:]:
                if mass.shaft.name == shaft.name:
                    x = self.responcesDict['w']
                    y = self.responcesDict[mass.name]
                    axes.plot(x, y, label=mass.name)
                    
            figure.legend()
            figure.savefig('responces_{}'.format(shaft.name))

        os.mkdir('modes')
        i = 1
        while 'mode{}'.format(i) in self.pulsatingsDict:
            figure = plt.figure(figsize=(10,5)) 
            axes = figure.add_subplot(111)
            axes.set_ylabel('Amplitude')
            axes.set_xlabel('Degrees of freedom')
            x = [i for i in range(1, len(self.pulsatingsDict['mode{}'.format(i)])+1)]
            y = self.pulsatingsDict['mode{}'.format(i)]
            axes.plot(x, y, label='mode{}'.format(i))

            figure.legend()
            figure.savefig('modes/responces_mode{}'.format(i))
            i += 1


