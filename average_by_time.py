import pyodbc
import pandas as pd

"""NOTES:
The pd.read_sql method cannot be used as the type of connection database I have is not supported.
"""

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IH85PI5;'
                      'Database=tracking;'
                      'Trusted_Connection=yes;')
table_name = 'NeckInj_GapFilled'
cursor = conn.cursor()

# Get out the SQL query
fd = open('Neckinj_withperiods_joined.sql', 'r')
sqlFile = fd.read()
fd.close()
query_list = sqlFile.split(';') # all SQL commands (split on ';')
query = query_list[0] # Extract the first query.

cursor.execute(query) #Doesn't return the headings.
columnHeadings = []
for column in cursor.description:
    columnHeading = str(column[0])
    columnHeadings.append(columnHeading)
print(type(columnHeadings))

neckinj_Table = pd.DataFrame = (cursor)
neckinj_Table.columns = columnHeadings
print(neckinj_Table)
