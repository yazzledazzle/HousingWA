import pandas as pd
from Waitlist_datav2 import *  

def Create_waitlist_latest_reports():
    Waitlist_trend, Waitlist_trend_monthly_change, Waitlist_trend_yearly_change, Waitlist_trend_end_last_year = Waitlist_datav2()
    Waitlist_latest_report = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Prior month', 'Prior year', 'Prior year end', 'Note Monthly', 'Note Annual', 'Note prior year end'])
    Waitlist_latest_report_pc_pt = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Prior month (%)', 'Prior year', 'Prior year end', 'Note Monthly', 'Note Annual', 'Note prior year end'])
    categories = ['total_applications', 'total_individuals', 'priority_applications', 'priority_individuals']
    index = 0
    for category in categories:
        df = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Prior month', 'Prior year', 'Prior year end', 'Note Monthly', 'Note Annual', 'Note prior year end'])
        df_pc = pd.DataFrame(columns=['Group', 'Count', 'Date', '#', 'Prior month', 'Prior year', 'Prior year end', 'Note Monthly', 'Note Annual', 'Note prior year end'])
        Waitlist_trend_latest = Waitlist_trend[['Date', category]]
        Waitlist_trend_monthly_change_latest = Waitlist_trend_monthly_change[Waitlist_trend_monthly_change['Category'] == category]
        Waitlist_trend_yearly_change_latest = Waitlist_trend_yearly_change[Waitlist_trend_yearly_change['Category'] == category]
        Waitlist_trend_end_last_year_latest = Waitlist_trend_end_last_year[Waitlist_trend_end_last_year['Category'] == category]
        Waitlist_trend_latest = Waitlist_trend_latest[Waitlist_trend_latest['Date'] == Waitlist_trend_latest['Date'].max()]
        Waitlist_trend_monthly_change_latest = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Date'] == Waitlist_trend_monthly_change_latest['Date'].max()]
        Waitlist_trend_yearly_change_latest = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Date'] == Waitlist_trend_yearly_change_latest['Date'].max()]
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
        df.loc[index, 'Prior month'] = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['M Delta'].values[0]
        df_pc.loc[index, 'Prior month (%)'] = Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['M Delta pc pt'].values[0]
        Waitlist_trend_monthly_change_latest['M MonthsElapsed'] = Waitlist_trend_monthly_change_latest['M MonthsElapsed']
        if Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['M MonthsElapsed'].values[0] == 1:
            df.loc[index, 'Note Monthly'] = None
            df_pc.loc[index, 'Note Monthly'] = None
        else:
            df.loc[index, 'Note Monthly'] = 'Prior month data not available for ' + category + ' - change calculated based on last figure, from ' + str(Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['M MonthsElapsed'].values[0]) + ' months ago.'
            df_pc.loc[index, 'Note Monthly'] = 'Prior month data not available for ' + category + ' - change calculated based on last figure, from ' + str(Waitlist_trend_monthly_change_latest[Waitlist_trend_monthly_change_latest['Category'] == category]['M MonthsElapsed'].values[0]) + ' months ago.'
        df.loc[index, 'Prior year'] = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y Delta'].values[0]
        df_pc.loc[index, 'Prior year'] = Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y Delta pc pt'].values[0]
        Waitlist_trend_yearly_change_latest['Y MonthsElapsed'] = Waitlist_trend_yearly_change_latest['Y MonthsElapsed']
        if Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y MonthsElapsed'].values[0] == 12:
            df.loc[index, 'Note annual'] = None
            df_pc.loc[index, 'Note annual'] = None
        elif Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y MonthsElapsed'].values[0] == np.nan:
            df.loc[index, 'Note annual'] = 'No year prior comparison available for ' + category + ' (including within two months).'
            df_pc.loc[index, 'Note annual'] = 'No year prior comparison available for ' + category + '(including within two months).'
        else:
            df.loc[index, 'Note annual'] = 'Approximate prior year comparison only for ' + category + ' data not available for same month prior year, nearby data point used as proxy (from ' + str(Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y MonthsElapsed'].values[0]) + ' months ago).'
            df_pc.loc[index, 'Note annual'] = 'Approximate prior year comparison only for ' + category + ' data not available for same month prior year, nearby data point used as proxy (from ' + str(Waitlist_trend_yearly_change_latest[Waitlist_trend_yearly_change_latest['Category'] == category]['Y MonthsElapsed'].values[0]) + ' months ago).'
        
        df.loc[index, 'Prior year end'] = Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['YE Delta'].values[0]
        df_pc.loc[index, 'Prior year end'] = Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['YE Delta pc pt'].values[0]
        if Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0].month == 12:
            df.loc[index, 'Note prior year end'] = None
            df_pc.loc[index, 'Note prior year end'] = None
        else:
            df.loc[index, 'Note prior year end'] = 'December ' + category + ' data not available for prior year; end of prior year comparison uses record from ' + str(Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0])
            df_pc.loc[index, 'Note prior year end'] = 'December ' + category + ' data not available for prior year; end of prior year comparison uses record from ' + str(Waitlist_trend_end_last_year_latest[Waitlist_trend_end_last_year_latest['Category'] == category]['Date end last year'].values[0])
        Waitlist_latest_report = pd.concat([Waitlist_latest_report, df], ignore_index=True)
        Waitlist_latest_report_pc_pt = pd.concat([Waitlist_latest_report_pc_pt, df_pc], ignore_index=True)
        index += 1


    #create Waitlist_latest_report_full, which is Waitlist_latest_report + columns 'Prior month (%)', 'Prior year', 'Prior year end' from Waitlist_latest_report_pc_pt
    Waitlist_latest_report_full = Waitlist_latest_report
    Waitlist_latest_report_full['Prior month %'] = Waitlist_latest_report_pc_pt['Prior month (%)']
    Waitlist_latest_report_full['Prior year %'] = Waitlist_latest_report_pc_pt['Prior year']
    Waitlist_latest_report_full['Prior year end %'] = Waitlist_latest_report_pc_pt['Prior year end']

    #reorder columns so Prior month % before Prior month, Prior year % before Prior year, etc.
    Waitlist_latest_report_full = Waitlist_latest_report_full[['Group', 'Count', 'Date', '#', 'Prior month %', 'Prior month', 'Prior year %', 'Prior year', 'Prior year end %', 'Prior year end', 'Note Monthly', 'Note Annual', 'Note prior year end']]
    Waitlist_latest_report_full.to_csv('Waitlist_latest_report_full2.csv')

    return Waitlist_latest_report, Waitlist_latest_report_pc_pt, Waitlist_latest_report_full
