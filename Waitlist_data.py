import pandas as pd
import numpy as np

def Waitlist_data():

    Waitlist_trend = pd.read_csv('/Users/yhanalucas/Desktop/Dashv1/Data/CSV/Public_housing/Waitlist_trend.csv')
    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%Y-%m-%d')
    Waitlist_trend = Waitlist_trend.sort_values(by='Date', ascending=True)
    
    Waitlist_categories = Waitlist_trend.columns
    Waitlist_categories = Waitlist_categories.drop('Date')
    
    Waitlist_trend_rolling_average = pd.DataFrame(columns=['Date', 'Category', 'Value', 'RecordsInYear', 'Rolling average', 'Delta', 'Delta pc pt'])
    Waitlist_trend_monthly_change = pd.DataFrame(columns=['Date', 'Category', 'Value', 'MonthsElapsed', 'Previous monthly value', 'Delta', 'Delta pc pt'])
    Waitlist_trend_yearly_change = pd.DataFrame(columns=['Date', 'Category', 'Value', 'MonthsElapsed', 'Prior year value', 'Delta', 'Delta pc pt'])
    Waitlist_trend_end_last_year = pd.DataFrame(columns=['Date', 'Category', 'Value', 'Date end last year', 'Value end last year', 'Delta', 'Delta pc pt'])
    for category in Waitlist_categories:
        RA_df = Waitlist_trend[['Date', category]]
        RA_df['Category'] = category
        RA_df = RA_df.dropna().reset_index(drop=True)
        RA_df = RA_df.rename(columns={category: 'Value'})
        RA_df['RecordsInYear'] = RA_df.apply(lambda row: RA_df[(RA_df['Date'] > row['Date'] - pd.DateOffset(months=12)) & (RA_df['Date'] <= row['Date'])]['Value'].count(), axis=1)
        RA_df['Rolling average'] = np.nan
        for ind in range(len(RA_df)):
            if RA_df.loc[RA_df.index[ind], 'RecordsInYear'] < 6:
                RA_df['Rolling average'][ind] = np.nan
            else:
                RA_df.loc[RA_df.index[ind], 'Rolling average'] = RA_df.Value.rolling(RA_df.loc[RA_df.index[ind], 'RecordsInYear']).mean()[ind].round(2).astype(float)
                RA_df.loc[RA_df.index[ind], 'Delta'] = RA_df.loc[RA_df.index[ind], 'Value'] - RA_df.loc[RA_df.index[ind], 'Rolling average']
                RA_df.loc[RA_df.index[ind], 'Delta pc pt'] = (RA_df.loc[RA_df.index[ind], 'Delta'] / RA_df.loc[RA_df.index[ind], 'Rolling average']) * 100
        Waitlist_trend_rolling_average = pd.concat([Waitlist_trend_rolling_average, RA_df], ignore_index=True)

    for category in Waitlist_categories:
        MC_df = Waitlist_trend[['Date', category]]
        MC_df['Category'] = category
        MC_df = MC_df.dropna().reset_index(drop=True)
        MC_df = MC_df.rename(columns={category: 'Value'})
        #Monthly Change process
        MC_df['MonthsElapsed'] = np.nan
        MC_df['Previous monthly value'] = np.nan
        MC_df['Delta'] = np.nan
        MC_df['Delta pc pt'] = np.nan
        for ind in range (len(MC_df)):
            if ind == 0:
                continue
            else:
                MC_df['MonthsElapsed'][ind] = (MC_df.loc[MC_df.index[ind], 'Date'] - MC_df.loc[MC_df.index[ind-1], 'Date']).days/30
                MC_df['MonthsElapsed'][ind] = round(MC_df.loc[MC_df.index[ind], 'MonthsElapsed'])
                MC_df['Previous monthly value'][ind] = MC_df.loc[MC_df.index[ind-1], 'Value']
                MC_df['Delta'][ind] = MC_df.loc[MC_df.index[ind], 'Value'] - MC_df.loc[MC_df.index[ind-1], 'Value']
                MC_df['Delta pc pt'][ind] = (MC_df.loc[MC_df.index[ind], 'Delta'] / MC_df.loc[MC_df.index[ind-1], 'Value']) * 100
        Waitlist_trend_monthly_change = pd.concat([Waitlist_trend_monthly_change, MC_df], ignore_index=True)

    for category in Waitlist_categories:
        YA_df = Waitlist_trend[['Date', category]]
        YA_df['Category'] = category
        YA_df = YA_df.dropna().reset_index(drop=True)
        YA_df = YA_df.rename(columns={category: 'Value'})
        #Yearly Change process
        YA_df['MonthsElapsed'] = np.nan
        YA_df['Prior year value'] = np.nan
        YA_df['Delta'] = np.nan
        YA_df['Delta pc pt'] = np.nan
        for ind in range (len(YA_df)):
            if ind == 0:
                continue
            else:
                current_date = YA_df.loc[YA_df.index[ind], 'Date']
                prior_year_date = current_date - pd.DateOffset(months=12)
                if prior_year_date in YA_df['Date'].values:
                    YA_df['MonthsElapsed'][ind] = 12
                    YA_df['Prior year value'][ind] = YA_df.loc[YA_df['Date'] == prior_year_date, 'Value'].values[0]
                    YA_df['Delta'][ind] = YA_df.loc[YA_df.index[ind], 'Value'] - YA_df.loc[YA_df.index[ind], 'Prior year value']
                    YA_df['Delta pc pt'][ind] = (YA_df.loc[YA_df.index[ind], 'Delta'] / YA_df.loc[YA_df.index[ind], 'Prior year value']) * 100
                elif prior_year_date - pd.DateOffset(months=1) in YA_df['Date'].values:
                    YA_df['MonthsElapsed'][ind] = 13
                    YA_df['Prior year value'][ind] = YA_df.loc[YA_df['Date'] == prior_year_date - pd.DateOffset(months=1), 'Value'].values[0]
                    YA_df['Delta'][ind] = YA_df.loc[YA_df.index[ind], 'Value'] - YA_df.loc[YA_df.index[ind], 'Prior year value']
                    YA_df['Delta pc pt'][ind] = (YA_df.loc[YA_df.index[ind], 'Delta'] / YA_df.loc[YA_df.index[ind], 'Prior year value']) * 100
                elif prior_year_date + pd.DateOffset(months=1) in YA_df['Date'].values:
                    YA_df['MonthsElapsed'][ind] = 11
                    YA_df['Prior year value'][ind] = YA_df.loc[YA_df['Date'] == prior_year_date + pd.DateOffset(months=1), 'Value'].values[0]
                    YA_df['Delta'][ind] = YA_df.loc[YA_df.index[ind], 'Value'] - YA_df.loc[YA_df.index[ind], 'Prior year value']
                    YA_df['Delta pc pt'][ind] = (YA_df.loc[YA_df.index[ind], 'Delta'] / YA_df.loc[YA_df.index[ind], 'Prior year value']) * 100
                elif prior_year_date - pd.DateOffset(months=2) in YA_df['Date'].values:
                    YA_df['MonthsElapsed'][ind] = 14
                    YA_df['Prior year value'][ind] = YA_df.loc[YA_df['Date'] == prior_year_date - pd.DateOffset(months=2), 'Value'].values[0]
                    YA_df['Delta'][ind] = YA_df.loc[YA_df.index[ind], 'Value'] - YA_df.loc[YA_df.index[ind], 'Prior year value']
                    YA_df['Delta pc pt'][ind] = (YA_df.loc[YA_df.index[ind], 'Delta'] / YA_df.loc[YA_df.index[ind], 'Prior year value']) * 100
                elif prior_year_date + pd.DateOffset(months=1) in YA_df['Date'].values:
                    YA_df['MonthsElapsed'][ind] = 10
                    YA_df['Prior year value'][ind] = YA_df.loc[YA_df['Date'] == prior_year_date + pd.DateOffset(months=2), 'Value'].values[0]
                    YA_df['Delta'][ind] = YA_df.loc[YA_df.index[ind], 'Value'] - YA_df.loc[YA_df.index[ind], 'Prior year value']
                    YA_df['Delta pc pt'][ind] = (YA_df.loc[YA_df.index[ind], 'Delta'] / YA_df.loc[YA_df.index[ind], 'Prior year value']) * 100
                else:
                    continue
        Waitlist_trend_yearly_change = pd.concat([Waitlist_trend_yearly_change, YA_df], ignore_index=True)

    for category in Waitlist_categories:
        YE_df = Waitlist_trend[['Date', category]]
        YE_df['Category'] = category
        YE_df = YE_df.dropna().reset_index(drop=True)
        YE_df = YE_df.rename(columns={category: 'Value'})
        years_in_df = YE_df['Date'].dt.year.unique()
        YE_df['Date end last year'] = np.nan
        YE_df['Value end last year'] = np.nan
        YE_df['Delta'] = np.nan
        YE_df['Delta pc pt'] = np.nan
        last_date_prior_year = {}
        for year in years_in_df:
            if year == years_in_df.min():
                continue
            else:
                last_date_prior_year[year] = YE_df[YE_df['Date'].dt.year == year - 1]['Date'].max()
        last_date_prior_year_value = {}
        for year in years_in_df:
            if year == years_in_df.min():
                continue
            else:
                last_date_prior_year_value[year] = YE_df[YE_df['Date'] == last_date_prior_year[year]]['Value'].values[0]
        for ind in range(len(YE_df)):
            if YE_df.loc[YE_df.index[ind], 'Date'].year == years_in_df.min():
                continue
            else:
                YE_df.loc[YE_df.index[ind], 'Date end last year'] = last_date_prior_year[YE_df.loc[YE_df.index[ind], 'Date'].year]
                YE_df.loc[YE_df.index[ind], 'Value end last year'] = last_date_prior_year_value[YE_df.loc[YE_df.index[ind], 'Date'].year]
                YE_df.loc[YE_df.index[ind], 'Delta'] = YE_df.loc[YE_df.index[ind], 'Value'] - YE_df.loc[YE_df.index[ind], 'Value end last year']
                YE_df.loc[YE_df.index[ind], 'Delta pc pt'] = (YE_df.loc[YE_df.index[ind], 'Delta'] / YE_df.loc[YE_df.index[ind], 'Value end last year']) * 100

        Waitlist_trend_end_last_year = pd.concat([Waitlist_trend_end_last_year, YE_df], ignore_index=True)

    return Waitlist_trend, Waitlist_trend_rolling_average, Waitlist_trend_monthly_change, Waitlist_trend_yearly_change, Waitlist_trend_end_last_year
