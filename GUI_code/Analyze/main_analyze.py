from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QTabWidget,
    QGridLayout,
    QHBoxLayout,
    QMainWindow
)

from AnalyzeModel import AnalyzeModel
from AnalyzeView import AnalyzeView
from AnalyzeController import AnalyzeController


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
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
        tab_analyze = self.construct_analyze_tab()
        centralTab = QTabWidget()
        centralTab.addTab(tab_analyze,"Analyze")
        mainLayout = QGridLayout()
        mainLayout.addWidget(centralTab)
        self.set_main_widget(mainLayout)

    def construct_analyze_tab(self):
        tabAnalyze = QWidget()
        model = AnalyzeModel("GUI_database.db")
        view = AnalyzeView()
        self.analyzecontroller = AnalyzeController(model, view)
        analyzeLayout = QHBoxLayout()
        analyzeLayout.addWidget(self.analyzecontroller.view)
        tabAnalyze.setLayout(analyzeLayout)
        return tabAnalyze

    def set_main_widget(self, main_layout):
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


if __name__ == "__main__" or True:
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())