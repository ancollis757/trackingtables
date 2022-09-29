import pyodbc
import pandas as pd

REPORT_COLUMNS = [
    'LogStart'
    ,'LogEnd'
    ,'LeftPain'
    ,'LeftNumb'
    ,'RightPain'
    ,'RightNumb'
    ,'NeckTotal'
    ,'LeftElbowPain'
    ,'LeftElbowNumb'
]

SQL_FILES = [
    'SelectfromNeckinj_wPeriod.sql'
]

""""
NOTES:
The pd.read_sql method cannot be used as the type of connection database I have is not supported.
"""

"""
DELIVERABLES:

Average of each numb and pain, by period.
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

# Get out the update, using today's date as the end of the current period.
neckinj_Table = pd.read_sql(query,cnxn)
summary = neckinj_Table.groupby(['PeriodName']).mean()
summary = pd.DataFrame(summary)  # Making a DF from the groupby object

# Need some intense group by action; getting out min and max for each period.
# Then order the table by start date (or end date).
# Drop ExternalityAdjustment for now; not sure how useful it is.

summary2 = neckinj_Table.groupby(['PeriodName']).min()
summary2 = pd.DataFrame(summary2)
summary2 = pd.DataFrame(summary2['LogDate'])  # Force back to a DF rather than a Series.
summary2.rename(columns={"LogDate": "LogStart"}, inplace=True)

summary3 = neckinj_Table.groupby(['PeriodName']).max()
summary3 = pd.DataFrame(summary3)
summary3 = pd.DataFrame(summary3['LogDate'])
summary3.rename(columns={"LogDate": "LogEnd"}, inplace=True)

summary4 = summary3.join(summary2)  # Join axis not specified; defaults to index.
summary5 = summary4.join(summary)
summary5.sort_values(['LogStart'], axis=0, inplace=True)
summary5['NeckTotal'] = summary5['LeftPain'] + summary5['LeftNumb'] + summary5['RightPain'] + summary5['RightNumb']
summary5 = summary5[REPORT_COLUMNS]

summary5.to_excel('output.xlsx')