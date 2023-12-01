import pandas as pd
from os import listdir
from collections import defaultdict


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def clean_census():
     # Get the list of CSV files
    dir = 'Data/Census'
    filenames = find_csv_filenames(dir)

    for csv in filenames:

        # Read the CSV file, skipping first 9 and last 8 rows
        df = pd.read_csv(dir + '/' + csv, skiprows=9, skipfooter=8, engine='python', encoding='latin-1')

        #fill blanks from previous row
        df = df.fillna(method='ffill')

        #starting from column 0, find first header that does not contain Unnamed
        for i in range(0, len(df.columns)):
            if 'Unnamed' not in df.columns[i]:
                dropcell = i
                break
        
        for column in range(dropcell+1, len(df.columns)):
            #fill blanks from previous row
            df.iloc[0,column] = df.columns[column]

        #make first row the header
        df.columns = df.iloc[0]
        #drop first row
        df = df.drop(df.index[0])
        #drop columns without data
        df = df.dropna(axis=1, how='all')
        #rename df to csv name
        df.name = csv[:-4]

        #make all headers uppercase
        df.columns = df.columns.str.upper()
        
        #add column CENSUS_YEAR, which is last two digits of csv name
        df['CENSUS_YEAR'] = '31/12/20' + csv[-6:-4]
        df['CENSUS_YEAR'] = pd.to_datetime(df['CENSUS_YEAR'], format='%d/%m/%Y', dayfirst=True)
        #extract year only
        df['CENSUS_YEAR'] = df['CENSUS_YEAR'].dt.year


         #if csv = SA4Rel_21.csv
        if csv == 'SA4Rel_21.csv':
            df.columns = df.columns.str.replace('HUSBAND, WIFE OR PARTNER IN A', 'PART OF')
            df.columns = df.columns.str.replace('HUSBAND, WIFE OR PARTNER IN A', 'PART OF')
            for header in df.columns:
                if header == 'PART OF REGISTERED MARRIAGE, OPPOSITE-SEX COUPLE':
                    df = df.rename(columns={header: 'PART OF MARRIED COUPLE - M/F'})
                elif header == 'PART OF REGISTERED MARRIAGE, MALE SAME-SEX COUPLE':
                    df = df.rename(columns={header: 'PART OF MARRIED COUPLE - M/M'})
                elif header == 'PART OF REGISTERED MARRIAGE, FEMALE SAME-SEX COUPLE':
                    df = df.rename(columns={header: 'PART OF MARRIED COUPLE - F/F'})
                elif header == 'PART OF REGISTERED MARRIAGE':
                    df = df.rename(columns={header: 'PART OF MARRIED COUPLE'})
            #create new column 'PART OF REGISTERED MARRIAGE', equal to sum of 'PART OF MARRIED COUPLE - M/F', 'PART OF MARRIED COUPLE - M/M', 'PART OF MARRIED COUPLE - F/F'
            df['PART OF MARRIED COUPLE'] = df['PART OF MARRIED COUPLE - M/F'] + df['PART OF MARRIED COUPLE - M/M'] + df['PART OF MARRIED COUPLE - F/F']
        else:
            df.columns = df.columns.str.replace(' (EN)', '')
            df.columns = df.columns.str.replace(' (EN)', '')
            for header in df.columns:
                if 'ENGLP' in header:
                    df = df.rename(columns={header: 'SPOKEN ENGLISH PROFICIENCY'})
                elif 'AGE5P' in header:
                    #rename header AGE
                    df = df.rename(columns={header: 'AGE'})


       
        #save to csv in subfolder Data, with df name
        df.to_csv('Data/Census/Cleaned/' + csv[:-4] + '.csv', index=False)

def census_multiyear():
    # Get the list of CSV files
    dir = 'Data/Census/Cleaned'
    clean_census = find_csv_filenames(dir)
    #create list df_21 and df_16
    list_21 = []
    list_16 = []
    #create empty dataframe "uncommon_headers" with columns "21" and "16"
    uncommon_headers = pd.DataFrame(columns=['Header', 'Year'])
    #for each csv in clean_census
    for csv in clean_census:
        #if csv file ends in _21
        if csv[-6:-4] == '21':
            #add name, excluding _21.csv, to df_21
            list_21.append(csv[:-6])
        #if csv file ends in _16
        elif csv[-6:-4] == '16':
            #add name, excluding _16.csv, to df_16
            list_16.append(csv[:-6])
    #create list of common names
    multiyear = list(set(list_21) & set(list_16))
    list_21 = list(set(list_21) - set(multiyear))
    #add _21 to each entry in df_21
    list_21 = [x + '21' for x in list_21]
    #list_16 is the non-set difference of list_16 and multiyear
    list_16 = list(set(list_16) - set(multiyear))
    #add _16 to each entry in df_16
    list_16 = [x + '16' for x in list_16]


    #for each entry in multiyear
    for entry in multiyear:
        #read csv entry_21.csv
        df_21 = pd.read_csv(dir + '/' + entry + '21.csv')
        #read csv entry_16.csv
        df_16 = pd.read_csv(dir + '/' + entry + '16.csv')
        #make all headers uppercase
        
        #compare headers
        if df_21.columns.equals(df_16.columns):
            #concatenate df_21 and df_16
            df = pd.concat([df_21, df_16])
            df.to_csv('Data/CSV/CensusCompare/' + entry + '1621.csv', index=False)
            #print Has same headers, concatenated and saved as entry_1621.csv
            print('Common headers, merged and saved to CensusCompare/ as ' + entry + '1621.csv')

        else:
            #merge df_21 and df_16 on CENSUS_YEAR
            #check which headers are in both df_21 and df_16
            common_headers = list(set(df_21.columns) & set(df_16.columns))
            #headers in df_21 but not common_headers, as dataframe with header 21
            #add headers in df_21 but not common_headers to uncommon_headers[Header], set uncommon_headers[Year] to 21
            for header in df_21.columns:
                if header not in common_headers:
                    #new row with Header and Year 
                    new_row = pd.DataFrame({'Header': [header], 'Year': [21]})
                    #concat uncommon_headers and new_row
                    uncommon_headers = pd.concat([uncommon_headers, new_row])
            #headers in df_16 but not common_headers, as dataframe with headers H
            #add headers in df_16 but not common_headers to uncommon_headers[Header], set uncommon_headers[Year] to 16
            for header in df_16.columns:
                if header not in common_headers:
                    #new row with Header and Year 
                    new_row = pd.DataFrame({'Header': [header], 'Year': [16]})
                    uncommon_headers = pd.concat([uncommon_headers, new_row])
            #merge on common_headers
            df_1621 = df_21
            df_1621 = df_1621.merge(df_16, on=common_headers)
            #replace any headers _x with _21
            df_1621.columns = df_1621.columns.str.replace('_x', '_21')
            #replace any headers _y with _16
            df_1621.columns = df_1621.columns.str.replace('_y', '_16')
            df_1621.to_csv('Data/CSV/CensusCompare/' + entry + '1621.csv', index=False)
            #print Has uncommon headers, merged on common headers, saved as entry_1621.csv
            print('Some uncommon headers, merged on common headers, saved to CensusCompare/ as ' + entry + '1621.csv')
    #for each entry in df_21
    for entry in list_21:
        #file name = entry+ _21.csv
        file_name = entry + '.csv'
        dir = 'Data/Census/Cleaned/'
        #read csv file_name
        df = pd.read_csv(dir + file_name)
        df.to_csv('Data/CSV/SingleYearCensus/' + file_name, index=False)
        #print 2021 data only, saved as file_name
        print('2021 data only, saved to /SingleYearCensus as ' + file_name)
    for entry in list_16:
        #file name = entry+ 16.csv
        file_name = entry + '.csv'
        dir = 'Data/Census/Cleaned/'
        #read csv file_name
        df = pd.read_csv(dir + file_name)
        df.to_csv('Data/CSV/SingleYearCensus/' + file_name, index=False)
        #print 2016 data only, saved as file_name
        print('2016 data only, saved to /SingleYearCensus as ' + file_name)

    #get uncommon_headers distinct
    uncommon_headers = uncommon_headers.drop_duplicates(subset=['Header'])
    #save uncommon_headers to csv
    uncommon_headers.to_csv('Data/Census/Cleaned/uncommon_headers.csv', index=False)

def get_SHS():
    # Load the Excel file
    file_path = 'Data/SHS.xlsx'
    xls = pd.ExcelFile(file_path)

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
            sheet.to_csv('Data/SHS_' + save_sheet_name + '.csv', index=False)
            all_sheets.update({sheet_name: sheet})

def get_data_workbook():
    file_path = 'Data/Data.xlsx'
    xls = pd.ExcelFile(file_path)

    # Read all the sheets into a dictionary of DataFrames
    all_sheets = {sheet_name: pd.read_excel(xls, sheet_name,header=0) for sheet_name in xls.sheet_names}
    xls.close()
    
    summary = defaultdict(dict)  # For storing tab summary


    
    #change sheet_name = Waitlist dataframe
    for sheet_name, df in all_sheets.items():
        if sheet_name == 'Waitlist':
            #separate Item == Waitlist trend into new df, Waitlist_trend
            Waitlist_trend = df[df['Item'] == 'Waitlist trend']
            df = df[df['Item'] != 'Waitlist trend']
            all_sheets.update({'Waitlist': df})

    all_sheets.update({'Waitlist_trend': Waitlist_trend})
        
        
    for sheet_name, df in all_sheets.items():

        if sheet_name == 'Waitlist_trend':
            #pivot table on Date, Category, Subcategory
            df_pivot = df.pivot_table(values='Value', index='Date', columns=['Category', 'Subcategory'], aggfunc='sum').reset_index()    
            df_pivot.columns = [col[0] if col[1] == '' else '_'.join(col) for col in df_pivot.columns.values]
            df_pivot.rename(columns={'Priority Waitlist_Applications': 'priority_applications'}, inplace=True)
            df_pivot.rename(columns={'Priority Waitlist_Individuals': 'priority_individuals'}, inplace=True)
            df_pivot.rename(columns={'Total Waitlist_Applications': 'total_applications'}, inplace=True)
            df_pivot.rename(columns={'Total Waitlist_Individuals': 'total_individuals'}, inplace=True)
            df_pivot = df_pivot[['Date', 'total_applications', 'total_individuals', 'priority_applications', 'priority_individuals']]
            #cast non-null values in total_applications, total_individuals, priority_applications, priority_individuals as int
            df_pivot['total_applications'] = df_pivot['total_applications'].astype('Int64')
            df_pivot['total_individuals'] = df_pivot['total_individuals'].astype('Int64')
            df_pivot['priority_applications'] = df_pivot['priority_applications'].astype('Int64')
            df_pivot['priority_individuals'] = df_pivot['priority_individuals'].astype('Int64')
            df = df_pivot
            all_sheets.update({'Waitlist_trend': df})

    for sheet_name, df in all_sheets.items():
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            #save to csv in subfolder Data, with sheet name.csv name
        df.to_csv('Data/CSV/' + sheet_name + '.csv', index=False)

        # Filter columns
        if sheet_name == "Population":
            filter_cols = ["Region"] 
            if sheet_name in ["Rentals", "Economy", "Stock", "Construction", "Waitlist"]:
                filter_cols.append("Category", "Subcategory", "Region", "Item")
            if sheet_name == "Waitlist":
                filter_cols.append("Detail")
                distinct_combinations = df[filter_cols].drop_duplicates().to_dict(orient='records')
            if sheet_name == "Waitlist_trend":
                filter_cols.append("total_applications", "total_individuals", "priority_applications", "priority_individuals")

        elif sheet_name == "Bonds":
            # Date Range
            summary[sheet_name]["Date Range"] = (df["Date"].min(), df["Date"].max())
            # Data Series (excluding the "Date" column)
            summary[sheet_name]["Data Series"] = list(df.columns)
            #remove Date from Data Series
            summary[sheet_name]["Data Series"].remove("Date")

        elif sheet_name == "ROGS2022":
            filter_cols = ["Year", "Measure", "Age", "Indigenous_Status", "Remoteness", "Service_Type",
                           "Client_Type", "Description1", "Description2", "Description3",
                           "Description4", "Description5", "Description6"]
            
            distinct_combinations = df[filter_cols].drop_duplicates().to_dict(orient='records')
            summary[sheet_name]["Filters"] = distinct_combinations
        
    
    return summary



