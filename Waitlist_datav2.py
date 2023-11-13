import pandas as pd
import numpy as np

def Waitlist_datav2():

    Waitlist_trend = pd.read_csv('/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend.csv')
    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%Y-%m-%d')
    Waitlist_trend = Waitlist_trend.sort_values(by='Date', ascending=True)
    
    Waitlist_categories = Waitlist_trend.columns
    Waitlist_categories = Waitlist_categories.drop('Date').to_list()

    Waitlist_trend_monthly_change = pd.DataFrame(columns=['Date', 'Category', 'Value', 'M MonthsElapsed', 'Previous monthly value', 'M Delta', 'M Delta pc pt'])
    Waitlist_trend_yearly_change = pd.DataFrame(columns=['Date', 'Category', 'Value', 'Y MonthsElapsed', 'Prior year value', 'Y Delta', 'Y Delta pc pt'])
    Waitlist_trend_end_last_year = pd.DataFrame(columns=['Date', 'Category', 'Value', 'Date end last year', 'Value end last year', 'YE Delta', 'YE Delta pc pt'])

    
    for category in Waitlist_categories:
        category_df = Waitlist_trend[['Date', category]].copy()
        category_df = category_df.dropna().reset_index(drop=True)
        category_df = category_df.rename(columns={category: 'Value'})
        category_df['Category'] = category
    

        category_df['M MonthsElapsed'] = np.nan
        category_df['Previous monthly value'] = np.nan
        category_df['M Delta'] = np.nan
        category_df['M Delta pc pt'] = np.nan

        category_df['Y MonthsElapsed'] = np.nan
        category_df['Prior year value'] = np.nan
        category_df['Y Delta'] = np.nan
        category_df['Y Delta pc pt'] = np.nan

        years_in_df = category_df['Date'].dt.year.unique()
        category_df['Date end last year'] = np.nan
        category_df['Value end last year'] = np.nan
        category_df['YE Delta'] = np.nan
        category_df['YE Delta pc pt'] = np.nan

        last_date_prior_year = {}
        
        for year in years_in_df:
            if year == years_in_df.min():
                continue
            else:
                last_date_prior_year[year] = category_df[category_df['Date'].dt.year == year - 1]['Date'].max()
        last_date_prior_year_value = {}
        for year in years_in_df:
            if year == years_in_df.min():
                continue
            else:
                last_date_prior_year_value[year] = category_df.loc[category_df['Date'] == last_date_prior_year[year], 'Value'].values[0]

        for ind in range (len(category_df)):
            if ind == 0:
                continue
            else:
                category_df.at[category_df.index[ind], 'M MonthsElapsed'] = (category_df.at[category_df.index[ind], 'Date'] - category_df.at[category_df.index[ind-1], 'Date']).days/30
                category_df.at[category_df.index[ind], 'M MonthsElapsed'] = round(category_df.at[category_df.index[ind], 'M MonthsElapsed'])
                category_df.at[category_df.index[ind], 'Previous monthly value'] = category_df.at[category_df.index[ind-1], 'Value']
                category_df.at[category_df.index[ind], 'M Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind-1], 'Value']
                category_df.at[category_df.index[ind], 'M Delta pc pt'] = (category_df.at[category_df.index[ind], 'M Delta'] / category_df.at[category_df.index[ind-1], 'Value']) * 100
                current_date = category_df.at[category_df.index[ind], 'Date']
                prior_year_date = current_date - pd.DateOffset(days=366) + pd.offsets.MonthEnd(0)
                prior_year_proxy_date_1 = prior_year_date + pd.DateOffset(days=1) + pd.offsets.MonthEnd(0)
                prior_year_proxy_date_2 = prior_year_date - pd.DateOffset(days=31) + pd.offsets.MonthEnd(0)
                prior_year_proxy_date_3 = prior_year_date + pd.DateOffset(days=32) + pd.offsets.MonthEnd(0)
                prior_year_proxy_date_4 = prior_year_date - pd.DateOffset(days=62) + pd.offsets.MonthEnd(0)
                
                if prior_year_date in category_df['Date'].values:
                    filtered_df = category_df[category_df['Date'] == prior_year_date]
                    if not filtered_df.empty:
                        prior_year_value = filtered_df['Value'].values[0]
                        category_df.at[category_df.index[ind], 'Prior year value'] = prior_year_value
                        category_df.at[category_df.index[ind], 'Y Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind], 'Prior year value']
                        category_df.at[category_df.index[ind], 'Y Delta pc pt'] = (category_df.at[category_df.index[ind], 'Y Delta'] / category_df.at[category_df.index[ind], 'Prior year value']) * 100
                    else:
                        category_df.at[category_df.index[ind], 'Prior year value'] = np.nan
                elif prior_year_proxy_date_1 in category_df['Date'].values:
                    category_df.at[category_df.index[ind], 'Y MonthsElapsed'] = 11
                    filtered_df = category_df[category_df['Date'] == prior_year_proxy_date_1]
                    if not filtered_df.empty:
                        prior_year_value = filtered_df['Value'].values[0]
                        category_df.at[category_df.index[ind], 'Prior year value'] = prior_year_value
                        category_df.at[category_df.index[ind], 'Y Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind], 'Prior year value']
                        category_df.at[category_df.index[ind], 'Y Delta pc pt'] = (category_df.at[category_df.index[ind], 'Y Delta'] / category_df.at[category_df.index[ind], 'Prior year value']) * 100
                    else:
                        category_df.at[category_df.index[ind], 'Prior year value'] = np.nan
                
                elif prior_year_proxy_date_2 in category_df['Date'].values:
                    category_df.at[category_df.index[ind], 'Y MonthsElapsed'] = 13
                    filtered_df = category_df[category_df['Date'] == prior_year_proxy_date_2]
                    if not filtered_df.empty:
                        prior_year_value = filtered_df['Value'].values[0]
                        category_df.at[category_df.index[ind], 'Prior year value'] = prior_year_value
                        category_df.at[category_df.index[ind], 'Y Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind], 'Prior year value']
                        category_df.at[category_df.index[ind], 'Y Delta pc pt'] = (category_df.at[category_df.index[ind], 'Y Delta'] / category_df.at[category_df.index[ind], 'Prior year value']) * 100
                    else:
                        category_df.at[category_df.index[ind], 'Prior year value'] = np.nan
                    
                elif prior_year_proxy_date_3 in category_df['Date'].values:    
                    category_df.at[category_df.index[ind], 'Y MonthsElapsed'] = 10
                    filtered_df = category_df[category_df['Date'] == prior_year_proxy_date_3]
                    if not filtered_df.empty:
                        prior_year_value = filtered_df['Value'].values[0]
                        category_df.at[category_df.index[ind], 'Prior year value'] = prior_year_value
                        category_df.at[category_df.index[ind], 'Y Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind], 'Prior year value']
                        category_df.at[category_df.index[ind], 'Y Delta pc pt'] = (category_df.at[category_df.index[ind], 'Y Delta'] / category_df.at[category_df.index[ind], 'Prior year value']) * 100
                    else:
                        category_df.at[category_df.index[ind], 'Prior year value'] = np.nan
                    
                elif prior_year_proxy_date_4 in category_df['Date'].values:
                    category_df.at[category_df.index[ind], 'Y MonthsElapsed'] = 14
                    filtered_df = category_df[category_df['Date'] == prior_year_proxy_date_3]
                    if not filtered_df.empty:
                        prior_year_value = filtered_df['Value'].values[0]
                        category_df.at[category_df.index[ind], 'Prior year value'] = prior_year_value
                        category_df.at[category_df.index[ind], 'Y Delta'] = category_df.at[category_df.index[ind], 'Value'] - category_df.at[category_df.index[ind], 'Prior year value']
                        category_df.at[category_df.index[ind], 'Y Delta pc pt'] = (category_df.at[category_df.index[ind], 'Y Delta'] / category_df.at[category_df.index[ind], 'Prior year value']) * 100
                    else:
                        category_df.at[category_df.index[ind], 'Prior year value'] = np.nan
            
        for ind in range(len(category_df)):
            if category_df.loc[category_df.index[ind], 'Date'].year == years_in_df.min():
                continue
            else:
                category_df.at[ind, 'Date end last year'] = last_date_prior_year[category_df.loc[category_df.index[ind], 'Date'].year]
                category_df.at[ind, 'Value end last year'] = last_date_prior_year_value[category_df.loc[category_df.index[ind], 'Date'].year]
                category_df.at[ind, 'YE Delta'] = category_df.loc[category_df.index[ind], 'Value'] - category_df.loc[category_df.index[ind], 'Value end last year']
                category_df.at[ind, 'YE Delta pc pt'] = (category_df.loc[category_df.index[ind], 'YE Delta'] / category_df.loc[category_df.index[ind], 'Value end last year']) * 100

        Waitlist_trend_monthly_change = pd.concat([Waitlist_trend_monthly_change, category_df], ignore_index=True)
        Waitlist_trend_yearly_change = pd.concat([Waitlist_trend_yearly_change, category_df], ignore_index=True)
        Waitlist_trend_end_last_year = pd.concat([Waitlist_trend_end_last_year, category_df], ignore_index=True)
    

    return Waitlist_trend, Waitlist_trend_monthly_change, Waitlist_trend_yearly_change, Waitlist_trend_end_last_year

    
