import pyodbc
import pandas as pd
from datetime import datetime
from pyxll import xl_func, plot
import matplotlib.pyplot as plt

REPORT_COLUMNS = [
    'LogStart',
    'LogEnd',
    'LeftPain',
    'LeftNumb',
    'RightPain',
    'RightNumb',
    'NITotal',
    'LeftElbowPain',
    'LeftElbowNumb'
]
SQL_FILE = 'SelectfromNeckinj_wPeriod.sql'
FILENAME_STEM = 'NI_Report_'
OUTPUT_LOCATION = 'C:\\Users\\nicko\\Desktop\\Reports\\'
TABLE_NAME = 'NeckInj_GapFilled'

def sql_connection():

    # Make connection to the on-premises database.
    cnxn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-IH85PI5;'
                          'Database=tracking;'
                          'Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    # Get out the SQL query
    fd = open(SQL_FILE, 'r')
    sqlFile = fd.read()
    fd.close()
    all_queries_in_file = sqlFile.split(';')  # all SQL commands (split on ';')
    query = all_queries_in_file[0]  # Extract the first query.

    # Extract the data from the table.
    neckinj_Table = pd.read_sql(query, cnxn)
    return neckinj_Table

# PLOTTING FUNCTIONALITY NOT YET OPERATIONAL.
# https://www.pyxll.com/docs/userguide/plotting/matplotlib.html
@xl_func
def plot(x_data, y_data):
    # Create the figure and plot the data
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    ax.set(xlabel='date', ylabel='NI Total',
           title='NI Total by time')
    ax.grid()
    plot(fig)

def produce_summary(pd_table):

    pd_table['NITotal'] = pd_table['LeftPain'] + pd_table['LeftNumb'] + pd_table['RightPain'] + \
                               pd_table['RightNumb']
    unformatted_results = pd_table.groupby(['PeriodName']).mean()
    unformatted_results = pd.DataFrame(unformatted_results)  # Making a DF from the group-by object

    # Get out log start as a single column DF, to join with results DF.
    log_Start = pd_table.groupby(['PeriodName']).min()
    log_Start = pd.DataFrame(log_Start['LogDate'])  # Force back to a DF rather than a Series.
    log_Start.rename(columns={"LogDate": "LogStart"}, inplace=True)

    # Get out log end as a single column DF, to join with results DF.
    log_End = pd_table.groupby(['PeriodName']).max()
    log_End = pd.DataFrame(log_End['LogDate'])
    log_End.rename(columns={"LogDate": "LogEnd"}, inplace=True)

    # Produce the summary.
    date_ranges = log_End.join(log_Start)  # Join axis not specified; defaults to index.
    pd_table = date_ranges.join(unformatted_results)
    pd_table.sort_values(['LogStart'], axis=0, inplace=True)
    pd_table = pd_table[REPORT_COLUMNS]
    return pd_table

# Run the query and get out the result.
neckinj_Table = sql_connection()
ni_report = produce_summary(neckinj_Table)

# Produce the report file name and export.
today = datetime.today().strftime('%Y-%m-%d')
output_filename = FILENAME_STEM + today + '.xlsx'
output_full = OUTPUT_LOCATION + output_filename
ni_report.to_excel(output_full, float_format='%.2f')

