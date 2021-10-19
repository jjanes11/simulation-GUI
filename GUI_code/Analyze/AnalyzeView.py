from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton
)

from .Abstract import View
from .AnalyzeSelector import DatabaseSelector, TableSelector, ParamSelector
from .PlotView import PlotView
from .decorators import wrap_widgets_in_layout

from typing import List, Dict


class AnalyzeView(View):
    
    def init_UI(self, db: str, tables: List[str], params: Dict[str, List[str]]):
        selector_layout, widgets = self.__create_selector_widgets(db, tables, params)
        plotview_layout, widgets = self.__create_plotview_widgets()
        layout = QHBoxLayout()
        layout.addLayout(selector_layout)
        layout.addLayout(plotview_layout)
        self.setLayout(layout)

    @wrap_widgets_in_layout
    def __create_plotview_widgets(self):
        self.plotview = PlotView()
        self.plotview.set_controller(self)
        return [self.plotview]

    @wrap_widgets_in_layout
    def __create_selector_widgets(self, db: str, tables: List[str], params: Dict[str, List[str]]):
        self.dbselector = DatabaseSelector(db)
        self.dbselector.add_observer(self.controller)
        self.tableselector = TableSelector(tables)
        self.tableselector.add_observer(self.controller)
        self.paramselector = ParamSelector(params)
        self.paramselector.add_observer(self.controller)
        #self.paramselector.notify()
        plotbutton = QPushButton("Plot!")
        plotbutton.clicked.connect(self.controller.plotButtonHandler)
        return [self.dbselector, self.tableselector, self.paramselector, plotbutton]
