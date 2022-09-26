import pandas as pd

#full_file_path = 'C:\Users\nicko\OneDrive\04 Health\PainLog_CriteriaandNotes.xlsx'

data = pd.read_excel('C:\\Users\\nicko\\OneDrive\\04 Health\\PainLog_CriteriaandNotes.xlsx', sheet_name='0 Tracking Criteria', header=None)

print(data)