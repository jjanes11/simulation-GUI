from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QProgressBar,
    QLabel,
    QLineEdit,
)

#custom Widget for simulation monitoring (status, output, progress, estimated time to end...)
class SimMonitor(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)
        self.init_UI(name)

    def init_UI(self, name):
        self.simMonitorLayout = QVBoxLayout()
        self.simMonitorLayout.setContentsMargins(0,0,0,0)
        self.config_simname_label(name)
        self.config_display()
        self.config_status_label()
        #self.config_directory_label()
        #self.config_progress_bar()
        #self.config_estimated_time_label()
        self.setLayout(self.simMonitorLayout)

    def config_simname_label(self, name):
        self.simNameLabel = QLabel()
        self.simNameLabel.setText(name)
        self.simMonitorLayout.addWidget(self.simNameLabel)

    def config_display(self):
        ##simulation stdout and stderr (error/log) displays
        self.simErrLogDisplay = QTextEdit()
        self.simErrLogDisplay.setReadOnly(True)
        self.simErrLogDisplay.setText("Stderr (errors, log and info)\n")
        self.simErrLogDisplay.setMaximumHeight(200)
        self.simMonitorLayout.addWidget(self.simErrLogDisplay)

    def config_status_label(self):
        #simulation status label
        self.simStatus = QLabel()
        self.simStatus.setText("No simulations running.")
        self.simMonitorLayout.addWidget(self.simStatus)

    def config_directory_label(self):
        self.simDirectory = QLineEdit()
        self.simDirectory.setReadOnly(True)
        self.simMonitorLayout.addWidget(self.simDirectory)
    
    def config_progress_bar(self):
        self.simProgressBar = QProgressBar()
        self.simMonitorLayout.addWidget(self.simProgressBar)

    def config_estimated_time_label(self):
        self.simEstimatedTime = QLabel()
        self.simMonitorLayout.addWidget(self.simEstimatedTime)
        

#start and terminate simulation buttons
class StartTerminateButtons(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)
        self.name = name
        self.observers = []
        self.init_UI(name)

    def init_UI(self, name):
        simControllerLayout = QHBoxLayout()
        simControllerLayout.setSpacing(30)
        simControllerLayout.setContentsMargins(0,0,0,0)
        self.startButton = self.create_start_button(name)
        simControllerLayout.addWidget(self.startButton)
        self.terminateButton = self.create_terminate_button(name)
        simControllerLayout.addWidget(self.terminateButton)
        self.setLayout(simControllerLayout)
    
    def create_start_button(self, name):
        startButton = QPushButton("Start {}!".format(name))
        startButton.clicked.connect(self.startButtonHandler)
        return startButton

    def create_terminate_button(self, name):
        terminateButton = QPushButton("Terminate {}!".format(name))
        terminateButton.clicked.connect(self.terminateButtonHandler)
        terminateButton.setEnabled(False)
        return terminateButton

    def startButtonHandler(self):
        for observer in self.observers:
            self.startButton.setEnabled(False)
            self.terminateButton.setEnabled(True)
            observer.notification(sender = self, event = "start_button_pressed")

    def terminateButtonHandler(self):
        for observer in self.observers:
            self.terminateButton.setEnabled(False)
            self.startButton.setEnabled(True)
            self.message = "Terminated {}.".format(self.name)
            observer.notification(sender = self, event = "terminate_button_pressed")

    def add_observer(self, observer):
        self.observers.append(observer)


#custom Widget for simulation controll and monitoring (combining SimMonitor and StartTerminateButtons)
class SimView(QWidget):
    def __init__(self, name):
        QWidget.__init__(self)
        self.init_UI(name)

    def init_UI(self, name):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10,10,10,10)
        #simMonitor
        self.simMonitor = SimMonitor(name)
        layout.addWidget(self.simMonitor)
        #start and terminate simulation buttons
        self.start_term_buttons = StartTerminateButtons(name)
        layout.addWidget(self.start_term_buttons)
        self.setLayout(layout)

    def add_observer(self, observer):
        self.start_term_buttons.add_observer(observer)
