import pyodbc
import pandas as pd

COLUMNS = [
    'LogDate'
    ,'RightPain'
    ,'RightNumb'
    ,'LeftPain'
    ,'LeftNumb'
    ,'LeftElbowPain'
    ,'LeftElbowNumb'
    ,'Notes'
    ,'ExternalityAdjustment'
    ,'PeriodName'
]

SQL_FILES = [
    'SCRIPTUSEONLY_SetCurrentPeriodEnd_ToToday.sql'
    ,'Neckinj_withperiods_joined.sql'
    ,'SCRIPTUSEONLY_SetCurrentPeriodEnd_NULL.sql'
]



""""
NOTES:
The pd.read_sql method cannot be used as the type of connection database I have is not supported.
"""

"""
DELIVERABLES:

Average of each numb and pain, by period.
Average of total, before and after externality adjustment, by period.
Date of latest entry.
Each period given its names and date period.

NOTING LONG TERM GOAL OF AUTOMATED REPORTING:

All the above ported to an excel spreadsheet in a standard format.

"""

cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IH85PI5;'
                      'Database=tracking;'
                      'Trusted_Connection=yes;')
table_name = 'NeckInj_GapFilled'
cursor = cnxn.cursor()

# Get out the SQL query

query_list = []
for file in SQL_FILES:

    fd = open(file, 'r')
    sqlFile = fd.read()
    fd.close()
    all_queries_in_file = sqlFile.split(';') # all SQL commands (split on ';')
    query = all_queries_in_file[0] # Extract the first query.
    query_list.append(query)

# Run update to set today's date as end of current period in the SQL table.
cursor.execute(query_list[0])

# Get out the update, using today's date as the end of the current period.
neckinj_Table = pd.read_sql(query,cnxn)
summary = neckinj_Table.groupby(['PeriodName']).mean()
print(summary)

# Run update to change end of current period back to Null.
cursor.execute(query_list[0])