from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QProcess
import settings
from .Abstract import Controller
import os
import uuid


class RunController(Controller):
    """Main controller for the GUI component for running simulations.
    
    Acts as a mediator between the RunView and RunModel classes.
    """
    def __init__(self, model, view):
        QWidget.__init__(self)
        self.model = model
        self.view = view
        self.config_model()
        self.config_view()

    def config_model(self):
        self.model.config()
        self.get_model_data()

    def config_view(self):
        self.view.controller = self
        self.view.init_UI(self.db, self.tables, self.param_names)

    def get_model_data(self):
        #get database
        self.db = self.model.db.split("/")[-1]
        #get database tables
        self.tables = self.model.get_database_tablenames()
        #select the first table for initialization of the view
        self.table = self.tables[0]
        #get parameter names that will be available for gui selection
        self.param_names= self.model.get_selectorNames(self.table)
    
    def notification(self, sender: QWidget, event: str):
        if event == "simview_created":
            SimController(self.model, self, sender.simview) 
        elif event == "selected_table_changed":
            self.table = sender.state()
        elif event == "database_selected":
            self.config_database(sender)

    def config_database(self, sender):
        self.model.db = os.path.join(settings.BASE_DIR, f'Databases/{sender.db}')
        self.update_selectors()

    def update_selectors(self):
        db_tables = self.model.get_database_tablenames()
        self.view.tableselector.update(db_tables)
        

#individual simulation process controller (start and terminate simulation buttons)
class SimController(Controller):
    """Simulation-specific controller for the GUI component for running simulations.
    
    Acts as a mediator between SimView and RunModel classes, although communication goes through the RunController.
    """
    def __init__(self, model, runcontroller, simview):
        QWidget.__init__(self)
        self.model = model
        self.runcontroller = runcontroller
        self.simview = simview
        self.simview.add_observer(self)

    def notification(self, sender: QWidget, event: str):
        if event == "start_button_pressed":
            self.start()
        elif event == "terminate_button_pressed":
            self.terminate(sender.message)

    def start(self):
        #get currently gui-selected params for the sim input
        selection = self.runcontroller.view.paramselector.state()
        #print("selection:", selection)
        inputParams = self.construct_inputparam_string(selection)
        #set simulation script to execute
        simscript_name = "simulation"
        #check if simulation script exists in path
        sim_path = f"{settings.BASE_DIR}/Simulation/"
        if os.path.isfile(f"{sim_path}{simscript_name}"):
            self.start_simulation_process(sim_path, simscript_name, inputParams)
        else:
            print(f"Error: No simulation file named {simscript_name} in the directory {settings.BASE_DIR}/Simulation!")

    def construct_inputparam_string(self, selection):
        inputParams = ""
        for param, value in selection.items():
            if value>=0:
                inputParams += "--{}={} ".format(param, value)
        inputParams += "--{}={} ".format("file_name", uuid.uuid4().hex)
        #print("inputparams:", inputParams, type(inputParams), inputParams.split("="))
        return inputParams

    def start_simulation_process(self, sim_path, simscript_name, inputParams):
            execute_sim_command = f"{sim_path}{simscript_name} {inputParams}"
            print("command:", execute_sim_command)
            #print(execute_sim_command)
            self.simProcess = QProcess()
            self.simProcess.readyReadStandardOutput.connect(self.updateProgressInfo)
            self.simProcess.readyReadStandardError.connect(lambda: self.simview.simMonitor.simErrLogDisplay.append(str(self.simProcess.readAllStandardError().data().decode('utf-8'))))
            #start the process
            self.simProcess.start(execute_sim_command)
            pid = self.simProcess.pid()
            #running_label = "Simulation running. PID: {}".format(pid)
            processState = {QProcess.NotRunning: "No simulations running.",
                            QProcess.Starting: "Simulation starting.",
                            QProcess.Running: "Simulation running. PID: {}".format(pid)}
            self.simProcess.stateChanged.connect(lambda: self.simview.simMonitor.simStatus.setText(processState[self.simProcess.state()]))
            self.simProcess.errorOccurred.connect(lambda: print("Error of type", self.simProcess.error()))
            self.simProcess.finished.connect(lambda: self.simFinished(inputParams))

    def updateProgressInfo(self):
        #get stdout and transform it to list of strings for convenience
        stdout=str(self.simProcess.readAllStandardOutput().data().decode('utf-8').split())
        self.simview.simMonitor.simErrLogDisplay.setText(stdout)

    def simFinished(self, inputparams):
        if not self.simProcess.exitStatus():
            print("The simulation process exited normally.")
            #self.simview.simMonitor.simProgressBar.reset()
            #self.simview.simMonitor.simEstimatedTime.setText("")
            self.model.save(inputparams, self.runcontroller.table)
        else:
            print("The simulation process crashed.")

    def terminate(self, message: str):
        self.simProcess.kill()
        #self.simview.simMonitor.simProgressBar.reset()
        #self.simview.simMonitor.simEstimatedTime.setText("")
        print(message)
