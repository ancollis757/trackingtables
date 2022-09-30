from datetime import datetime


FILENAME_STEM = 'NI_Report_'

today = datetime.today().strftime('%Y-%m-%d')
output_filename = FILENAME_STEM + today + '.xlsx'
print(output_filename)