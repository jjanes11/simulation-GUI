from .Abstract import Selector
from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog
)
from .decorators import wrap_widgets_in_layout
from typing import List, Dict

import settings


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
        #state = self.state()
        for observer in self.observers:
            observer.notification(self, "selected_table_changed")


#custom Widget for the input of simulation parameters
class InputParamSelector(Selector):
    def __init__(self, param_names: List[str]):
        QWidget.__init__(self)
        param_names = ["bias", "variance"]
        layout, self.param_boxes = self.__create_paramboxes(param_names)
        #print("boxes:", self.param_boxes)
        self.setLayout(layout)

    @wrap_widgets_in_layout
    def __create_paramboxes(self, param_names):
        param_boxes = []
        for param in param_names:
            #add newlayout as a row to the selectorLayout, check if input values of parameters should be integer (QSpinBox) or float (QDoubleSpinBox)
            if param in ["bias", "variance"]:
                self.box = QLabeledSpinBox()
                self.box.label.setText(f"{param}")
                self.box.spinbox.setMinimum(0)
                self.box.spinbox.setMaximum(2147483647)
            else:
                self.box = QLabeledDoubleSpinBox()
                self.box.label.setText(f"{param}")
                self.box.spinbox.setMinimum(0)
                self.box.spinbox.setMaximum(2147483647)
            self.box.spinbox.setValue(1)
            #self.spinbox.valueChanged.connect(self.spin_changed)
            param_boxes.append(self.box)
        return param_boxes

    def update(self, param_names):
        self.__create_paramboxes(param_names)

    def state(self) -> Dict[str, int]:
        '''returns current selections'''
        state = {}
        for box in self.param_boxes:
            state[box.label.text()] = box.spinbox.value()
        #print("Parameters currently selected:",state)
        #print("state:", state)
        return state


class QLabeledComboBox(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.combobox = QComboBox()
        setattr(self.combobox, "allItems", lambda: [self.combobox.itemText(i) for i in range(self.combobox.count())])
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)
        #layout.addStretch()
        self.setLayout(layout)


class QLabeledSpinBox(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.spinbox = QSpinBox()
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        #layout.addStretch()
        self.setLayout(layout)


class QLabeledDoubleSpinBox(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.label = QLabel()
        self.spinbox = QDoubleSpinBox()
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        #layout.addStretch()
        self.setLayout(layout)


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

    def notify(self):
        for observer in self.observers:
            observer.notification(self, "database_selected")

    def add_observer(self, observer: QWidget):
        self.observers.append(observer)