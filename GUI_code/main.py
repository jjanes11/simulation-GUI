from PyQt5.QtWidgets import QApplication

from Run.RunModel import RunModel
from Run.RunView import RunView
from Run.RunController import RunController

from Analyze.AnalyzeModel import AnalyzeModel
from Analyze.AnalyzeView import AnalyzeView
from Analyze.AnalyzeController import AnalyzeController

from MainView import MainView


if __name__ == "__main__" or True:
    import sys

    app = QApplication(sys.argv)
    runcontroller = RunController(RunModel(), RunView())
    analyzecontroller = AnalyzeController(AnalyzeModel(), AnalyzeView())
    mainWin = MainView(runcontroller, analyzecontroller)
    mainWin.show()
    sys.exit(app.exec_())