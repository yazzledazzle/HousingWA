import pandas as pd
from os import listdir

path_to_dir = '/Users/yhanalucas/Desktop/Dashv1/Data/CSV/SHS/'
prefix = 'SHS_'
suffix = '.csv'

def find_csv_filenames(prefix, path_to_dir, suffix):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) and filename.startswith(prefix) ]

def date_to_quarter(date):
    if date.month in [1, 2]:
        return pd.Timestamp(f'31-12-{(date.year)-1}')
    elif date.month in [4, 5]:
        return pd.Timestamp(f'31-03-{date.year}')
    elif date.month in [7, 8]:
        return pd.Timestamp(f'30-06-{date.year}')
    elif date.month in [10, 11]:
        return pd.Timestamp(f'30-09-{date.year}')
    else:
        return date

def convert_case(df):
    # Convert column names to uppercase
    df.columns = [col.upper() for col in df.columns]
    
    # Convert string values in all columns to uppercase
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.capitalize()

    return df

def identify_ignore_columns(dataframes_dict):
    ignore_columns = set()
    for _, df in dataframes_dict.items():
        for column in df.columns:
            if df[column].dtype in ['int64', 'float64']:
                ignore_columns.add(column)
            elif 'datetime64' in str(df[column].dtype):
                ignore_columns.add(column)
            elif column == 'MONTH':  # specifically ignore 'MONTH' column
                ignore_columns.add(column)
    return list(ignore_columns)

def load_and_preprocess_data():
    # Import Population.csv
    Population = pd.read_csv('Data/CSV/Population/Population_State_Sex_Age_to_65+.csv')
    Population = convert_case(Population)
    # date is dd-mm-yyyy
    Population['DATE'] = pd.to_datetime(Population['DATE'], format='%Y-%m-%d')
    # sort by Date ascending
    Population = Population.sort_values(by='DATE', ascending=True)
    Population_all_ages = Population[Population['AGE GROUP'] == 'All ages']
    Population_all_ages = Population_all_ages.drop(['AGE GROUP'], axis=1)
    # sort by Date ascending
    Population_all_ages = Population_all_ages.sort_values(by='DATE', ascending=True)

    # use find_csv_filenames function to find all csv files in Data/CSV/ with prefix 'SHS_' and suffix '.csv', read in
    filenames = find_csv_filenames(prefix, path_to_dir, suffix)
    processed_dataframes = {}
    filters_dict = {}
    filter_select = {}

    # First, iterate over filenames to load the dataframes and store them in processed_dataframes
    for filename in filenames:
        df_name = filename.replace('.csv', '')
        df = pd.read_csv(path_to_dir + filename)
        df = convert_case(df)

        # Drop any rows where specified columns are null / NaN
        cols_to_check = ['NSW','VIC','QLD','WA','SA','TAS','ACT','NT', 'NATIONAL']
        df = df.dropna(subset=cols_to_check)

        # Identify columns that should not be checked for NaN (those with numeric and datetime values)
        ignore_cols = identify_ignore_columns({df_name: df})

        # Columns to check for NaN (non-numeric columns)
        check_for_nan_cols = [col for col in df.columns if col not in ignore_cols]

        # Drop rows where columns (that aren't in ignore_cols) contain NaN values
        df = df.dropna(subset=check_for_nan_cols)

        if 'AGE GROUP' in df.columns:
            if 'All females' in df['AGE GROUP'].unique() or 'All males' in df['AGE GROUP'].unique():
                df = df[~df['AGE GROUP'].isin(['All females', 'All males'])]
                df['AGE GROUP'] = df['AGE GROUP'].str.replace(" years", "")
        
        # Convert Month column to a Date format
        if 'MONTH' in df.columns:
            df['DATE'] = '20' + df['MONTH'].str[3:5] + '-' + df['MONTH'].str[0:3] + '-01'
            df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%b-%d')
            df['DATE'] = df['DATE'] + pd.offsets.MonthEnd(0)
        
        # Sort dataframe by Date ascending
        df = df.sort_values(by='DATE', ascending=True)
        
        processed_dataframes[df_name] = df

    # Next, identify columns to ignore for all dataframes
    ignore_columns = identify_ignore_columns(processed_dataframes)

    filters_dict = {}
    filter_select = {}

    # Separate the loop for filtering 'Total' and 'All ages' from the loop collecting unique values
    for df_name, df in list(processed_dataframes.items()):  # Use list() to prevent runtime issues
        filters = [column for column in df.columns if column not in ignore_columns]
        filters_dict[df_name] = filters
        total_df_name = df_name.replace('SHS_', 'SHS_Total_')

        # Filter 'Total' and 'All ages' rows
        for filter in filters:
            if df[filter].str.contains('Total|All ages').any():
                total_df = df[df[filter].str.contains('Total|All ages')]
                df = df[~df[filter].str.contains('Total|All ages')]
                processed_dataframes[total_df_name] = total_df
                processed_dataframes[df_name] = df

        # This df will not contain rows with 'Total' or 'All ages' anymore
    processed_dataframes[df_name] = df


    # Separate loop for collecting unique values
    for df_name, df in processed_dataframes.items():
        filters = filters_dict.get(df_name, [])
        filter_select[df_name] = {}
        for filter in filters:
            unique_values = list(df[filter].unique())
            filter_select[df_name][filter] = unique_values
    processed_dataframes[df_name] = df

    return processed_dataframes, Population, Population_all_ages, filters_dict, filter_select

def merge_and_calculate(processed_dataframes, Population, Population_all_ages):

    # Convert the 'Date' columns to datetime format for Population DataFrames
    Population['DATE'] = pd.to_datetime(Population['DATE'], format='%Y-%m-%d')
    Population_all_ages['DATE'] = pd.to_datetime(Population_all_ages['DATE'], format='%Y-%m-%d')

    regions = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']

    for df_name, df in processed_dataframes.items():

        # Convert the 'Date' column to datetime format
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['QUARTER'] = df['DATE'].apply(date_to_quarter)

        if 'AGE GROUP' in df.columns:
            merged_df = pd.merge(df, Population, left_on=['QUARTER', 'SEX', 'AGE GROUP'], right_on=['DATE', 'SEX', 'AGE GROUP'], how='left')
        else:
            merged_df = pd.merge(df, Population_all_ages, left_on=['QUARTER', 'SEX'], right_on = ['DATE', 'SEX'], how='left')

        # Drop columns Quarter, Date_y, rename Date_x to Date
        merged_df = merged_df.drop(['QUARTER', 'DATE_y'], axis=1)
        merged_df = merged_df.rename(columns={'DATE_x': 'DATE'})

        # Calculation for National and each region
        merged_df['NATIONAL_PER_10,000'] = merged_df['NATIONAL'] / merged_df['NATIONAL_POPULATION'] * 10000
        for region in regions:
            population_column = f"{region}_POPULATION"
            per_10000_column = f"{region}_PER_10,000"
            merged_df[per_10000_column] = merged_df[region] / merged_df[population_column] * 10000

            proportion_of_national_column = f"{region}_PROPORTION_OF_NATIONAL"
            merged_df[proportion_of_national_column] = merged_df[region] / merged_df['NATIONAL']

            proportion_of_national_per_10000_column = f"{region}_PROPORTION_OF_NATIONAL_PER_10,000"
            merged_df[proportion_of_national_per_10000_column] = merged_df[per_10000_column] / merged_df['NATIONAL_PER_10,000']

        # Store processed DataFrame back in the dictionary
        processed_dataframes[df_name] = merged_df

    return processed_dataframes


processsed_dataframes, Population, Population_all_ages, filters_dict, filter_select = load_and_preprocess_data()
processed_dataframes = merge_and_calculate(processsed_dataframes, Population, Population_all_ages)

