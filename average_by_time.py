import pyodbc
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IH85PI5;'
                      'Database=tracking;'
                      'Trusted_Connection=yes;')




table_name = 'NeckInj'
cursor = conn.cursor()

fd = open('SummarybyPeriod.sql', 'r') # Open and read the file as a single buffer
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
query = sqlFile.split(';')
print (query)



#query = 'SELECT * FROM NeckInj'
cursor.execute(query)

for i in cursor:
    print(i)