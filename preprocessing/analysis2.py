#removing unimportant columns

import pandas as pd

# Load the CSV file
df = pd.read_csv('ADNIMERGE_18Sep2023_final2.csv')

# List of columns to be deleted
columns_to_delete = ['PTEDUCAT', 'PTETHCAT', 'PTRACCAT', 'PTMARRY', 
                     'FLDSTRENG', 'FSVERSION', 'FLDSTRENG_bl', 'FSVERSION_bl', 'M']

# Drop the columns from the DataFrame
df = df.drop(columns=columns_to_delete, errors='ignore')

# Save the modified DataFrame back to a CSV file
df.to_csv('ADNIMERGE_18Sep2023_final3.csv', index=False)

print("Columns removed and file saved.")

