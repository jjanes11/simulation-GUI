from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QGridLayout,
    QHBoxLayout,
    QMainWindow
)


class MainView(QMainWindow):
    """The main view of GUI."""
    def __init__(self, runcontroller, analyzecontroller):
        QMainWindow.__init__(self)
        self.runcontroller = runcontroller
        self.analyzecontroller = analyzecontroller
        self.configure_main_window()
        self.initUIelements()

    def configure_main_window(self):
        self.setWindowTitle("GUI")
        self.left = 0
        self.top = 0
        self.move(self.left, self.top)
        self.setFixedWidth(1500)
        self.setFixedHeight(1000)

    def initUIelements(self):
        tab_run = self.config_run_tab()
        tab_analyze = self.config_analyze_tab()
        centralTab = QTabWidget()
        centralTab.addTab(tab_run,"Run")
        centralTab.addTab(tab_analyze,"Analyze")
        mainLayout = QGridLayout()
        mainLayout.addWidget(centralTab)
        self.set_main_widget(mainLayout)

    def config_run_tab(self):
        #Simulate tab
        tabSimulate = QWidget()
        self.simview = self.runcontroller.view
        #self.simview
        simulateLayout = QHBoxLayout()
        simulateLayout.addWidget(self.simview)     
        #add to centraltab
        tabSimulate.setLayout(simulateLayout)
        return tabSimulate

    def config_analyze_tab(self):
        tabAnalyze = QWidget()
        analyzeLayout = QHBoxLayout()
        analyzeLayout.addWidget(self.analyzecontroller.view)
        tabAnalyze.setLayout(analyzeLayout)
        return tabAnalyze

    def set_main_widget(self, main_layout):
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)