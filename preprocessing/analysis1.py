#counting of the patients having different sessions

import pandas as pd

# Load the dataset
df = pd.read_csv('ADNIMERGE_18Sep2023_final2.csv')

# Define the required sessions (months)
required_sessions = {60}

# Function to check if all required sessions are present for a patient
def check_sessions(group):
    sessions_present = set(group['Month'])
    return required_sessions.issubset(sessions_present)

# Group data by PTID and apply the checking function
grouped = df.groupby('PTID').apply(check_sessions)

# Count the number of patients with all required sessions
count_patients = grouped.sum()

print(f'Number of unique patients with sessions at months {required_sessions}: {count_patients}')

with open("analysis1.txt", "a") as file:
        file.write(f'Number of unique patients with sessions at months {required_sessions}: {count_patients}\n')

