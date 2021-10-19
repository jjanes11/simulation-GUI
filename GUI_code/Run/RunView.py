#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout
)
from .Abstract import View
from .RunSelector import DatabaseSelector, InputParamSelector, TableSelector
from .SimView import SimView
from .decorators import wrap_widgets_in_layout

from typing import List

class RunView(View):
    '''Main GUI View for simulation running and progress tracking.'''

    def init_UI(self, db: str, tables: List[str], param_names): 
        #create selector view
        simSelectorLayout, widgets = self.__create_selector_widgets(db, tables, param_names)
        #create simulation monitor/control view
        simMonitorControll = self.__create_simview_widgets()
        #set layout
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(simSelectorLayout)
        mainLayout.addLayout(simMonitorControll)
        self.setLayout(mainLayout)

    @wrap_widgets_in_layout
    def __create_selector_widgets(self, db, tables, param_names):
        self.dbselector = DatabaseSelector(db)
        self.dbselector.add_observer(self.controller)
        self.tableselector = TableSelector(tables)
        self.tableselector.add_observer(self.controller)
        self.paramselector = InputParamSelector(param_names)
        return [self.dbselector, self.tableselector, self.paramselector]

    #each simualtion gets its own SimView object and SimController 
    #which is fetchingSimController(self.model, self, simview) the selected input parameters and writting to the database and SimMonitor
    def __create_simview_widgets(self):
        simLayout = QGridLayout()
        pos = {0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1), 4:(2,0), 5:(2,1), 6:(3,0), 7:(3,1)}
        for i in range(6):
            self.simview = SimView(f"sim{i+1}")
            simLayout.addWidget(self.simview, pos[i][0],pos[i][1])
            self.controller.notification(sender = self, event = "simview_created")

        return simLayout

    def update_selectors(self):
        pass




