import csv

from os import listdir
from typing import List

import pandas as pd


def find_csv_filenames(path_to_dir: str, suffix: str = ".csv") -> List[str]:
    """
    Returns a list of filenames in the given directory that end with the specified suffix.

    Args:
        path_to_dir (str): The path to the directory to search for files.
        suffix (str, optional): The file extension to search for. Defaults to ".csv".

    Returns:
        List[str]: A list of filenames that end with the specified suffix.
    """
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def create_census_file_details() -> pd.DataFrame:
    """
    This function creates a DataFrame containing details of all the CSV files 
    in the 'Data/Census' directory. The DataFrame is then saved to a CSV file 
    named 'census_file_details.csv' in the 'Data' directory.
    """
    # Get the list of CSV files
    data_dir = 'Data/Census/'
    filenames = find_csv_filenames(data_dir)

    # create file_details with desired columns
    file_details = pd.DataFrame(columns=[
                                'FILE_NAME', 'FILE_DESCRIPTION1', 'FILE_DESCRIPTION2', 'SOURCE1', 'SOURCE2'])

    for file in filenames:
        with open(data_dir + file, encoding='utf-8') as census_file:
            reader = csv.reader(census_file)
            rows = list(reader)

            # Create a dictionary for the current file's details
            current_file_details = {
                'FILE_NAME': file,
                'FILE_DESCRIPTION1': rows[3][0] if len(rows) > 3 else '',
                'FILE_DESCRIPTION2': rows[4][0] if len(rows) > 4 else '',
                'SOURCE1': rows[0][0] if len(rows) > 0 else '',
                'SOURCE2': rows[2][0] if len(rows) > 2 else ''
            }

            # Use pandas.concat to append this dictionary to the DataFrame
            file_details = pd.concat([file_details, pd.DataFrame(
                [current_file_details])], ignore_index=True)

    # Save file_details to csv
    file_details.to_csv('Data/census_file_details.csv', index=False)

    return file_details


create_census_file_details()
