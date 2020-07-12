
import sys
import os
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


# ----------------------------------------------------- #
# ---------------- Popup_Dialog_Single ---------------- #
# ----------------------------------------------------- #
class Popup_Dialog_Single(qtw.QDialog):
    def __init__(self, title, buttonText, recWidth=None, recHeight=None):
        super(Popup_Dialog_Single, self).__init__()
        self.setWindowTitle(title)

        # width for a lineEdit = 125; height = 28
        self.width, self.height = 100, 48
        self.recWidth, self.recHeight = recWidth, recHeight

        self.valueDict = {}
        self.lineDict = {}
        self.lineCount = 0
        self.widthUnit = 0
        self.pressed = False

        self.button = qtw.QPushButton(buttonText, self)
        self.button.clicked.connect(self.add_value)
        self.button.move(10, 10)

        self.update_position()
        # self.setGeometry(50, 50, self.width, self.height)


    def add_line(self, valueName, valueUnit=''):
        self.valueDict[valueName] = None
        self.lineDict['{}'.format(self.lineCount)] = []
        labelName = qtw.QLabel(valueName, self)
        self.lineDict['{}'.format(self.lineCount)].append(labelName)
        labelEqual = qtw.QLabel('=', self)
        self.lineDict['{}'.format(self.lineCount)].append(labelEqual)

        widthText = 0
        for char in valueName:
            if char == char.lower():
                widthText += 7
            else:
                widthText += 9

        widthUnit = 0
        for char in valueUnit:
            if char == char.lower():
                widthUnit += 7
            else:
                widthUnit += 9
        if widthUnit > self.widthUnit:
            self.widthUnit = widthUnit

        width = 10 + widthText + 10 + 10 + 10 + 125 + 10 + self.widthUnit + 10
        if width > self.width:
            self.width = width
        
        self.lineCount += 1
        self.height += 38


    def add_lineEdit(self, valueName, valueUnit=''):
        self.add_line(valueName, valueUnit=valueUnit)
        
        lineEdit = qtw.QLineEdit('', self)
        self.lineDict['{}'.format(self.lineCount-1)].append(lineEdit)
        labelUnit = qtw.QLabel(valueUnit, self)
        self.lineDict['{}'.format(self.lineCount-1)].append(labelUnit)

        self.update_position()
        

    def add_comboBox(self, valueName, valuelist):
        self.add_line(valueName, valueUnit='')
        
        comboBox = qtw.QComboBox(self)
        comboBox.addItems(valuelist)
        self.lineDict['{}'.format(self.lineCount-1)].append(comboBox)

        self.update_position()
        

    def update_position(self):
        if not self.recWidth:
            left = 0
        else:
            left = (self.recWidth - self.width)/2
        if not self.recHeight:
            top = 0
        else:
            top = (self.recHeight - self.height)/2
        
        self.setGeometry(left, top, self.width, self.height)
        i = 0
        for i in range(0, self.lineCount):
            self.lineDict['{}'.format(i)][0].move(10, 15 + 38*i)
            self.lineDict['{}'.format(i)][1].move(self.width - 165 - self.widthUnit , 15 + 38*i)
            self.lineDict['{}'.format(i)][2].move(self.width - 145 - self.widthUnit , 10 + 38*i)
            if len(self.lineDict['{}'.format(i)]) == 4:
                self.lineDict['{}'.format(i)][3].move(self.width - 10 - self.widthUnit , 15 + 38*i)

        i += 1
        self.button.move(10 + (self.width-100)/2, 10 + 38*i)


    def add_value(self):
        for i in range(0, self.lineCount):
            if type(self.lineDict['{}'.format(i)][2]) == qtw.QLineEdit:
                value = self.lineDict['{}'.format(i)][2].text()
            elif type(self.lineDict['{}'.format(i)][2]) == qtw.QComboBox:
                value = self.lineDict['{}'.format(i)][2].currentIndex()
            else:
                raise TypeError('undified type {} for self.lineDict["{}"][2]'.format(type(self.lineDict['{}'.format(i)][2]), i))
            
            name = self.lineDict['{}'.format(i)][0].text()
            self.valueDict[name] = value

        self.pressed = True
        self.close()


    def get_value(self):
        if self.pressed:
            return self.valueDict
        else:
            return 'None'



# ---------------------------------------------------- #
# ---------------- Popup_Dialog_Multi ---------------- #
# ---------------------------------------------------- #
class Popup_Dialog_Multi(Popup_Dialog_Single):
    def __init__(self, title, buttonText, recWidth=None, recHeight=None):
        super(Popup_Dialog_Multi, self).__init__(title, buttonText, recWidth=recWidth, recHeight=recHeight)


    def add_line(self, valueName, valueUnit=''):
        super(Popup_Dialog_Multi, self).add_line(valueName, valueUnit='')
        self.valueDict[valueName] = []


    def add_value(self):
        for i in range(0, self.lineCount):
            if type(self.lineDict['{}'.format(i)][2]) == qtw.QLineEdit:
                value = self.lineDict['{}'.format(i)][2].text()
            elif type(self.lineDict['{}'.format(i)][2]) == qtw.QComboBox:
                value = self.lineDict['{}'.format(i)][2].currentIndex()
            else:
                raise TypeError('undified type {} for self.lineDict["{}"][2]'.format(type(self.lineDict['{}'.format(i)][2]), i))
            
            name = self.lineDict['{}'.format(i)][0].text()
            self.valueDict[name].append(value)

        self.pressed = True
        


# ----------------------------------------------------- #
# ---------------- Popup_Dialog_Remove ---------------- #
# ----------------------------------------------------- #
class Popup_Dialog_Remove(Popup_Dialog_Single):
    def __init__(self, title, valueName, valuelist, recWidth=None, recHeight=None):
        super(Popup_Dialog_Remove, self).__init__(title, 'remove', recWidth=recWidth, recHeight=recHeight)
        self.valueName = valueName

        self.add_comboBox(valueName, valuelist)


    def get_value(self):
        if self.pressed:
            return self.valueDict[self.valueName]
        else:
            return 'None'



# -------------------------------------------- #
# ---------------- Popup_Info ---------------- #
# -------------------------------------------- #
class Popup_Info(qtw.QWidget):
    def __init__(self, text, recWidth=None, recHeight=None):
        super(Popup_Info, self).__init__()
        # width for 1 char = 9 (capital) or 7 (low); height for 1 char = 19
        # width for the button = 80; height for the button = 28
        self.width, self.height = 100, 77

        label = qtw.QLabel(text, self)
        buttonOk = qtw.QPushButton('OK', self)
        buttonOk.clicked.connect(self.close_window)
        
        self.widthText = 0
        for char in text:
            if char == char.lower():
                self.widthText += 7
            else:
                self.widthText += 9

        if self.widthText > 100:
            self.width = self.widthText + 20
        
        label.move(10 + (self.width - self.widthText -20)/2, 10)
        buttonOk.move(10 + (self.width - 100)/2, 39)

        if not recWidth:
            left = 0
        else:
            left = (recWidth - self.width)/2

        if not recHeight:
            top = 0
        else:
            top = (recHeight - self.height)/2

        self.setWindowTitle('Info')
        self.setGeometry(left, top, self.width, self.height)

        self.show()

    def close_window(self):
        self.close()
    