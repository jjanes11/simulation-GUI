from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QTabWidget,
    QGridLayout,
    QHBoxLayout,
    QMainWindow
)

from RunModel import RunModel
from RunView import *
from RunController import RunController

'''
Main window of the app.
'''
class MainWindow(QMainWindow):
    '''
    the analyzeLayout (window) consists of the the selectorLayout and the plotLayout
    selectorLayout holds the ComboBoxes for selecting simTables and simParams and different plotting options
    plotLayout holds the  canvas and the toolbar for modifying the plot (zoom, coordinates, save...)
    '''

    '''
    current implementation assumes that the database table with the simulation input paramteres as column names
    already exists and pram names can be read from it.
    TO be 
    With diferent simulation options corresponding to different physical models, it would be useful that each model
    has its own database table (potentially different number of input parameters and different role of parameters in the model).
    Alternatively, all models could be in in the same table, but one would have to deal with possible  inconsistent number and kind of parameters,
    and therefore inconsistent db_table columns.
    The model and the corresponding db_table would be given as input arguments to the simulation script (executed from the gui).
    As different models can have different params, the number and/or order of input args could also be modified (in the c++ script as well as in gui selectors).
    If the db_table corresponding to the model doesn't exist it should be created, as soon as I choose a simulation model option.
    '''

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.init_UI()

    def init_UI(self):
        self.config_main_window()
        self.mainLayout = QGridLayout()
        self.config_central_tab()
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    def config_main_window(self):
        self.setWindowTitle("GUI")
        self.left = 0
        self.top = 0
        self.move(self.left, self.top)
        self.setFixedWidth(1500)
        self.setFixedHeight(1000)

    def config_central_tab(self):
        self.centralTab = QTabWidget()
        tabSimulate = self.config_simulation_tab()
        self.centralTab.addTab(tabSimulate,"Simulate")
        self.mainLayout.addWidget(self.centralTab)

    def config_simulation_tab(self):
        #Simulate tab
        tabSimulate = QWidget()
        self.simview = self.controller.view
        #self.simview
        simulateLayout = QHBoxLayout()
        simulateLayout.addWidget(self.simview)     
        #add to centraltab
        tabSimulate.setLayout(simulateLayout)
        return tabSimulate


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    controller = RunController(RunModel(), RunView())
    mainWin = MainWindow(controller)
    mainWin.show()
    sys.exit(app.exec_())

