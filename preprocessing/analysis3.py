import pandas as pd
import numpy as np

def load_data(filename):
    """ Load CSV data into a DataFrame. """
    return pd.read_csv(filename)

def filter_patients(df, required_months):
    """ Filter DataFrame to include only patients with at least the required sessions and make sure they are consecutive. """
    # Check if each patient group includes all required sessions
    def includes_required_sessions(group):
        # Check if the set of required months is a subset of the months in the group
        return set(required_months).issubset(set(group['Month']))

    # Filter groups and retain only the required month sessions
    filtered_groups = df.groupby('PTID').filter(includes_required_sessions)
    # Filter out only the required months
    result = filtered_groups[filtered_groups['Month'].isin(required_months)]
    # Sort by PTID and Month to ensure consecutive order
    result = result.sort_values(by=['PTID', 'Month'])
    # Remove any potential duplicates
    result = result.drop_duplicates()
    return result

def save_filtered_data(df, output_filename):
    """ Save the filtered DataFrame to a CSV file. """
    df.to_csv(output_filename, index=False)
    print(f"Filtered data saved to {output_filename}")

def count_rows_per_patient(df):
    """ Count the number of rows per patient and identify those not equal to 5. """
    # Count the rows for each PTID
    patient_counts = df.groupby('PTID').size()

    # Filter patients who do not have exactly 5 entries
    incorrect_counts = patient_counts[patient_counts != 5]
    return incorrect_counts

def remove_duplicate_months(df):
    """ Remove one record from duplicated month entries randomly. """
    def remove_random_duplicate(group):
        # If group is exactly 5 and unique, return as is
        if len(group) == 5 and len(group['Month'].unique()) == 5:
            return group
        # Else, find duplicates and remove one entry randomly
        else:
            # Count the occurrences of each month
            counts = group['Month'].value_counts()
            # Identify months with more than one entry
            duplicate_months = counts[counts > 1].index
            for month in duplicate_months:
                # Get indices of duplicates for the month
                duplicate_indices = group[group['Month'] == month].index
                # Randomly select one to drop
                to_drop = np.random.choice(duplicate_indices, size=1, replace=False)
                group = group.drop(to_drop)
            return group
    
    # Apply the function to each group of PTID and combine results
    return df.groupby('PTID').apply(remove_random_duplicate).reset_index(drop=True)


def main():
    input_filename = 'ADNIMERGE_18Sep2023_final3.csv'
    output_filename = 'ADNIMERGE_18Sep2023_final4.csv'
    required_months = [0, 6, 12, 18, 24]  # Update this as needed for different subsets

    # Load the dataset
    df = load_data(input_filename)

    # Filter the dataset to only include patients with at least the required month sessions
    filtered_df = filter_patients(df, required_months)

    # Calculate and print statistics
    unique_patients_count = len(filtered_df['PTID'].unique())
    print(f"Number of unique patients with at least sessions at months {required_months}: {unique_patients_count}")
    with open("analysis.txt", "a") as file:
        file.write(f'Number of unique patients with sessions at months {required_months}: {unique_patients_count}\n')

    print(f"Total number of rows in the output file: {filtered_df.shape[0]}")

    # Get counts of rows per patient and identify discrepancies
    discrepancies = count_rows_per_patient(filtered_df)

    if discrepancies.empty:
        print("All patients have exactly 5 records.")
        # Save the filtered DataFrame to a new CSV file
        save_filtered_data(filtered_df, output_filename)
        flag = 0
    else:
        print("Patients not having exactly 5 records:")
        print(discrepancies)
        flag = 1

    if flag == 1:
        print("cleaning duplicates")
        cleaned_df = remove_duplicate_months(filtered_df)

        # Get counts of rows per patient and identify discrepancies
        discrepancies = count_rows_per_patient(cleaned_df)

        if discrepancies.empty:
            print("All patients have exactly 5 records.")
            # Save the filtered DataFrame to a new CSV file
            save_filtered_data(cleaned_df, output_filename)
        else:
            print("Patients not having exactly 5 records:")
            print(discrepancies)

    



if __name__ == '__main__':
    main()
