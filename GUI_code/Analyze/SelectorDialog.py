from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QFrame,
    QDialog, QDialogButtonBox
)

class PlotValuesDialog(QWidget):
    def __init__(self, parameter, values):
        super(PlotValuesDialog,self).__init__()
        self.parameter = parameter
        self.values = values

        label1 = QLabel("single value:")
        label2X = QLabel("range of values:")
        label3 = QLabel("values to plot:")

        self.singleValue = QComboBox()
        self.rangeLower = QComboBox()
        self.rangeHigher = QComboBox()
        for value in self.values:
            self.singleValue.addItems([str(value) if not isinstance(value, str) else '"{}"'.format(value)])
            self.rangeLower.addItems([str(value) if not isinstance(value, str) else '"{}"'.format(value)])
            self.rangeHigher.addItems([str(value) if not isinstance(value, str) else '"{}"'.format(value)])


        self.valuesToPlot = QLabel()
        self.valuesList = []
        self.valuesToPlot.setText(str(self.valuesList))
        self.valuesToPlot.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        addSingleValueButton = QPushButton("Add value to list")
        addSingleValueButton.clicked.connect(self.addSingleValue)
        addRangeButton = QPushButton("Add values to list")
        addRangeButton.clicked.connect(self.addRange)
        emptyListButton = QPushButton("Empty list")
        emptyListButton.clicked.connect(self.emptyList)

        mainLayout = QGridLayout()
        mainLayout.addWidget(label1,          0, 0)
        mainLayout.addWidget(self.singleValue,  0, 1, 1, 2)
        mainLayout.addWidget(addSingleValueButton,      0, 3)
        mainLayout.addWidget(label2X,          1, 0)
        mainLayout.addWidget(self.rangeLower,1, 1)
        mainLayout.addWidget(self.rangeHigher,1, 2)
        mainLayout.addWidget(addRangeButton,    1, 3)
        mainLayout.addWidget(label3,          2, 0)
        mainLayout.addWidget(self.valuesToPlot,   2, 1, 1, 2)
        mainLayout.addWidget(emptyListButton,    2, 3)
        mainLayout.setRowMinimumHeight(2, 40)
        mainLayout.addWidget(QLabel(), 3, 0)
        mainLayout.setRowStretch(3, 1)
        #mainLayout.setColumnMinimumWidth(1, 200 )
        mainLayout.setSpacing(5)

        self.setLayout(mainLayout)

    def addSingleValue(self):
        self.valuesList.append(int(self.singleValue.currentText()))
        self.valuesList = sorted(set(self.valuesList))
        self.valuesToPlot.setText(str(self.valuesList))

    def addRange(self):
        for value in self.values:
            if value >= int(self.rangeLower.currentText()) and int(self.rangeHigher.currentText()) >= value:
                self.valuesList.append(value)
        self.valuesList = sorted(set(self.valuesList))
        self.valuesToPlot.setText(str(self.valuesList))

    def emptyList(self):
        self.valuesList=[]
        self.valuesToPlot.setText(str(self.valuesList))


class SelectorDialog(QDialog):
    def __init__(self, parameter, values):
        super().__init__()
        self.parameter = parameter
        print(values)
        try:
            self.values = [int(val) for val in values]
        except:
            self.valuse = values
        print(values)
        self.setWindowTitle("Choose values. of {} to plot!".format(parameter))

        self.chooseValues = PlotValuesDialog(self.parameter, self.values)
        QBtn = QDialogButtonBox.Ok
        self.buttonBox= QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chooseValues)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        if len(self.chooseValues.valuesList)==0:
            print ("You did not choose any values!")
        else:
            if len(self.chooseValues.valuesList)==1:
                self.choosenValues = self.chooseValues.valuesList[0]
            else:
                self.choosenValues = ""
                for val in self.chooseValues.valuesList:
                    if self.choosenValues == "":
                        self.choosenValues += str(val)
                    else:
                        self.choosenValues += "," + str(val)
            self.reject()