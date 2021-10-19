from abc import ABCMeta, abstractmethod
from typing import List, Dict
import settings

from sip import wrappertype as pyqtWrapperType
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QFileDialog,
    QPushButton
)
from .decorators import wrap_widgets_in_layout

class FinalMeta(pyqtWrapperType, ABCMeta):
    pass


class Selector(QWidget, metaclass=FinalMeta):
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def state(self):
        pass

    @abstractmethod
    def add_observer(self):
        pass

    @abstractmethod
    def notify(self):
        pass


class TableSelector(Selector):
    def __init__(self, tables: List[str]) -> None:
        QWidget.__init__(self)
        self.observers=[]
        layout, widget = self.__create_widgets(tables)
        self.setLayout(layout)

    @wrap_widgets_in_layout
    def __create_widgets(self, tables: List[str]) -> List[QComboBox]:
        widgets = []
        self.box = QLabeledComboBox()
        self.box.label.setText("database table")
        self.box.combobox.activated.connect(self.notify)
        for _ in tables:
            self.box.combobox.addItem(f"{_}")
        widgets.append(self.box)
        return widgets
    
    def update(self, tables: List[str]):
        self.box.combobox.clear()
        for table in tables:
            self.box.combobox.addItem(table)

    def state(self) -> List[str]:
        state = self.box.combobox.currentText()
        print("Table currently selected:", state)
        return state

    def add_observer(self, observer: QWidget):
        self.observers.append(observer)

    def notify(self):
        state = self.state()
        for observer in self.observers:
            observer.notify("state of the table_selector changed", state)


class QLabeledComboBox(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.combobox = QComboBox()
        setattr(self.combobox, "allItems", lambda: [self.combobox.itemText(i) for i in range(self.combobox.count())])
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)
        layout.addStretch()
        self.setLayout(layout)


class ParamSelector(Selector):
    def __init__(self, param_values: Dict[str, List[str]]) -> None:
        QWidget.__init__(self)
        self.observers=[]
        # param_values: {param_name : [distinct_param_values]}
        # param_values = {
        #     "bias" : ["1","2","3","4","5","6"], 
        #     "variance" : ["6","5","4","3","2","1"],
        #     "file_name" : ["file1", "file2", "file3", "file4", "file5", "file6"]}
        layout, self.param_boxes = self.__create_widgets(param_values)
        self.setLayout(layout)
        self.update(param_values)

    @wrap_widgets_in_layout
    def __create_widgets(self, param_values: Dict[str, List[str]]) -> List[QLabeledComboBox]:
        param_boxes = []
        for _ in param_values:
            box = QLabeledComboBox()
            box.combobox.activated.connect(self.notify)
            param_boxes.append(box)
        return param_boxes

    def update(self, param_values: Dict[str, List[str]], selection = None,) -> None:
        #print("selection in update:", selection)
        print("param_values:", param_values)
        if len(self.param_boxes) == len(param_values):
            i=0
            for key in param_values:
                #print(param_boxes[i], param_values[key])
                self.param_boxes[i].label.setText(f"{key}")
                self.param_boxes[i].combobox.clear()
                self.param_boxes[i].combobox.addItem("all values")
                self.param_boxes[i].combobox.addItem("combination of values")
                self.param_boxes[i].combobox.addItems(param_values[key])
                if selection != None:
                    # boxItems = self.param_boxes[i].combobox.allItems()
                    # #print("combobox values:",boxItems)
                    # if selection[key] not in boxItems:
                    self.param_boxes[i].combobox.addItem(selection[key])
                    self.param_boxes[i].combobox.setCurrentText(selection[key])
                i+=1
        else:
            print("Number of selectors does not mach the number of parameters!")


    def state(self) -> Dict[str, List[str]]:
        '''returns current selections'''
        state = {}
        for box in self.param_boxes:
            state[box.label.text()] = box.combobox.currentText()
        #print("Parameters currently selected:",state)
        print("state:", state)
        return state

    def add_observer(self, observer: QWidget):
        self.observers.append(observer)

    def notify(self):
        state = self.state()
        for observer in self.observers:
            observer.notify("state of the param_selector changed", state)


class DatabaseSelector(QWidget):
    def __init__(self, db):
        QWidget.__init__(self)
        self.observers = []
        self.db = db
        layout = QVBoxLayout()
        button = QPushButton("Select another database")
        button.clicked.connect(self.handle)
        self.db_label = QLabel(f"Database: {self.db}")
        layout.addWidget(button)
        layout.addWidget(self.db_label)
        self.setLayout(layout)
        
    def handle(self):
        self.filename, filter = QFileDialog.getOpenFileName(self, 'Open file', f"{settings.BASE_DIR}/Databases", 'Kicad PCB Files (*.db)')
        if self.filename:
            self.db = self.filename.split("/")[-1]
            self.db_label.setText(f"Database: {self.db}")
            self.notify()

    def state(self) -> List[str]:
        state = self.box.combobox.currentText()
        #print("Database currently selected:", state)
        return state

    def notify(self):
        for observer in self.observers:
            observer.notification(self, "database_selected")

    def add_observer(self, observer: QWidget):
        self.observers.append(observer)


