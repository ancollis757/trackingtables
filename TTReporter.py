import pyodbc
import pandas as pd
from datetime import datetime
from pyxll import xl_func, plot
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr  # For bespoke formatting of graph ticks.
import numpy as np
import pandas as pd
import os
import datetime as dt

REPORT_COLUMNS = [
    'LogDate',
    'LIT_Minutes',
    'OW_Minutes',
    'Notes',
]
SQL_FILE = 'SelectfromWTT.sql'
FILENAME_STEM = 'WTT_Report_'
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
    wtt_table = pd.read_sql(query, cnxn)
    return wtt_table


# PLOTTING FUNCTIONALITY NOT YET OPERATIONAL.
# https://www.pyxll.com/docs/userguide/plotting/matplotlib.html
@xl_func
def plot(pd_table):

    # Create plot canvas
    plt.style.use("ggplot")
    fig = plt.figure()
    fig.suptitle("WTT Plots")

    ax1 = fig.add_subplot(2, 1, 1)  # nrows, ncols, index.
    ax2 = fig.add_subplot(2, 1, 2)  # nrows, ncols, index.
    pd_table['LIT_Minutes'].sort_values(ascending=True).plot(title='LiT', kind='line', ax=ax1)
    pd_table['OW_Minutes'].sort_values(ascending=True).plot(title='OW T', kind='line', ax=ax2)

    plt.show(block=True)


def produce_summary(pd_table):
    pd_table['WTT_Total'] = pd_table['LIT_Minutes'] + pd_table['OW_Minutes']
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
wtt_table = sql_connection()
wtt_plot = plot(wtt_table)

# Produce the report file name and export.
today = datetime.today().strftime('%Y-%m-%d')
output_filename = FILENAME_STEM + today + '.xlsx'
output_full = OUTPUT_LOCATION + output_filename
# wtt_report.to_excel(output_full, float_format='%.2f')
