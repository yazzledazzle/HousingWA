
import os
from os import listdir
import pandas as pd
import openpyxl
from openpyxl import load_workbook

def delete_source_file(file):
    if os.path.exists(file):
        os.remove(file)
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

def get_airbnb():
    filenames = listdir('DATA/SOURCE DATA/Market and economy/Airbnb')
    airbnb0 = 'DATA/PROCESSED DATA/Market and economy/airbnb_summary.csv'
    dfs = {}
    df_summaries = {}

    for filename in filenames:
        df_name = filename[:10]
        df = pd.read_csv('DATA/SOURCE DATA/Market and economy/Airbnb/' + filename)
        dfs[df_name] = df

    for df_name, df in dfs.items():
        df_summary_name = f"{df_name}_summary"
        #group by room_type, neighbourhood, column for count, calculate mean and median price, mean and median availability_365, store as row in df_summary
        df = df.groupby(['neighbourhood', 'room_type']).agg({'id': 'count', 'price': ['mean', 'median'], 'availability_365': ['mean', 'median']})
        #rename 2 level column names - price mean to mean_price, price median to median_price, availability_365 mean to mean_availability_365, availability_365 median to median_availability_365
        df.columns = ['_'.join(col) for col in df.columns]
        #col1 name = neighbourhood, col2 name = room_type, col3 name = count
        df = df.reset_index()
        #rename count column to count_listings
        df = df.rename(columns={'id_count': 'count_listings'})
        #add column for date
        df['date'] = df_name
        #add df to df_summary
        df_summaries[df_summary_name] = df

    #concatenate all df_summary_name dfs in df_summaries
    df_summary = pd.concat(df_summaries.values())


    latest_date = df_summary['date'].max()
    latest_date = pd.to_datetime(latest_date).strftime('%d/%m/%Y')
    
    #try read csv airbnb0, concatenate df_summary to airbnb0, save as airbnb_summary.csv
    try:
        airbnb0 = pd.read_csv('DATA/PROCESSED DATA/Market and economy/airbnb_summary.csv')
        airbnb0 = pd.concat([airbnb0, df_summary])
        #drop duplicates
        airbnb0 = airbnb0.drop_duplicates()
        airbnb0.to_csv('DATA/PROCESSED DATA/Market and economy/airbnb_summary.csv', index=False)
        update_log(latest_date, pd.to_datetime('today'), 'Airbnb')
        for filename in filenames:
            delete_source_file('DATA/SOURCE DATA/Market and economy/Airbnb/' + filename)
    except:
        df_summary.to_csv('DATA/PROCESSED DATA/Market and economy/airbnb_summary.csv', index=False)
        update_log(latest_date, pd.to_datetime('today'), 'Airbnb')
        for filename in filenames:
            delete_source_file('DATA/SOURCE DATA/Market and economy/Airbnb/' + filename)
    return


get_airbnb()










