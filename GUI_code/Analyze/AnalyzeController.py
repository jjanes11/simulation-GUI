#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from .SelectorDialog import SelectorDialog

from .AnalyzeView import AnalyzeView
from typing import List, Dict
import settings
import os

class AnalyzeController(QWidget):
    def __init__(self, model, view: AnalyzeView):
        QWidget.__init__(self)
        self.model = model
        self.view = view
        self.configure_model()
        self.config_view()
        self.table = self.view.tableselector.state()
        self.selection = self.view.paramselector.state()

    def configure_model(self):
        self.model.config()
        self.model.set_controller(self)
        self.db = self.model.db.split("/")[-1]
        self.table_names = self.model.get_db_tablenames()
        self.param_names = self.model.get_param_names(self.table_names[0])
        self.distinct_param_values = self.model.find_distinct_params(f"SELECT * FROM {self.table_names[0]}")

    def config_view(self):
        self.view.controller = self
        self.view.init_UI(self.db, self.table_names, self.distinct_param_values)

    def notify(self, event: str, selection: Dict[str, List[str]] or str):
        EventResponseStrategy(self, self.view, event, selection)

    def notification(self, sender: QWidget, event: str):
        if event == "database_selected":
            self.config_database(sender)

    def config_database(self, sender):
        self.model.db = os.path.join(settings.BASE_DIR, f'Databases/{sender.db}')
        self.update_selectors()

    def update_selectors(self):
        db_tables = self.model.get_db_tablenames()
        self.view.tableselector.update(db_tables)
        selection_options = self.model.get_selection_options(None, db_tables[0])
        print("selection option:", selection_options)
        self.view.paramselector.update(selection_options, None)

    def plotButtonHandler(self):
        selected_table = self.model.read(self.selection, self.table)
        self.view.plotview.update(selected_table)



class EventResponseStrategy:
    def __init__(self, controller: AnalyzeController, view: AnalyzeView, event: str, selection: Dict[str, List[str]] or str):
        if event == "state of the param_selector changed":
            #get the selected table
            table = view.tableselector.state()
            #if user chose to select a combination of values open the selection dialog,
            #else return the input selection
            distinct_params = controller.model.find_distinct_params(sql_querry = f"SELECT * FROM {table}")
            selection = ParamDialog().choose_values_in_dialog(selection, table, distinct_params)
            selection_options = controller.model.get_selection_options(selection, table)
            view.paramselector.update(selection_options, selection)
            self.update_controller_data_on_selection(controller, selection, table)

        elif event == "state of the table_selector changed":
            table = selection
            #get the selected params
            selection = view.paramselector.state()
            #get the selection options for the selected table (all of them assuming there is no param selection)
            selection_options = controller.model.get_selection_options(None, table)
            print("table selection_options:", selection_options)
            view.paramselector.update(selection_options, None)
            self.update_controller_data_on_selection(controller, selection, table)


    def update_controller_data_on_selection(self, controller, param_selection: str, table: str):
        controller.selection = param_selection
        controller.table = table


class ParamDialog:
    def choose_values_in_dialog(self, selection: Dict[str, List[str]], table: str, distinct_params):
        for param, val in selection.items():
            if val == "combination of values":
                print("created dialog!")
                self.dialog = SelectorDialog(param, distinct_params[param])
                self.dialog.exec_()
                print("choosen values:", self.dialog.choosenValues, type(self.dialog.choosenValues))
                selection[param] = self.dialog.choosenValues
        return  selection