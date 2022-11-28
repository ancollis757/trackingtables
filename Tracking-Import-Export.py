#################  IMPORTS  ###############

import pandas as pd
import pyodbc
from datetime import datetime
import os

############  GLOBAL VARIABLES  ###########

TRACKER_NAMES = ['', '']
TRACKER_TABLE_NAMES = ['', '']
TRACKER_SPREADSHEET_NAMES = ['', '']
SPREADSHEETS_DIRECTORY = r'blah'
DATABASE_NAME = 'tracking'
SERVER = 'DESKTOP-IH85PI5'

#################  CLASSES  ###############

class Tracker:
    def __init__(self, tracker_name, tracker_table_name, tracker_spreadsheet_name):
        self.tracker_name = tracker_name
        self.tracker_table_name = tracker_table_name
        self.tracker_spreadsheet_name = tracker_spreadsheet_name

        print("New tracker instance being creating...")

    def import_sql(self):
        # Make connection to the on-premises database.
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-IH85PI5;'
                              'Database=DATABASE_NAME;' 
                              'Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        # Get out the SQL query
        fd = open(self.tracker_table_name, 'r')
        sqlFile = fd.read()
        fd.close()
        all_queries_in_file = sqlFile.split(';')  # all SQL commands (split on ';')
        query = all_queries_in_file[0]  # Extract the first query.

        # Extract the data from the table.
        self.unprocessed_sql_data = pd.read_sql(query, cnxn)

#################  MAIN RUN  ###############

os.chdir(SPREADSHEETS_DIRECTORY)  # Set current working directory to location of data spreadsheets.
