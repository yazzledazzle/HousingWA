import pandas as pd
import os
from os import listdir
from openpyxl import load_workbook

path_to_dir = "DATA/PROCESSED DATA/SHS"
prefix = 'SHS_'
suffix = '.csv'
source_file = 'DATA/SOURCE DATA/ROGS and SHS/SHS.xlsx'
dataset = 'Monthly SHS data from AIHW'

def delete_source_file(file):
    if os.path.exists(source_file):
        os.remove(source_file)
        return
    else:
        return

def update_log(latest_date, update_date, dataset):
    try:
        update_log = pd.read_excel('DATA/SOURCE DATA/update_log.xlsx')
    except:
        update_log = pd.DataFrame(columns=['Dataset', 'Latest data point', 'Date last updated'])
    new_row = pd.DataFrame({'Dataset': [dataset], 'Latest data point': [latest_date], 'Date last updated': [update_date]})
    update_log = pd.concat([update_log, new_row], ignore_index=True)
    update_log['Latest data point'] = pd.to_datetime(update_log['Latest data point'], format='%d/%m/%Y')
    update_log['Date last updated'] = pd.to_datetime(update_log['Date last updated'], format='%d/%m/%Y')
    update_log = update_log.sort_values(by=['Latest data point', 'Date last updated'], ascending=False).drop_duplicates(subset=['Dataset'], keep='first')
    #convert Latest data point and Date last updated to string
    update_log['Latest data point'] = update_log['Latest data point'].dt.strftime('%d/%m/%Y')
    update_log['Date last updated'] = update_log['Date last updated'].dt.strftime('%d/%m/%Y') 
    update_log.to_excel('DATA/SOURCE DATA/update_log.xlsx', index=False)
    book = load_workbook('DATA/SOURCE DATA/update_log.xlsx')
    sheet = book.active
    for column_cells in sheet.columns:
        length = max(len(as_text(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length
    book.save('DATA/SOURCE DATA/update_log.xlsx')
    return

def as_text(value):
    if value is None:
        return ""
    return str(value)

def get_SHS(source_file):
    xls = pd.ExcelFile(source_file)

    # Read all the sheets into a dictionary of DataFrames
    all_sheets = {sheet_name: pd.read_excel(xls, sheet_name, header=3) for sheet_name in xls.sheet_names}
    xls.close()

    #for each sheet in the dictionary
    for sheet_name, sheet in all_sheets.items():
        #check if has at least 100 rows
        if len(sheet) > 100:
            #drop last 2 rows
            sheet = sheet.drop(sheet.index[-2:])
            for col in sheet.columns:
                #if object
                if sheet[col].dtype == 'object':
                    sheet[col] = sheet[col].str.replace(chr(8211), "-").str.replace(chr(8212), "-")

            save_sheet_name = sheet_name.replace(' ', '_')
            sheet.to_csv('DATA/PROCESSED DATA/SHS/SHS_' + save_sheet_name + '.csv', index=False)
            all_sheets.update({sheet_name: sheet})

def find_csv_filenames(prefix, path_to_dir, suffix):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) and filename.startswith(prefix) ]

def date_to_quarter(date):
    if date.month in [1, 2, 3]:
        return pd.Timestamp(f'31-12-{(date.year)-1}')
    elif date.month in [4, 5, 6]:
        return pd.Timestamp(f'31-03-{date.year}')
    elif date.month in [7, 8, 9]:
        return pd.Timestamp(f'30-06-{date.year}')
    elif date.month in [10, 11, 12]:
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
    Population = pd.read_csv('DATA/PROCESSED DATA/Population/Population_State_Sex_Age_to_65+.csv')
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
        df = pd.read_csv(path_to_dir + '/'+ filename)
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
            df['AGE GROUP'] = df['AGE GROUP'].str.replace(chr(45), " to ").str.replace(chr(8211), " to ")
            if 'All females' in df['AGE GROUP'].unique() or 'All males' in df['AGE GROUP'].unique():
                df = df[~df['AGE GROUP'].isin(['All females', 'All males'])]
                df['AGE GROUP'] = df['AGE GROUP'].str.replace(" years", "")

                #group 15-17 and 18-19 into 15-19
                df.loc[df['AGE GROUP'] == '15 to 17', 'AGE GROUP'] = '15 to 19'
                df.loc[df['AGE GROUP'] == '18 to 19', 'AGE GROUP'] = '15 to 19'
                #sum 15 to 19 numerical columns, retain datetime and object columns
                object_cols = [col for col in df.columns if df[col].dtype == 'object']
                datetime_cols = [col for col in df.columns if 'datetime64' in str(df[col].dtype)]
                numeric_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
                df = df.groupby(object_cols + datetime_cols)[numeric_cols].sum().reset_index()
                

        
        # Convert Month column to a Date format
        if 'MONTH' in df.columns:
            df['DATE'] = '20' + df['MONTH'].str[3:5] + '-' + df['MONTH'].str[0:3] + '-01'
            df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%b-%d')
            df['DATE'] = df['DATE'] + pd.offsets.MonthEnd(0)
        
        # Sort dataframe by Date ascending
        df = df.sort_values(by='DATE', ascending=True)
    # Next, identify columns to ignore for all dataframes
    ignore_columns = identify_ignore_columns(processed_dataframes)

    filters_dict = {}
    filter_select = {}

    # Separate the loop for filtering 'Total' and 'All ages' from the loop collecting unique values
    for df_name, df in list(processed_dataframes.items()):  # Use list() to prevent runtime issues
        filters = [column for column in df.columns if column not in ignore_columns]
        filters_dict[df_name] = filters
        total_df_name = df_name.replace('SHS_', 'SHS_Total_')

        if 'AGE GROUP' in df.columns:
            if len(df['AGE GROUP'].unique()) > 1:
                if 'All ages' in df['AGE GROUP'].unique():
                    df = df[df['AGE GROUP'] != 'All ages']
                    processed_dataframes[df_name] = df
                    

        if 'SEX' in df.columns:
            if len(df['SEX'].unique()) > 1:
            #check if Total is in the unique values
                if 'Total' in df['SEX'].unique():
                    total_df = df[df['SEX'] == 'Total']
                    total_df = total_df.drop(['SEX'], axis=1)
                    df = df[df['SEX'] != 'Total']
                    processed_dataframes[df_name] = df
            object_cols = [col for col in total_df.columns if total_df[col].dtype == 'object']
            datetime_cols = [col for col in total_df.columns if 'datetime64' in str(total_df[col].dtype)]
            numeric_cols = [col for col in total_df.columns if total_df[col].dtype in ['int64', 'float64']]
            total_df = total_df.groupby(object_cols + datetime_cols)[numeric_cols].sum().reset_index()
            total_df.to_csv(f'DATA/PROCESSED DATA/SHS/DropSex/{total_df_name}.csv', index=False)
            processed_dataframes[total_df_name] = total_df

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
    
    #replace ['-' or '–' with space in AGE GROUP column
    Population['AGE GROUP'] = Population['AGE GROUP'].str.replace(chr(45), " to ").str.replace(chr(8211), " to ")

    regions = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
    SHS_with_population_calcs = {}

    for df_name, df in processed_dataframes.items():

        # Convert the 'Date' column to datetime format
        df['DATE'] = pd.to_datetime(df['DATE'])
        df['QUARTER'] = df['DATE'].apply(date_to_quarter)

        if 'SEX' in df.columns:
            if 'AGE GROUP' in df.columns:
                merged_df = pd.merge(df, Population, left_on=['QUARTER', 'SEX', 'AGE GROUP'], right_on=['DATE', 'SEX', 'AGE GROUP'], how='left')
            else:
                merged_df = pd.merge(df, Population_all_ages, left_on=['QUARTER', 'SEX'], right_on = ['DATE', 'SEX'], how='left')
        else:
            #filter population SEX = 'Total'
            PopulationNoSex = Population[Population['SEX'] == 'Total']
            PopulationNoSex = PopulationNoSex.drop(['SEX'], axis=1)
            PopulationNoSex = PopulationNoSex.groupby(['DATE', 'AGE GROUP']).sum().reset_index()
            #to csv in Population folder
            PopulationNoSex.to_csv(f'DATA/PROCESSED DATA/Population/PopulationNoSex.csv', index=False)
            Population_all_agesNoSex = Population_all_ages[Population_all_ages['SEX']=='Total']
            Population_all_agesNoSex = Population_all_agesNoSex.drop(['SEX'], axis=1)
            Population_all_agesNoSex = Population_all_agesNoSex.groupby(['DATE']).sum().reset_index()
            #to csv in Population folder
            Population_all_agesNoSex.to_csv(f'DATA/PROCESSED DATA/Population/Population_all_agesNoSex.csv', index=False)


            if 'AGE GROUP' in df.columns:
                merged_df = pd.merge(df, PopulationNoSex, left_on=['QUARTER', 'AGE GROUP'], right_on=['DATE', 'AGE GROUP'], how='left')
            else:
                merged_df = pd.merge(df, Population_all_agesNoSex, left_on=['QUARTER'], right_on = ['DATE'], how='left')

        # Drop columns Quarter, Date_y, rename Date_x to Date
        merged_df = merged_df.drop(['QUARTER', 'DATE_y'], axis=1)
        merged_df = merged_df.rename(columns={'DATE_x': 'DATE'})
        #move Date column to front
        cols = list(merged_df.columns)
        cols.insert(0, cols.pop(cols.index('DATE')))
        merged_df = merged_df[cols]

        # Calculation for National and each region
        merged_df['NATIONAL_PER_10k'] = merged_df['NATIONAL'] / merged_df['NATIONAL_POPULATION'] * 10000
        for region in regions:
            population_column_name = f"{region}_POPULATION"
            per_10000_column = f"{region}_PER_10k"
            merged_df[per_10000_column] = merged_df[region] / merged_df[population_column_name] * 10000

            proportion_of_national_column = f"{region}_PROPORTION_OF_NATIONAL"
            merged_df[proportion_of_national_column] = merged_df[region] / merged_df['NATIONAL']

            proportion_of_national_per_10000_column = f"{region}_PROPORTION_OF_NATIONAL_PER_10k"
            merged_df[proportion_of_national_per_10000_column] = merged_df[per_10000_column] / merged_df['NATIONAL_PER_10k']

            prop_national_pop_column = f"{region}_PROPORTION_OF_NATIONAL_POPULATION"     
            merged_df[prop_national_pop_column] = merged_df[population_column_name] / merged_df['NATIONAL_POPULATION']

            prop_compared_prop_pop = f"{region}_PROPORTION_OF_NATIONAL_COMPARED_TO_PROP_POP"
            merged_df[prop_compared_prop_pop] = merged_df[proportion_of_national_column] / merged_df[prop_national_pop_column]
        # Store processed DataFrame back in the dictionary
        SHS_with_population_calcs[df_name] = merged_df
        #save to csv
        merged_df.to_csv(f'DATA/PROCESSED DATA/SHS/WithPopulation/{df_name}_WithPopulation.csv', index=False)

    return SHS_with_population_calcs

def long_formSHS(SHS_with_population_calcs):
    long_form_dfs = {}
    for df_name, df in SHS_with_population_calcs.items():
        id_vars = ['DATE'] + [col for col in df.columns if df[col].dtype == 'object']
        value_vars = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        long_form_dfs[df_name] = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='MEASURE', value_name='VALUE')
        long_form_dfs[df_name]['MEASURE'] = long_form_dfs[df_name]['MEASURE'].str.replace('_', ' ')
        long_form_dfs[df_name]['MEASURE'] = long_form_dfs[df_name]['MEASURE'].str.lower()
        long_form_dfs[df_name]['MEASURE'] = long_form_dfs[df_name]['MEASURE'].str.capitalize()
            #replace Wa with WA, Nsw with NSW, Sa with SA, Nt with NT, Act with ACT

        #create column State, which is measure before first space
        long_form_dfs[df_name]['STATE'] = long_form_dfs[df_name]['MEASURE'].str.split(' ').str[0]
        #create column Measure, which is remaining measure after moving State to its own column
        long_form_dfs[df_name]['MEASURE'] = long_form_dfs[df_name]['MEASURE'].str.split(' ').str[1:].str.join(' ')
        long_form_dfs[df_name]['STATE'] = long_form_dfs[df_name]['STATE'].str.replace('Wa', 'WA').str.replace('Nsw', 'NSW').str.replace('Sa', 'SA').str.replace('Nt', 'NT').str.replace('Act', 'ACT')
        #move State column to second column
        cols = list(long_form_dfs[df_name].columns)
        cols.insert(1, cols.pop(cols.index('STATE')))
        long_form_dfs[df_name] = long_form_dfs[df_name][cols]
                
        long_form_dfs[df_name].to_csv(f'DATA/PROCESSED DATA/SHS/Long_Form/{df_name}_Long_Form.csv', index=False)
        WA_only_df = long_form_dfs[df_name][long_form_dfs[df_name]['STATE'] == 'WA']
        WA_only_df = WA_only_df.drop(['STATE'], axis=1)
        WA_name = df_name.replace('SHS_', 'SHS_WA_')
        long_form_dfs[WA_name] = WA_only_df

        WA_only_df.to_csv(f'DATA/PROCESSED DATA/SHS/Long_Form/{df_name}_WA_Long_Form.csv', index=False)
        
        delete_source_file(source_file)
        latest_dates = []
    for df_name, df in SHS_with_population_calcs.items():
        latest_date = df['DATE'].max()
        latest_date = pd.to_datetime(latest_date)
        latest_dates.append(latest_date)
    latest_date = max(latest_dates)
    latest_date = pd.to_datetime(latest_date)
    update_date = pd.to_datetime('today').strftime('%d/%m/%Y')
    update_log(latest_date, update_date, dataset)

    return 

def import_shs_data():
    try:
        get_SHS(source_file)
        processsed_dataframes, Population, Population_all_ages, filters_dict, filter_select = load_and_preprocess_data()
        SHS_with_population_calcs = merge_and_calculate(processsed_dataframes, Population, Population_all_ages)
        long_formSHS(SHS_with_population_calcs)
    except:
        pass
    return