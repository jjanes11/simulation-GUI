#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import sqlite3
import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict
from six import string_types
import glob

'''
Model class. Models manage reading and writting to the sqlite database GUI.db and fething corresponding 
data files in the directory output.
'''

class Model(ABC):

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def set_controller(self):
        pass


'''ReadOnlyModel'''
class AnalyzeModel(Model):

    def config(self):
        databases = self.get_databases()
        self._db = databases[0]
        print("db:", self.db)
        self.db_tablenames = self.get_db_tablenames()
        self.sqlquerry = SQLQuerry()

    @property
    def db(self) -> str:
        return self._db

    @db.setter
    def db(self, db: str) -> None:
        self._db = db

    def get_databases(self) -> List[str]:
        databases = []
        db_folder_path = f"{settings.BASE_DIR}/Databases"
        for db in glob.glob(f"{db_folder_path}/*"):
            print(db)
            databases.append(db)
        if len(databases) == 0:
            print("No databases in the Databases folder!")
        print("databases:", databases)
        return databases

    def set_controller(self, controller):
        self.controller = controller

    def notify(self, controller):
        controller.notify()

    def read(self, selection: Dict[str, List[str]], table: str) -> pd.DataFrame:
        sql_querry = self.sqlquerry.construct(selection, table)
        print("sql_querry:", sql_querry)
        return self.read_sql_querry(sql_querry)

    def read_sql_querry(self, sql_querry: str) -> pd.DataFrame:
        '''Reads the database as a pandas dataframe simTable'''
        try:
            conn = sqlite3.connect(self._db)
            print("Connected to SQLite")
            conn.row_factory = sqlite3.Row
            simTable = pd.read_sql_query(sql_querry, conn)
            #print("simTable:", simTable)
            print(f"Succsesfully read from database {self._db}.")
            #print(self.simTable)
        except sqlite3.Error as error:
            print(f"Failed to read from database {self._db}!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

        return simTable

    def save(self):
        self.notify(self.controller)

    def get_db_tablenames(self) -> List[str]:
        tables = []
        try:
            conn = sqlite3.connect(self._db)
            print("Connected to SQLite")
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tableNames = c.fetchall()
            for table in tableNames:
                tables.append(table[0])    
            c.close()
            conn.close()
            return tables

        except sqlite3.Error as error:
            print(f"Failed to read from database {self._db}!", error)
        
    def get_param_names(self, table: str) -> List[str]:
        try:
            conn = sqlite3.connect(self._db)
            print("Connected to SQLite")
            conn.row_factory = sqlite3.Row
            print("tablename in get_param_names:", table)
            cursor = conn.execute(f"SELECT * FROM {table}")
            print("cursor.fetchone():", cursor.fetchone())
            param_names = cursor.fetchone().keys()
            conn.close()
            return param_names

        except sqlite3.Error as error:
            print(f"Failed to read from database {self._db}", error)

    def find_distinct_params(self, sql_querry) -> Dict[str, List[str]]:
        simtable = self.read_sql_querry(sql_querry)
        table_name_index = sql_querry.split(" ").index("FROM") + 1
        table_name = sql_querry.split(" ")[table_name_index]
        param_names = self.get_param_names(table_name)
        distinct_simParams = dict()
        for name in param_names:
            distinct_simParams.update({name : sorted(simtable[name].unique())})
        #convert to list of strings for convenience
        for key in distinct_simParams:
            distinct_simParams[key] = [str(elem) for elem in distinct_simParams[key]] 

        return distinct_simParams

    def get_selection_options(self, selection: Dict[str, List[str]], table: str):
        sql_querry = self.sqlquerry.construct(selection, table)
        #print("sql_querry:", sql_querry)
        return self.find_distinct_params(sql_querry)

 


class SQLQuerry:
    '''Class with methods for constructing the sql querries which are passed to the model methods'''
    def construct(self, selection: Dict[str, List[str]], table: str) -> str:
        query_template = "SELECT * FROM {}"
        
        if selection == None and table != None:
            sql_querry = query_template.format(table)
        elif selection == None and table == None:
            sql_querry = query_template.format(f"{table}")
        elif selection != None:
            #format.strings modifyies the selection dict in place so we pass a copy,
            #as selection is needed in other parts of the code unmodified'''
            selection = self.format_strings(selection.copy())
            print("selection:", selection)
            selection_made = False  #set to true when at least one tableParam has been selected (different from <any>)
            for param, value in selection.items():
                if value != "'all values'":
                    if selection_made:
                        query_template += " AND "
                    else:
                        query_template += " WHERE "
                    query_template += f"{param} IN ({value})"
                    selection_made = True
            #print(query_template)
            # selected_db_table = self.tableSelector.currentText()
            # sql_querry = query_template.format(selected_db_table)
            if table != None:
                sql_querry = query_template.format(table)
            else:
                sql_querry = query_template.format(f"{self._db}")
        print("sql_querry:", sql_querry)
        return sql_querry   

    def format_strings(self, params):
        for key, val in params.items():
            print("key, val:", key, val)
            params[key] = self.quote_sql_string(val)
            print(key, val)
        return params

    def quote_sql_string(self, value):
        '''
        If `value` is a string type, escapes single quotes in the string
        and returns the string enclosed in single quotes.
        '''
        # try:
        #     value.split(",")
        #     return int(value)
        # except:
        #     if isinstance(value, string_types):
        #         new_value = str(value)
        #         new_value = new_value.replace("'", "''")
        #         return "'{}'".format(new_value)
        #     return value

        try:
            bla = value.split(",")
            if len(bla) == 1:
                try:    
                    return int(value)
                except:
                    if isinstance(value, string_types):
                        new_value = str(value)
                        new_value = new_value.replace("'", "''")
                        return "'{}'".format(new_value)
                    return value
            else:
                try:    
                    for e in bla:
                        int(e)
                    return value
                except:
                    for e in bla:
                        value_string = ""
                        if isinstance(e, string_types):
                            new_value = str(e)
                            new_value = new_value.replace("'", "''")
                            value_string += "'{}'".format(new_value)
                        return value_string
        except:
            return value
    # def check_selection_type(slef, selection):
    #     if selection != None:
    #         for key, val in selection.items():
    #             print("val:",val, type(val))
    #             try:
    #                 for elem in val:  
    #                     print(elem, type(elem))
    #             except:
    #                 print("except", val, type(val))


# '''ComplexModel'''
# class ComplexModel:
#     def __init__(self, database):
#         self.db = database
#         self.db_tablenames = self.get_database_tablenames()
#         #self.read(sql_select_querry = "SELECT * from {}", selected_db_table  = self.db_tablenames[0][0])

#     def get_database_tablenames(self):
#         db = sqlite3.connect(self.db)
#         c = db.cursor()
#         c.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         tableNames = c.fetchall()
#         c.close()
#         db.close()
#         #print(tableNames)
#         return tableNames

#     def get_selectorNames(self):
#         writeTableSelector = []
#         self.tables= self.model.get_database_tablenames()
#         for table in self.tables:
#             writeTableSelector.addItem(table[0])
#         #read column names of the selected simTable
#         self.conn = sqlite3.connect(self.db)
#         self.conn.row_factory = sqlite3.Row
#         self.cursor = self.conn.execute("select * from {}".format(writeTableSelector.currentText()))
#         self.selectorNames = self.cursor.fetchone().keys()
#         self.conn.close()

#     def read(self, sql_querry):
#         '''Reads the database as a pandas dataframe simTable'''
#         try:
#             conn = sqlite3.connect(self.db)
#             print("Connected to SQLite")
#             conn.row_factory = sqlite3.Row
#             simTable = pd.read_sql_query(sql_querry, conn)
#             #print("assigned simTable to:", self.simTable)
#             print(f"Succsesfully read from database {self.db}.")
#             #print(self.simTable)
#         except sqlite3.Error as error:
#             print(f"Failed to read from database {self.db}!", error)
#         finally:
#             if conn:
#                 conn.close()
#                 print("The SQLite connection is closed")

#         return simTable

#     def save(self, data):
#         inputparams={}
#         #print("data", data, data.split("="))
#         for input in data.split():
#             a = input.split("=")
#             if a[0][2:] in ["bias", "variance"]:
#                 inputparams[a[0][2:]] = int(a[1])
#             else:
#                 inputparams[a[0][2:]] = a[1]
#         try:
#             sqliteConnection = sqlite3.connect('GUI_database.db')
#             cursor = sqliteConnection.cursor()
#             print("Successfully Connected to SQLite")
#             #print((inputparams["bias"], inputparams["variance"], inputparams["file_name"]))
#             sqlite_insert_query = f"""INSERT INTO GUI_table
#                                 (bias, variance, file_name)
#                                 VALUES
#                                 {(inputparams["bias"], inputparams["variance"], inputparams["file_name"])}
#                                 """

#             count = cursor.execute(sqlite_insert_query)
#             sqliteConnection.commit()
#             print("Record inserted successfully into GUI_table table ", cursor.rowcount)
#             cursor.close()

#         except sqlite3.Error as error:
#             print("Failed to insert data into sqlite table", error)
#         finally:
#             if sqliteConnection:
#                 sqliteConnection.close()
#                 print("The SQLite connection is closed")

#     def find_distinct_params(self, sql_querry):
#         simtable = self.read(sql_querry)
#         distinct_simParams = dict()
#         for name in self.selectorNames:
#             distinct_simParams.update({name : sorted(simtable[name].unique())})
#         return distinct_simParams
