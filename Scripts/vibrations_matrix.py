
from abc import ABC, abstractmethod

from vibrations_elements import EquivalentMass, DiscretizedEquivalentMass, EquivalentInertia_Cylinder

# --------------------------------------------------- #
# ---------------- Class Matrix_Mass ---------------- #
# --------------------------------------------------- #  
class Matrix_Mass(ABC):
    def __init__(self):
        self.name = 'Mass_matrix'
        self.matrix = None


    def gen(self, massList):
        self.matrix = [[0 for i in range(1, len(massList))] for j in range(1, len(massList))]
        for k in range(1, len(massList)):
            self.matrix[k-1][k-1] = massList[k].totalValue


    def print(self):
        if self.matrix:
            print(self.name)
            for line in self.matrix:
                print(line)
            print(' ')


    def save(self, fileMatrix, massList):
        if self.matrix:
            fileMatrix.write('begin {} :\n'.format(self.name))

            fileMatrix.write('{0: >20};'.format(' '))
            for mass in massList[:-1]:
                fileMatrix.write('{0: >20};'.format(mass.name))
            fileMatrix.write('{0: >20}\n'.format(massList[-1].name))
            
            for line in self.matrix:
                fileMatrix.write('{0: >20};'.format(massList[self.matrix.index(line)].name))
                if type(line) == list:
                    for i in range(0, len(line)-1):
                        fileMatrix.write('{0: >20};'.format(line[i]))
                    fileMatrix.write('{0: >20}\n'.format(line[-1]))
                else:
                    fileMatrix.write('{}\n'.format(line))
            fileMatrix.write('end\n\n')



# ----------------------------------------------------------- #
# ---------------- Class LitteralMatrix_Mass ---------------- #
# ----------------------------------------------------------- #  
class LitteralMatrix_Mass(Matrix_Mass):
    def __init__(self):
        self.name = 'mass_litteralMatrix'
        self.matrix = None


    def gen(self, massList):
        self.matrix = [[0 for i in range(1, len(massList))] for j in range(1, len(massList))]
        for k in range(1, len(massList)):
            value = massList[k].name
            for addedMass in massList[k].addedMass:
                value += '+{}'.format(addedMass.name)
            self.matrix[k-1][k-1] = value



# -------------------------------------------------------- #
# ---------------- Class Matrix_Stiffness ---------------- #
# -------------------------------------------------------- #  
class Matrix_Stiffness(Matrix_Mass):
    def __init__(self, typeStiffness):
        self.matrix = None
        self.type = typeStiffness
        if self.type == 'stiffness':
            self.name = 'Stiffness_matrix'
        else:
            self.name = 'Damping_matrix'


    def gen(self, massList):
        self.matrix = [[0 for i in range(1, len(massList))] for j in range(1, len(massList))]
        for k in range(1, len(massList)):
            if self.type == 'stiffness':
                linked_stiffness = massList[k].linked_stiffness
            else:
                linked_stiffness = massList[k].linked_damping
            
            for stiffness in linked_stiffness:
                if stiffness:
                    self.matrix[k-1][k-1] += stiffness.value
                    i = linked_stiffness.index(stiffness)
                    linkedMass = massList[k].linked_mass[i]
                    while type(linkedMass) in [EquivalentMass, DiscretizedEquivalentMass, EquivalentInertia_Cylinder]:
                        linkedMass = linkedMass.equivalentMass
                    if linkedMass.name != 'frame':
                        l = massList.index(linkedMass)
                        self.matrix[k-1][l-1] -= stiffness.value

        
    def add_globalDamping(self, globalDamping, stiffnessMatrix):
        for i in range(0, len(stiffnessMatrix[0])):
            for j in range(0, len(stiffnessMatrix[0])):
                self.matrix[i][j] += globalDamping*stiffnessMatrix[i][j]


# ---------------------------------------------------------------- #
# ---------------- Class LitteralMatrix_Stiffness ---------------- #
# ---------------------------------------------------------------- #  
class LitteralMatrix_Stiffness(Matrix_Mass):
    def __init__(self, typeStiffness):
        self.matrix = None
        self.type = typeStiffness
        if self.type == 'stiffness':
            self.name = 'Stiffness_litteralMatrix'
        else:
            self.name = 'Damping_litteralMatrix'


    def gen(self, massList):
        self.matrix = [[0 for i in range(1, len(massList))] for j in range(1, len(massList))]
        for k in range(1, len(massList)):
            if self.type == 'stiffness':
                linked_stiffness = massList[k].linked_stiffness
            else:
                linked_stiffness = massList[k].linked_damping
            
            for l in range(1, len(massList)):
                stiffnessValue = ''
                if k == l:
                    for stiffness in linked_stiffness:
                        if stiffness:
                            stiffnessValue += '+{}'.format(stiffness.name)
                else:
                    if massList[l] in massList[k].linked_mass and linked_stiffness[massList[k].linked_mass.index(massList[l])]:
                        stiffnessValue += '-{}'.format(linked_stiffness[massList[k].linked_mass.index(massList[l])].name)

                self.matrix[k-1][l-1] = stiffnessValue

    
    def add_globalDamping(self, stiffnessMatrix):
        for i in range(0, len(stiffnessMatrix[0])):
            for j in range(0, len(stiffnessMatrix[0])):
                if stiffnessMatrix[i][j] != '':
                    if self.matrix[i][j] != '': 
                        self.matrix[i][j] += '+d({})'.format(stiffnessMatrix[i][j])
                    else:
                        self.matrix[i][j] += 'd({})'.format(stiffnessMatrix[i][j])



# ------------------------------------------------------ #
# ---------------- Class Matrix_Loading ---------------- #
# ------------------------------------------------------ #  
class Matrix_Loading(Matrix_Mass):
    def __init__(self):
        self.name = 'Loading_matrix'
        self.matrix = None


    def gen(self, massList):
        self.matrix = []
        for i in range(1, len(massList)):
            if massList[i].loading:
                self.matrix.append(massList[i].loading.value)
            else:
                self.matrix.append(0)


    def save(self, fileMatrix, massList):
        if self.matrix:
            fileMatrix.write('begin {} :\n'.format(self.name))
            
            for i in range(0, len(self.matrix)):
                fileMatrix.write('{0: >20};'.format(massList[i].name))
                fileMatrix.write('{0: >20}\n'.format(self.matrix[i]))                

            fileMatrix.write('end\n\n')



# -------------------------------------------------------------- #
# ---------------- Class LitteralMatrix_Loading ---------------- #
# -------------------------------------------------------------- #  
class LitteralMatrix_Loading(Matrix_Loading):
    def __init__(self):
        self.name = 'Loading_litteralMatrix'
        self.matrix = None


    def gen(self, massList):
        self.matrix = []
        for i in range(1, len(massList)):
            if massList[i].loading:
                self.matrix.append(massList[i].loading.name)
            else:
                self.matrix.append('0')



