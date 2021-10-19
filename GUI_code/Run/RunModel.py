#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import pandas as pd
from abc import ABC, abstractmethod
from typing import List
import os
import glob
import settings


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


class RunModel:

    def config(self):
        databases = self.get_databases()
        self._db = databases[0]
        print("db:", self.db)
        self.db_tablenames = self.get_database_tablenames()

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

    def get_database_tablenames(self) -> List[str]:
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

    def get_selectorNames(self, table: str) -> List[str]:
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


    def read(self, sql_querry):
        '''Reads the database as a pandas dataframe simTable'''
        try:
            conn = sqlite3.connect(self._db)
            print("Connected to SQLite")
            conn.row_factory = sqlite3.Row
            simTable = pd.read_sql_query(sql_querry, conn)
            #print("assigned simTable to:", self.simTable)
            print(f"Succsesfully read from database {self._db}.")
            #print(self.simTable)
        except sqlite3.Error as error:
            print(f"Failed to read from database {self._db}!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

        return simTable

    def save(self, data, table):
        inputparams={}
        #print("data", data, data.split("="))
        for input in data.split():
            a = input.split("=")
            if a[0][2:] in ["bias", "variance"]:
                inputparams[a[0][2:]] = int(a[1])
            else:
                inputparams[a[0][2:]] = a[1]
        try:
            sqliteConnection = sqlite3.connect(f"{self._db}")
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            #print((inputparams["bias"], inputparams["variance"], inputparams["file_name"]))
            sqlite_insert_query = f"""INSERT INTO {table}(bias, variance, file_name)
                                VALUES
                                {(inputparams["bias"], inputparams["variance"], inputparams["file_name"])}
                                """

            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print(f"Record inserted successfully into {table} table of database {self._db} ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def find_distinct_params(self, sql_querry):
        simtable = self.read(sql_querry)
        distinct_simParams = dict()
        for name in self.selectorNames:
            distinct_simParams.update({name : sorted(simtable[name].unique())})
        return distinct_simParams