import pyodbc
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IH85PI5;'
                      'Database=tracking;'
                      'Trusted_Connection=yes;')

table_name = 'NeckInj'
cursor = conn.cursor()
cursor.execute('SELECT * FROM NeckInj') #All text here so no variable names.

for i in cursor:
    print(i)


