import pyodbc
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

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

# Extract the data from the table.
neckinj_Table = pd.read_sql(query, cnxn)

# Produce plot of total against time.
date_range_x_axis = neckinj_Table['LogDate'].tolist()
neckinj_Table['NITotal'] = neckinj_Table['LeftPain'] + neckinj_Table['LeftNumb'] + neckinj_Table['RightPain'] + neckinj_Table['RightNumb']
date_range_y_axis = neckinj_Table['NITotal'].tolist()
ni_total_plot = plt.plot(date_range_x_axis, date_range_y_axis, label='Muhline')

x = [3,4,5]
y = [6,7,8]

plt.plot

print(type(plt.plot(date_range_x_axis, date_range_y_axis, label='Muhline')))
print(type(ni_total_plot))

# naming the x axis
ni_total_plot.xlabel('Log Date')
# naming the y axis
ni_total_plot.ylabel('Total NI')
# giving a title to my graph
ni_total_plot.title('NI by Time')
# function to show the plot
ni_total_plot.show()
ni_total_plot.ylim(0, 8)
ni_total_plot.xlim(0, 8)


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

# Produce the summary.
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

