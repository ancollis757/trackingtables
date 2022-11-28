#################  IMPORTS  ###############

import pandas as pd
import pyodbc
from datetime import datetime
import os

############  GLOBAL VARIABLES  ###########

TRACKER_NAMES = ['NeckInj', 'WTT']
TRACKER_TABLE_NAMES = ['NeckInj_wPeriod', 'WTT']
TRACKER_SPREADSHEET_NAMES = ['NeckInj_Uploader.xlsx', 'WTT_Uploader.xlsx']
SPREADSHEETS_DIRECTORY = r'C:\Users\nicko\Documents\GitHub\trackingtables'
SQL_EXTRACT_QUERIES = ['SelectfromNeckinj_wPeriod.sql','']

# Issue of linking to variables not yet fixed. See SQL import method for hard-coding of server and database names.
# SERVER_STRING = 'Server=DESKTOP-IH85PI5;'  # Cannot insert variable in cnxn statement so global whole string.
# DATABASE_CNXN_STRING = 'Database=tracking;'  # Cannot insert variable in cnxn statement so global whole string.

#################  CLASSES  ###############

class Tracker:
    def __init__(self, tracker_name, tracker_table_name, tracker_spreadsheet_name, sql_extract_query):
        print("New tracker instance being creating...")
        self.tracker_name = tracker_name
        self.tracker_table_name = tracker_table_name
        self.tracker_spreadsheet_name = tracker_spreadsheet_name
        self.sql_extract_query = sql_extract_query

    def import_sql(self):
        print(f"Importing table for {self.tracker_name}...")
        # Make connection to the on-premises database.
        cnxn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-IH85PI5;'
                              'Database=tracking;'
                              'Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        # Get out the SQL query
        fd = open(self.sql_extract_query, 'r')
        sqlFile = fd.read()
        fd.close()
        all_queries_in_file = sqlFile.split(';')  # all SQL commands (split on ';')
        query = all_queries_in_file[0]  # Extract the first query.

        # Extract the data from the table.
        self.unprocessed_sql_data = pd.read_sql(query, cnxn)


#################  MAIN RUN  ###############

os.chdir(SPREADSHEETS_DIRECTORY)  # Set current working directory to location of data spreadsheets.
tracker_1 = Tracker(TRACKER_NAMES[0], TRACKER_TABLE_NAMES[0], TRACKER_SPREADSHEET_NAMES[0], SQL_EXTRACT_QUERIES[0])
tracker_1.import_sql()
