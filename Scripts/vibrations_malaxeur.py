#!/usr/bin/python3.5

# ----------------------------------------------------------------
#       Import all the libraries for exactra functions      
# ----------------------------------------------------------------
# General librarie for operating system parameters
import sys
# General librarie for Graphic User Interface
import PyQt5.QtWidgets as qtw 

# Custom libraries for Graphical User Interfaces (see file vibrations_resultsWindow.py)
from vibrations_resultsWindow import ResultsWindows



# ----------------------------------------------------------------
#       Function : main     
# ----------------------------------------------------------------
def main():
    '''
    Function : main
    Description : Create an application and open the GUI for the project
    Parameters : None
    Returns : None
    '''
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    _ = ResultsWindows(rect.width(), rect.height())
    sys.exit(app.exec_())



# ----------------------------------------------------------------
#       Main part      
# ----------------------------------------------------------------
if __name__ == '__main__':
    main()

