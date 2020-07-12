
from abc import ABC, abstractmethod
from math import pi

# --------------------------------------------- #
# ---------------- Class Shaft ---------------- #
# --------------------------------------------- #   
class Shaft:
    def __init__(self, name, ratio, connectedShaft=None):
        self.name = name
        self.shaftList = []
        self.massList = []
        self.stiffnessList = []
        self.dampingList = []
        if connectedShaft:
            self.ratio = ratio * connectedShaft.ratio
            connectedShaft.shaftList.append(self)
        else:
            self.ratio = ratio

    def get_minMass(self):
        if len(self.massList) == 0:
            minMass = None
        else:
            minMass = self.massList[0].value if self.massList[0].name != 'frame' else self.massList[1].value
            # print(self.listDict['Mass_list'][1].name, self.listDict['Mass_list'][1].value)
            # print(self.name, self.massList)
            for i in range(1, len(self.massList)):
                if type(self.massList[i]) in [Mass, Inertia_Cylinder, EquivalentMass, EquivalentInertia_Cylinder] and self.massList[i].value < minMass:
                    minMass = self.massList[i].value 
                    # print(self.listDict['Mass_list'][i].name, self.listDict['Mass_list'][i].value)
        
        return minMass



# -------------------------------------------- #
# ---------------- Class Mass ---------------- #
# -------------------------------------------- #   
class Mass:
    def __init__(self, name, value, shaft):
        self.name = name 
        self.shaft = shaft
        self.shaft.massList.append(self)
        self.value = value * (self.shaft.ratio)**2
        self.linked_mass = []
        self.linked_stiffness = []
        self.linked_damping = []
        self.loading = None
        self.addedMass = []
        # print(self.name, self.value)


    @property
    def totalValue(self):
        total = self.value
        for mass in self.addedMass:
            total += mass.value
        return total


    def add_link(self, mass, stiffness=None, damping=None):
        if mass in self.linked_mass:
            if stiffness:
                self.linked_stiffness[self.linked_mass.index(mass)] = stiffness
            if damping:
                self.linked_damping[self.linked_mass.index(mass)] = damping
        else:
            self.linked_mass.append(mass)
            self.linked_stiffness.append(stiffness)
            self.linked_damping.append(damping)


    def read(self, dictClass):
        self.name = dictClass['name']
        self.value = float(dictClass['value'])



# -------------------------------------------------------- #
# ---------------- Class Discretized_Mass ---------------- #
# -------------------------------------------------------- #   
class Discretized_Mass(Mass):
    def __init__(self, name, value, shaft):
        super().__init__(name, value, shaft)



# -------------------------------------------------------- #
# ---------------- Class Inertia_Cylinder ---------------- #
# -------------------------------------------------------- #   
class Inertia_Cylinder(Mass):
    def __init__(self, name, d, l, rho, shaft):
        self.d = d
        self.l = l
        self.rho = rho
        value = pi*d**4*l/32*rho
        super().__init__(name, value, shaft)



# ------------------------------------------------------ #
# ---------------- Class EquivalentMass ---------------- #
# ------------------------------------------------------ #   
class EquivalentMass(Mass):
    def __init__(self, name, value, shaft, mass):
        super(EquivalentMass, self).__init__(name, value, shaft)
        self.equivalentMass = mass
        mass.addedMass.append(self)


    def add_link(self, mass, stiffness=None, damping=None):
        self.equivalentMass.add_link(mass, stiffness=stiffness, damping=damping)



# ----------------------------------------------------------------- #
# ---------------- Class DiscretizedEquivalentMass ---------------- #
# ----------------------------------------------------------------- #   
class DiscretizedEquivalentMass(EquivalentMass):
    def __init__(self, name, value, shaft, mass):
        super().__init__(name, value, shaft, mass)



# ------------------------------------------------------------------ #
# ---------------- Class EquivalentInertia_Cylinder ---------------- #
# ------------------------------------------------------------------ #   
class EquivalentInertia_Cylinder(EquivalentMass):
    def __init__(self, name, d, l, rho, shaft, mass):
        self.d = d
        self.l = l
        self.rho = rho
        value = pi*d**4*l/32*rho
        super().__init__(name, value, shaft, mass)



# ------------------------------------------------- #
# ---------------- Class Stiffness ---------------- #
# ------------------------------------------------- #   
class Stiffness(ABC):
    def __init__(self, name, value, shaft, mass1, mass2):
        # print(name)
        # print('mass1:', mass1.name, 'mass2:', mass2.name)
        self.name = name 
        self.shaft = shaft
        if type(mass1) in [EquivalentMass, EquivalentInertia_Cylinder]:
            self.mass1 = mass1.equivalentMass
        elif type(mass1) in [StiffnessDiscretized, StiffnessDiscretized_Shaft]:
            if mass1.mass2 and mass1.mass2.name != 'frame':
                self.mass1 = mass1.mass2
            else:
                self.mass1 = mass1.massList[-1]
        else:
            self.mass1 = mass1
        if type(mass2) in [EquivalentMass, EquivalentInertia_Cylinder]:
            # print('mass2:', mass2.name, 'mass2.equivalentMass:', mass2.equivalentMass.name)
            self.mass2 = mass2.equivalentMass
        elif type(mass2) in [StiffnessDiscretized, StiffnessDiscretized_Shaft]:
            if mass2.mass1 and mass2.mass1.name != 'frame':
                self.mass2 = mass2.mass1
            else:
                self.mass2 = mass2.massList[0]
        else:
            self.mass2 = mass2
        # print('self.mass1:', self.mass1.name, 'self.mass2:', self.mass2.name)
        if mass1 and mass2:
            self.update_value(value)


    def update_value(self, value):
        self.value = value * (self.shaft.ratio)**2
        self.mass1.add_link(self.mass2, stiffness=self)
        self.mass2.add_link(self.mass1, stiffness=self)


    def read(self, dictClass, massList):
        self.name = dictClass['name']
        for mass in massList:
            if mass.name == dictClass['mass1']:
                self.mass1 = mass
            if mass.name == dictClass['mass2']:
                self.mass2 = mass
        self.update_value(float(dictClass['value']))



# ---------------------------------------------------------- #
# ---------------- Class Stiffness_Cylinder ---------------- #
# ---------------------------------------------------------- #   
class Stiffness_Cylinder(Stiffness):
    def __init__(self, name, d, l, g, shaft, mass1, mass2):
        self.d = d
        self.l = l
        self.g = g
        value = pi*d**4*g/(32*l)
        super().__init__(name, value, shaft, mass1, mass2)




# ------------------------------------------------------------ #
# ---------------- Class StiffnessDiscretized ---------------- #
# ------------------------------------------------------------ #   
class StiffnessDiscretized(ABC):
    def __init__(self, name, massValue, stiffnessValue, nbDiscretization, shaft, mass1=None, mass2=None, minMass=None):
        self.name = name 
        self.shaft = shaft
        self.massValue = massValue * (self.shaft.ratio)**2
        self.sitffnessValue = stiffnessValue * (self.shaft.ratio)**2
        # print(minMass)
        if nbDiscretization:
            if type(nbDiscretization) == int and nbDiscretization >= 1:
                self.nbDiscretization = nbDiscretization
            else:
                raise ValueError('nbDiscretization must be an integer >= 1')
        # elif minMass:
        #     self.nbDiscretization = int(massValue/minMass) + 1
        else:
            minMass = self.shaft.get_minMass()
            if minMass:
                self.nbDiscretization = int(self.massValue/minMass) + 1
            else:
                self.nbDiscretization = 1
            # raise Exception('no nbDiscretization and minMass define')
        # print('nb dis', self.nbDiscretization, self.name, self.massValue, minMass)
        if type(mass1) in [StiffnessDiscretized, StiffnessDiscretized_Shaft]:
            if mass1.mass2 and mass1.mass2.name != 'frame':
                self.mass1 = mass1.mass2
            else:
                self.mass1 = mass1.massList[-1]
        else:
            self.mass1 = mass1
        if type(mass2) in [StiffnessDiscretized, StiffnessDiscretized_Shaft]:
            if mass2.mass1 and mass2.mass1.name != 'frame':
                self.mass2 = mass2.mass1
            else:
                self.mass2 = mass2.massList[0]
        else:
            self.mass2 = mass2
        self.massList = []
        self.equivalentMassList = []
        self.stiffnessList = []
        if self.nbDiscretization:
            self.gen_lists()
        

    def gen_lists(self):
        massDis = self.massValue/self.nbDiscretization
        if self.mass1 and self.mass1.name == 'frame' and self.mass2 and self.mass2.name == 'frame':
            stiffDis = self.sitffnessValue*(self.nbDiscretization+2)
        elif (self.mass1 and self.mass1.name == 'frame') or (self.mass2 and self.mass2.name == 'frame'):
            stiffDis = self.sitffnessValue*(self.nbDiscretization+1)
        else:
            stiffDis = self.sitffnessValue*self.nbDiscretization

        if not self.mass1 or self.mass1.name == 'frame':
            startMass = Discretized_Mass('{}.0'.format(self.name), massDis/2, self.shaft)
            self.massList.append(startMass)
        else:
            startMass = DiscretizedEquivalentMass('{}.0'.format(self.name), massDis/2, self.shaft, self.mass1)
            self.equivalentMassList.append(startMass)
        for i in range(1, self.nbDiscretization):
            mass = Discretized_Mass('{}.{}'.format(self.name, i), massDis, self.shaft)
            self.massList.append(mass)
        if not self.mass2 or self.mass2.name == 'frame':
            endMass = Discretized_Mass('{}.{}'.format(self.name, self.nbDiscretization), massDis/2, self.shaft)
            self.massList.append(endMass)
        else:
            endMass = DiscretizedEquivalentMass('{}.{}'.format(self.name, self.nbDiscretization), massDis/2, self.shaft, self.mass2)
            self.equivalentMassList.append(endMass)
        

        if self.nbDiscretization < 1:
            raise ValueError('nbDiscretization must be an integer superior to 1')
        elif self.nbDiscretization == 1:
            i = 0
            if self.mass1 and self.mass1.name == 'frame':
                k = Stiffness('{}.{}'.format(self.name, i), stiffDis, self.shaft, self.mass1, startMass)
                self.stiffnessList.append(k)
                i += 1

            # print(startMass.name)
            k = Stiffness('{}.{}'.format(self.name, i), stiffDis, self.shaft, startMass, endMass)
            self.stiffnessList.append(k)
            i += 1

            if self.mass2 and self.mass2.name == 'frame':
                k = Stiffness('{}.{}'.format(self.name, i), stiffDis, self.shaft, endMass, self.mass2)
                self.stiffnessList.append(k)
            
        else:
            if self.mass1:
                if self.mass1.name == 'frame':
                    k = Stiffness('{}.0'.format(self.name), stiffDis, self.shaft, self.mass1, startMass)
                else:
                    k = Stiffness('{}.0'.format(self.name), stiffDis, self.shaft, self.mass1, self.massList[0])
                self.stiffnessList.append(k)
            
            for i in range(0, len(self.massList)-1):
                k = Stiffness('{}.{}'.format(self.name, i), stiffDis, self.shaft, self.massList[i], self.massList[i+1])
                self.stiffnessList.append(k)
            
            if self.mass2:
                if self.mass2.name == 'frame':
                    k = Stiffness('{}.0'.format(self.name), stiffDis, self.shaft, endMass, self.mass2)
                else:
                    k = Stiffness('{}.0'.format(self.name), stiffDis, self.shaft, self.massList[-1], self.mass2)
                self.stiffnessList.append(k)
            

    def get_lists(self):
        # if (not self.mass1 and not self.mass2) or (self.mass1 and self.mass2 and self.mass1.name == 'frame' and self.mass2.name == 'frame'):
        #     massList = self.massList
        # elif (self.mass1 and self.mass2 and self.mass2.name == 'frame') or (self.mass1 and self.mass1.name != 'frame'):
        #     massList = self.massList[1:]
        # elif (self.mass1 and self.mass2 and self.mass1.name == 'frame') or (self.mass2 and self.mass2.name != 'frame'):
        #     massList = self.massList[:-1]
        # else:
        #     massList = self.massList[1:-1]

        # print(massList[0].name)
        # print(self.stiffnessList[1].name)
        
        return self.massList, self.equivalentMassList, self.stiffnessList


    def read(self, dictClass, massList, stiffnessList):
        self.name = dictClass['name']
        self.nbDiscretization = dictClass['nbDiscretization']
        self.sitffnessValue = dictClass['sitffnessValue']
        self.massValue = dictClass['massValue']
        for mass in massList:
            if mass.name == dictClass['mass1']:
                self.mass1 = mass
            if mass.name == dictClass['mass2']:
                self.mass2 = mass
            for massName in dictClass['massList'][2:-3].split(', '):
                if mass.name == massName:
                    self.massList.append(mass)

        # print(self.massList)

        for stiffness in stiffnessList:
            for stiffnessName in dictClass['stiffnessList'][2:-3].split(', '):
                if stiffness.name == stiffnessName:
                    self.stiffnessList.append(stiffness)



# ------------------------------------------------------------------ #
# ---------------- Class StiffnessDiscretized_Shaft ---------------- #
# ------------------------------------------------------------------ #   
class StiffnessDiscretized_Shaft(StiffnessDiscretized):
    def __init__(self, name, d, l, g, rho, nbDiscretization, shaft, mass1=None, mass2=None, minMass=None):
        stiffness = pi*d**4*g/(32*l)
        inertia = pi*d**4*l/32*rho
        super().__init__(name, inertia, stiffness, nbDiscretization, shaft, mass1=mass1, mass2=mass2, minMass=minMass)



# ----------------------------------------------- #
# ---------------- Class Damping ---------------- #
# ----------------------------------------------- #   
class Damping(Stiffness):
    def __init__(self, name, value, shaft, mass1, mass2):
        self.name = name 
        self.shaft = shaft
        self.mass1 = mass1
        self.mass2 = mass2
        if mass1 and mass2:
            self.update_value(value)


    def update_value(self, value):
        self.value = value * (self.shaft.ratio)**2
        self.mass1.add_link(self.mass2, damping=self)
        self.mass2.add_link(self.mass1, damping=self)



# ----------------------------------------------- #
# ---------------- Class Loading ---------------- #
# ----------------------------------------------- #   
class Loading:
    def __init__(self, name, value, mass):
        self.name = name 
        self.mass = mass
        self.value = value * (self.mass.shaft.ratio)**2
        if mass:
            self.mass.loading = self


    def read(self, dictClass, massList):
        self.name = dictClass['name']
        for mass in massList:
            if mass.name == dictClass['mass']:
                self.mass = mass
        self.value = float(dictClass['value'])
        self.mass.loading = self