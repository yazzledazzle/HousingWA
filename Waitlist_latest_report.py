import pandas as pd
from Waitlist_data import *  


def Create_waitlist_latest_reports():
    Waitlist_trend, Waitlist_trend_rolling_average, Waitlist_trend_monthly_change, Waitlist_trend_yearly_change, Waitlist_trend_end_last_year = Waitlist_data()
    Waitlist_latest_report = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Change', 'Annual change', 'Rolling average delta', 'Prior year end delta', 'Note Monthly', 'Note Annual', 'Note Rolling average', 'Note prior year end'])
    Waitlist_latest_report_pc_pt = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Change_pc_pt', 'Annual_change_pc_pt', 'Rolling_average_delta_pc_pt', 'Prior_year_end_delta_pc_pt', 'Note Monthly', 'Note Annual', 'Note Rolling average', 'Note prior year end'])
    categories = ['total_applications', 'total_individuals', 'priority_applications', 'priority_individuals']
    index = 0
    for category in categories:
        df = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Change', 'Annual change', 'Rolling average delta', 'Prior year end delta', 'Note Monthly', 'Note Annual', 'Note Rolling average', 'Note prior year end'])
        df_pc = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Change_pc_pt', 'Annual_change_pc_pt', 'Rolling_average_delta_pc_pt', 'Prior_year_end_delta_pc_pt', 'Note Monthly', 'Note Annual', 'Note Rolling average', 'Note prior year end'])
        #filter dataframes for category = category
        Waitlist_trend_latest = Waitlist_trend[['Date', category]]
        Waitlist_trend_monthly_change_latest = Waitlist_trend_monthly_change[Waitlist_trend_monthly_change['Category'] == category]
        Waitlist_trend_yearly_change_latest = Waitlist_trend_yearly_change[Waitlist_trend_yearly_change['Category'] == category]
        Waitlist_trend_rolling_average_latest = Waitlist_trend_rolling_average[Waitlist_trend_rolling_average['Category'] == category]
        Waitlist_trend_end_last_year_latest = Waitlist_trend_end_last_year[Waitlist_trend_end_last_year['Category'] == category]
        #filter for latest date
        Waitlist_trend_latest = Waitlist_trend_latest[Waitlist_trend_latest['Date'] == Waitlist_trend_latest['Date'].max()]
        Waitlist_trend_monthly_change_latest = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Date'] == Waitlist_trend_monthly_change_latest['Date'].max()]
        Waitlist_trend_yearly_change_latest = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Date'] == Waitlist_trend_yearly_change_latest['Date'].max()]
        Waitlist_trend_rolling_average_latest = Waitlist_trend_rolling_average_latest[Waitlist_trend_rolling_average_latest['Date'] == Waitlist_trend_rolling_average_latest['Date'].max()]
        Waitlist_trend_end_last_year_latest = Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Date'] == Waitlist_trend_end_last_year_latest['Date'].max()]

        df.loc[index, 'Group'] = 'Total' if 'total' in category else 'Priority'
        df_pc.loc[index, 'Group'] = 'Total' if 'total' in category else 'Priority'
        df.loc[index, 'Count'] = 'Applications' if 'applications' in category else 'Individuals'
        df_pc.loc[index, 'Count'] = 'Applications' if 'applications' in category else 'Individuals'
        df.loc[index, 'Date'] = pd.to_datetime(Waitlist_trend_latest['Date'].values[0])
        df.loc[index, 'Date'] = df.loc[index, 'Date'].strftime('%d %b %Y')
        df_pc.loc[index, 'Date'] = pd.to_datetime(Waitlist_trend_latest['Date'].values[0])
        df_pc.loc[index, 'Date'] = df_pc.loc[index, 'Date'].strftime('%d %b %Y')

        df.loc[index, '#'] = Waitlist_trend_latest[category].values[0]
        df_pc.loc[index, '#'] = Waitlist_trend_latest[category].values[0]
        df.loc[index, 'Change'] = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['Delta'].values[0]
        df_pc.loc[index, 'Change_pc_pt'] = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['Delta pc pt'].values[0]
        Waitlist_trend_monthly_change_latest['MonthsElapsed'] = Waitlist_trend_monthly_change_latest['MonthsElapsed'].astype(int)
        if Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['MonthsElapsed'].values[0] == 1:
            df.loc[index, 'Note Monthly'] = None
            df_pc.loc[index, 'Note Monthly'] = None
        else:
            df.loc[index, 'Note Monthly'] = 'Note: Prior month data not available - change calculated based on last figure, from ' + str(Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['MonthsElapsed'].values[0]) + ' months ago.'
            df_pc.loc[index, 'Note Monthly'] = 'Note: Prior month data not available - change calculated based on last figure, from ' + str(Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['MonthsElapsed'].values[0]) + ' months ago.'
        df.loc[index, 'Annual change'] = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Delta'].values[0]
        df_pc.loc[index, 'Annual_change_pc_pt'] = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Delta pc pt'].values[0]
        Waitlist_trend_yearly_change_latest['MonthsElapsed'] = Waitlist_trend_yearly_change_latest['MonthsElapsed'].astype(int)
        if Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['MonthsElapsed'].values[0] == 12:
            df.loc[index, 'Note annual'] = None
            df_pc.loc[index, 'Note annual'] = None
        elif Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['MonthsElapsed'].values[0] == np.nan:
            df.loc[index, 'Note annual'] = 'Note: Data not available'
            df_pc.loc[index, 'Note annual'] = 'Note: Data not available'
        else:
            df.loc[index, 'Note annual'] = 'Note: Data not available for this month last year- change calculated based on closest record, from ' + str(Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['MonthsElapsed'].values[0]) + ' months ago.'
            df_pc.loc[index, 'Note annual'] = 'Note: Data not available for this month last year- change calculated based on closest record, from ' + str(Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['MonthsElapsed'].values[0]) + ' months ago.'
        df.loc[index, 'Rolling average delta'] = Waitlist_trend_rolling_average_latest[Waitlist_trend_rolling_average_latest['Category'] == category]['Delta'].values[0]
        df_pc.loc[index, 'Rolling_average_delta_pc_pt'] = Waitlist_trend_rolling_average_latest[Waitlist_trend_rolling_average_latest['Category'] == category]['Delta pc pt'].values[0]
        Waitlist_trend_rolling_average_latest['RecordsInYear'] = Waitlist_trend_rolling_average_latest['RecordsInYear'].astype(int)
        if Waitlist_trend_rolling_average_latest.loc[Waitlist_trend_rolling_average_latest['Category'] == category]['RecordsInYear'].values[0] == 12:
            df.loc[index, 'Note Rolling average'] = None
            df_pc.loc[index, 'Note Rolling average'] = None
        elif Waitlist_trend_rolling_average_latest.loc[Waitlist_trend_rolling_average_latest['Category'] == category]['RecordsInYear'].values[0] < 6:
            df.loc[index, 'Note Rolling average'] = 'Note: Rolling average not available - less than 6 months of data.'
            df_pc.loc[index, 'Note Rolling average'] = 'Note: Rolling average not available - less than 6 months of data.'
        else: 
            df.loc[index, 'Note Rolling average'] = 'Note: Rolling average calculated based on last ' + str(Waitlist_trend_rolling_average_latest.loc[Waitlist_trend_rolling_average_latest['Category'] == category]['RecordsInYear'].values[0]) + ' data points (monthly values) for the past 12 month period.'
            df_pc.loc[index, 'Note Rolling average'] = 'Note: Rolling average calculated based on last ' + str(Waitlist_trend_rolling_average_latest.loc[Waitlist_trend_rolling_average_latest['Category'] == category]['RecordsInYear'].values[0]) + ' data points (monthly values) for the past 12 month period.'
        df.loc[index, 'Prior year end delta'] = Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Delta'].values[0]
        df_pc.loc[index, 'Prior_year_end_delta_pc_pt'] = Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Delta pc pt'].values[0]
        if Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0].month == 12:
            df.loc[index, 'Note prior year end'] = None
            df_pc.loc[index, 'Note prior year end'] = None
        else:
            df.loc[index, 'Note prior year end'] = 'Note: Prior year end figure from ' + str(Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0])
            df_pc.loc[index, 'Note prior year end'] = 'Note: Prior year end figure from ' + str(Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0])
        Waitlist_latest_report = pd.concat([Waitlist_latest_report, df], ignore_index=True)
        Waitlist_latest_report_pc_pt = pd.concat([Waitlist_latest_report_pc_pt, df_pc], ignore_index=True)
        index += 1

    Waitlist_latest_report['#'] = Waitlist_latest_report['#'].astype(int)
    Waitlist_latest_report['Change'] = Waitlist_latest_report['Change'].astype(int)
    Waitlist_latest_report['Annual change'] = Waitlist_latest_report['Annual change'].astype(int)
    Waitlist_latest_report['Rolling average delta'] = Waitlist_latest_report['Rolling average delta'].astype(int)
    Waitlist_latest_report['Prior year end delta'] = Waitlist_latest_report['Prior year end delta'].astype(int)
    Waitlist_latest_report.to_csv('Waitlist_latest_report.csv')

    Waitlist_latest_report_pc_pt['#'] = Waitlist_latest_report_pc_pt['#'].astype(int)
    Waitlist_latest_report_pc_pt['Change_pc_pt'] = Waitlist_latest_report_pc_pt['Change_pc_pt'].astype(float).round(2)
    Waitlist_latest_report_pc_pt['Annual_change_pc_pt'] = Waitlist_latest_report_pc_pt['Annual_change_pc_pt'].astype(float).round(2)
    Waitlist_latest_report_pc_pt['Rolling_average_delta_pc_pt'] = Waitlist_latest_report_pc_pt['Rolling_average_delta_pc_pt'].astype(float).round(2)
    Waitlist_latest_report_pc_pt['Prior_year_end_delta_pc_pt'] = Waitlist_latest_report_pc_pt['Prior_year_end_delta_pc_pt'].astype(float).round(2)
    Waitlist_latest_report_pc_pt.to_csv('Waitlist_latest_report_pc_pt.csv')
    
    return Waitlist_latest_report, Waitlist_latest_report_pc_pt
