import pandas as pd

SHS_Reasons = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/SHS/Long_Form/SHS_Reasons_Long_Form.csv')
SHS_Clients = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/SHS/Long_Form/SHS_Clients_Long_Form.csv')

SHS_Groups = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/SHS/Long_Form/SHS_Client_Groups_Long_Form.csv')
Rentals = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Market/Rentals.csv')
Waitlist_trend = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Public_housing/Waitlist_trend_long.csv')
Bonds = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Market/Bonds.csv')
Construction = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Market/Construction.csv')
Economy = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Market/Economy.csv')
SH_Stock = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Public_housing/Stock.csv')
Waitlist_breakdowns = pd.read_csv('/Users/yhanalucas/Desktop/Nov/Data/Public_housing/Waitlist_breakdowns.csv')

content = {}
files_dict = {}
times = {}

files = [SHS_Reasons, SHS_Clients, SHS_Groups, Rentals, Waitlist_trend, Bonds, Construction, Economy, SH_Stock, Waitlist_breakdowns]
file_names = ['SHS_Reasons', 'SHS_Clients', 'SHS_Groups', 'Rentals', 'Waitlist_trend', 'Bonds', 'Construction', 'Economy', 'SH_Stock', 'Waitlist_breakdowns']

SHS_Reasons_dict, SHS_Clients_dict, SHS_Groups_dict, Rentals_dict, Waitlist_trend_dict, Bonds_dict, Construction_dict, Economy_dict, SH_Stock_dict, Waitlist_breakdowns_dict = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}


for file in files:
    # make column names uppercase
    file.columns = map(str.upper, file.columns)
    # if column name contains 'DATE':
    if 'DATE' in file.columns:
        if file.dtypes['DATE'] == 'object' and file['DATE'].str.len().max() == 5:
            file['DATE'] = file['DATE'].str[:3] + '-' + file['DATE'].str[3:]
            file['DATE'] = pd.to_datetime(file['DATE'], format='%b-%y')
        elif file.dtypes['DATE'] == 'object' and file['DATE'].str.contains('-').any():
            file['DATE'] = file['DATE'].str.replace('-', '/')
        # if any DATE value has / in 5th position
        elif file.dtypes['DATE'] == 'object' and file['DATE'][0][4] == '/':
            file['DATE'] = pd.to_datetime(file['DATE'], format='%Y/%m/%d')
        elif file.dtypes['DATE'] == 'object':
            file['DATE'] = pd.to_datetime(file['DATE'], dayfirst=True, errors='coerce')
        else:
            pass

files_dict = dict(zip(file_names, files))

for key, df in files_dict.items():
    content_df = df
    content_df = content_df.select_dtypes(include=['object'])
    content[key] = content_df.columns.tolist()

for key, columnlist in content.items():
    for column in columnlist:
        if 'DATE' in column:
            pass
        elif 'MONTH' in column:
            pass
        else:
            unique_values = files_dict[key][column].unique()
            #make unique_values a df
            unique_values = pd.DataFrame(unique_values, columns=[column])
            #make unique_values['Dataset'] = key
            unique_values['Dataset'] = key
            if key == 'SHS_Reasons':
                SHS_Reasons_dict[column] = unique_values
            elif key == 'SHS_Clients':
                SHS_Clients_dict[column] = unique_values
            elif key == 'SHS_Groups':
                SHS_Groups_dict[column] = unique_values
            elif key == 'Rentals':
                Rentals_dict[column] = unique_values
            elif key == 'Waitlist_trend':
                Waitlist_trend_dict[column] = unique_values
            elif key == 'Bonds':
                Bonds_dict[column] = unique_values
            elif key == 'Construction':
                Construction_dict[column] = unique_values
            elif key == 'Economy':
                Economy_dict[column] = unique_values
            elif key == 'SH_Stock':
                SH_Stock_dict[column] = unique_values
            elif key == 'Waitlist_breakdowns':
                Waitlist_breakdowns_dict[column] = unique_values
            else:
                pass



for key, df in files_dict.items():
    if 'DATE' in df.columns:
        #time_df = start: DATE.min, end: DATE.max, count: unique(DATE)
        time_df = pd.DataFrame({'start': [df['DATE'].min()], 'end': [df['DATE'].max()], 'count': [len(df['DATE'].unique())]})
        times[key] = time_df
    else:
        pass
