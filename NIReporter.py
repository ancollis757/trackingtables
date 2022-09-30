import pyodbc
import pandas as pd
from datetime import datetime

REPORT_COLUMNS = [
    'LogStart',
    'LogEnd',
    'LeftPain',
    'LeftNumb',
    'RightPain',
    'RightNumb',
    'NeckTotal',
    'LeftElbowPain',
    'LeftElbowNumb'
]

SQL_FILE = 'SelectfromNeckinj_wPeriod.sql'

FILENAME_STEM = 'NI_Report_'

OUTPUT_LOCATION = 'C:\\Users\\nicko\\Desktop\\Reports\\'

# Make connection to the on-premises database.
cnxn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IH85PI5;'
                      'Database=tracking;'
                      'Trusted_Connection=yes;')
table_name = 'NeckInj_GapFilled'
cursor = cnxn.cursor()

# Get out the SQL query
fd = open(SQL_FILE, 'r')
sqlFile = fd.read()
fd.close()
all_queries_in_file = sqlFile.split(';')  # all SQL commands (split on ';')
query = all_queries_in_file[0]  # Extract the first query.

# Pull data from DB using the query, take the mean and then put into a pandas DF.
neckinj_Table = pd.read_sql(query, cnxn)
unformatted_results = neckinj_Table.groupby(['PeriodName']).mean()
unformatted_results = pd.DataFrame(unformatted_results)  # Making a DF from the group-by object

# Get out log start as a single column DF, to join with results DF.
log_Start = neckinj_Table.groupby(['PeriodName']).min()
log_Start = pd.DataFrame(log_Start)
log_Start = pd.DataFrame(log_Start['LogDate'])  # Force back to a DF rather than a Series.
log_Start.rename(columns={"LogDate": "LogStart"}, inplace=True)

# Get out log end as a single column DF, to join with results DF.
log_End = neckinj_Table.groupby(['PeriodName']).max()
log_End = pd.DataFrame(log_End)
log_End = pd.DataFrame(log_End['LogDate'])
log_End.rename(columns={"LogDate": "LogEnd"}, inplace=True)

# Produce the completed report.
ni_date_ranges = log_End.join(log_Start)  # Join axis not specified; defaults to index.
ni_report = ni_date_ranges.join(unformatted_results)
ni_report.sort_values(['LogStart'], axis=0, inplace=True)
ni_report['NeckTotal'] = ni_report['LeftPain'] + ni_report['LeftNumb'] + ni_report['RightPain'] + ni_report['RightNumb']
ni_report = ni_report[REPORT_COLUMNS]

# Produce the report file name and export.
today = datetime.today().strftime('%Y-%m-%d')
output_filename = FILENAME_STEM + today + '.xlsx'
output_full = OUTPUT_LOCATION + output_filename
ni_report.to_excel(output_full, float_format='%.2f')
