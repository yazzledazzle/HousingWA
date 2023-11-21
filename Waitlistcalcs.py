import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def convert_to_long_form(df):
    df_long = df.melt(id_vars=["Date"], 
                      var_name="Category", 
                      value_name="Waitlist figure")
    df_long['Date'] = pd.to_datetime(df_long['Date'])
    df_long = df_long.sort_values(['Category', 'Date'], ascending=[True, True])
    df_long = df_long.dropna(subset=['Waitlist figure'])
    return df_long


def gap_filler(df_long):
    missing_dates = []
    Category_dfs = []
    for Category in df_long['Category'].unique():
        Category_df = df_long[df_long['Category'] == Category].copy()
        for i in range(len(Category_df)-1):
            if Category_df['Date'].iloc[i] + pd.DateOffset(days=1) + pd.offsets.MonthEnd(0) != Category_df['Date'].iloc[i+1]:    
                gap = round((Category_df['Date'].iloc[i+1] - Category_df['Date'].iloc[i]).days / 30) - 1
                diff = Category_df['Waitlist figure'].iloc[i+1] - Category_df['Waitlist figure'].iloc[i]
                for j in range(gap):
                    missing_date = Category_df['Date'].iloc[i] + pd.DateOffset(days=1) + pd.offsets.MonthEnd(0)
                    proxy_value = round(Category_df['Waitlist figure'].iloc[i] + (diff / (gap+1)))
                    missing_dates.append(missing_date)
                    new_row = {'Date': missing_date, 'Category': Category, 'Waitlist figure': proxy_value, 'Estimate flag - Waitlist figure': '^'}
                    Category_df = pd.concat([Category_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)
        Category_dfs.append(Category_df)
    df_long = pd.concat(Category_dfs)
    df_long = df_long.sort_values(by=['Date'])
    df_long = df_long.reset_index(drop=True)
    df_long['Estimate flag - Waitlist figure'] = df_long['Estimate flag - Waitlist figure'].fillna('')
    df_long['Estimate flag - Waitlist figure'] = df_long['Estimate flag - Waitlist figure'].astype(str)
    df_long['Date'] = pd.to_datetime(df_long['Date'])
    df_long['Category'] = df_long['Category'].astype(str)
    df_long['Waitlist figure'] = df_long['Waitlist figure'].astype(float)
    return df_long

def FYtdchange(df_long):
    for Category in df_long['Category'].unique():
        
        df_long_Category = df_long[df_long['Category'] == Category].copy()
        for i, row in df_long_Category.iterrows():
            if row['Date'].month > 6:
                eofy = str(row['Date'].year) + "-06-30"
            else:
                eofy = str((row['Date'].year)-1) + "-06-30"
            eofy = pd.to_datetime(eofy, format='%Y-%m-%d')
            if eofy in df_long_Category['Date'].values:
                df_long_Category.loc[i, 'Difference - financial year to date'] = row['Waitlist figure'] - df_long_Category.loc[df_long_Category['Date']==eofy, 'Waitlist figure'].values[0]
                df_long_Category.loc[i, 'Difference - financial year to date (per cent)'] = df_long_Category.loc[i, 'Difference - financial year to date'] / df_long_Category.loc[df_long_Category['Date']==eofy, 'Waitlist figure'].values[0] * 100 
            else:
                df_long_Category.loc[i, 'Difference - financial year to date'] = float('nan')
                df_long_Category.loc[i, 'Difference - financial year to date (per cent)'] = float('nan')
        df_long = df_long.drop(df_long[df_long['Category'] == Category].index)
        df_long = pd.concat([df_long, df_long_Category])
    return df_long

def calculate_12_month_average(df_long):
    def average_last_12_months(row):
        start_date = row['Date'] - pd.offsets.MonthEnd(12)
        end_date = row['Date']
        filtered_df = df_long[(df_long['Date'] >= start_date) & (df_long['Date'] <= end_date) & (df_long['Category'] == row['Category'])]
        return filtered_df['Waitlist figure'].sum() / len(filtered_df)
    df_long['12 month rolling average'] = df_long.apply(average_last_12_months, axis=1)
    df_long['Difference - 12 month rolling average'] = df_long['Waitlist figure'] - df_long['12 month rolling average']
    df_long['Difference - 12 month rolling average (per cent)'] = df_long['Difference - 12 month rolling average'] / df_long['12 month rolling average'] * 100
    return df_long

def month_diff(df_long):
    df_long['Estimate flag - prior month'] = ''
    for Category in df_long['Category'].unique():
        df_long_Category = df_long[df_long['Category'] == Category].copy()
        df_long_Category['helper'] = df_long_Category['Date'] - pd.offsets.MonthEnd(1)
        df_long_Category['helper2'] = df_long_Category['helper'].apply(lambda x: df_long_Category.loc[df_long_Category['Date']==x, 'Waitlist figure'].values[0] if x in df_long_Category['Date'].values else float('nan'))
        df_long_Category['Difference - Prior month'] = df_long_Category['Waitlist figure'] - df_long_Category['helper2']
        df_long_Category['Difference - Prior month (per cent)'] = df_long_Category['Difference - Prior month'] / df_long_Category['helper2'] * 100
        df_long_Category['Estimate flag - prior month'] = df_long_Category['helper2'].apply(lambda x: '*' if pd.isnull(x) else '*')
        for i, row in df_long_Category.iterrows():
            if i == 0:
                continue
            if row['Estimate flag - prior month'] == '*':
                if i-1 in df_long_Category.index:
                    month_diff = row['Date'].month - df_long_Category.at[i-1, 'Date'].month
                    if month_diff != 0:
                        df_long_Category.loc[i, 'Difference - Prior month'] = (row['Waitlist figure'] - df_long_Category.at[i-1, 'Waitlist figure']) / month_diff
                        df_long_Category.loc[i, 'Difference - Prior month (per cent)'] = df_long_Category.loc[i, 'Difference - Prior month'] / df_long_Category.at[i-1, 'Waitlist figure'] * 100
        df_long_Category = df_long_Category.drop(['helper', 'helper2'], axis=1)
        df_long = df_long.drop(df_long[df_long['Category'] == Category].index)
        df_long = pd.concat([df_long, df_long_Category])
    return df_long

def year_diff(df_long):
    df_long['Estimate flag - prior year'] = ''
    for Category in df_long['Category'].unique():
        df_long_Category = df_long[df_long['Category'] == Category].copy()
        df_long_Category['helper'] = df_long_Category['Date'] - pd.offsets.MonthEnd(12)
        df_long_Category['helper2'] = df_long_Category['helper'].apply(lambda x: df_long_Category.loc[df_long_Category['Date']==x, 'Waitlist figure'].values[0] if x in df_long_Category['Date'].values else float('nan'))
        df_long_Category['Difference - 12 months prior'] = df_long_Category['Waitlist figure'] - df_long_Category['helper2']
        df_long_Category['Difference - 12 months prior (per cent)'] = df_long_Category['Difference - 12 months prior'] / df_long_Category['helper2'] * 100
        df_long_Category['Estimate flag - prior year'] = df_long_Category['helper2'].apply(lambda x: '#' if pd.isnull(x) else '')
        for i, row in df_long_Category.iterrows():
            if row['Date'] < df_long_Category['Date'].min() + pd.offsets.MonthEnd(12):
                continue
            if row['Estimate flag - prior year'] == '#':
                year_prior_date = row['Date'] - pd.offsets.MonthEnd(12)
                closest_date = min(df_long_Category['Date'], key=lambda x: abs(x - year_prior_date))
                df_long_Category.loc[i, 'Difference - 12 months prior'] = (row['Waitlist figure'] - df_long_Category.loc[df_long_Category['Date']==closest_date, 'Waitlist figure'].values[0]/(row['Date'].month-closest_date.month/12))
                df_long_Category.loc[i, 'Difference - 12 months prior (per cent)'] = df_long_Category.loc[i, 'Difference - 12 months prior'] / df_long_Category.loc[df_long_Category['Date']==closest_date, 'Waitlist figure'].values[0] * 100
        df_long_Category = df_long_Category.drop(['helper', 'helper2'], axis=1)
        df_long = df_long.drop(df_long[df_long['Category'] == Category].index)
        df_long = pd.concat([df_long, df_long_Category])
    return df_long

def calculate_cydiff(df_long):
    df_long['helper'] = df_long['Date'] - pd.offsets.YearEnd(1)
    df_long['helper2'] = df_long['helper'].apply(lambda x: df_long['Waitlist figure'][df_long['Date']==x].values[0] if x in df_long['Date'].values else float('nan'))
    df_long['Difference - calendar year to date'] = df_long['Waitlist figure'] - df_long['helper2']
    df_long['Difference - calendar year to date (per cent)'] = df_long['Difference - calendar year to date'] / df_long['helper2'] * 100
    df_long = df_long.drop(['helper', 'helper2'], axis=1)
    return df_long

def date_to_quarter_end(date):
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

def add_quarter(df_long):
    df_long['Quarter'] = df_long['Date'].apply(date_to_quarter_end)
    return df_long

def population_to_monthly(population_file_path, df_long):
    population = pd.read_csv(population_file_path)
    population['DATE'] = pd.to_datetime(population['DATE'])
    population.set_index('DATE', inplace=True)
    population = population.resample('M').mean()
    population = population.interpolate(method='linear')
    population = population.reset_index()
    date_list = df_long['Date'].unique()
    population_date_list = population['DATE'].unique()
    missing_dates = [date for date in date_list if date not in population_date_list]
    population = population.sort_values('DATE', ascending=True)
    for date in missing_dates:
        new_row = population.iloc[[-1]].copy()
        new_row['DATE'] = date
        population = pd.concat([population, new_row])
    return population

def add_population(df_long, population):
    population = population[['DATE', 'WA_POPULATION']]
    df_long = df_long.merge(population, how='left', left_on='Date', right_on='DATE')
    df_long['percent_of_population'] = df_long.apply(lambda row: row['Waitlist figure'] / row['WA_POPULATION'] * 100 if row['Category'] in ['total_individuals', 'priority_individuals'] else float('nan'), axis=1)
    df_long['Value_per10k'] = df_long.apply(lambda row: row['Waitlist figure'] / row['WA_POPULATION'] * 10000 if row['Category'] in ['total_individuals', 'priority_individuals'] else float('nan'), axis=1)
    df_long['12 month rolling average_per10k'] = df_long.apply(lambda row: row['12 month rolling average'] / row['WA_POPULATION'] * 10000 if row['Category'] in ['total_individuals', 'priority_individuals'] else float('nan'), axis=1)
    df_long = df_long.drop(['DATE'], axis=1)
    return df_long

def save_and_pass(df_long, save_to, save_latest_to):
    df_long['Category'] = df_long['Category'].str.replace('_', ' ')
    df_long['Category'] = df_long['Category'].str.title()
    df_long['Group'] = df_long['Category'].str.split(' ').str[0]
    df_long['Count'] = df_long['Category'].str.split(' ').str[1]

    df_long.to_csv(save_to, index=False)
    df_long_latest = df_long[df_long['Date'] == df_long['Date'].max()]
    df_long_latest.to_csv(save_latest_to, index=False)
    return df_long, df_long_latest

def final_long(plot_df, save_to):
    cols = plot_df.columns.tolist()
    ids =["Date", "Category", "Group", "Count", "Estimate flag - Waitlist figure", "Estimate flag - prior month", "Estimate flag - prior year"]
    values = [col for col in cols if col not in ids]
    plot_df = plot_df.melt(id_vars=ids, value_vars=values, var_name="Metric", value_name="Value")
    plot_df = plot_df[plot_df['Metric'] != 'WA_POPULATION']
    plot_df['Metric change - monthly'] = plot_df.groupby(['Category', 'Metric'])['Value'].diff()
    plot_df.loc[(plot_df['Metric'] == 'Difference - financial year to date') & (plot_df['Date'].dt.month == 7), 'Metric change - monthly'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - financial year to date (per cent)') & (plot_df['Date'].dt.month == 7), 'Metric change - monthly'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - calendar year to date') & (plot_df['Date'].dt.month == 1), 'Metric change - monthly'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - calendar year to date (per cent)') & (plot_df['Date'].dt.month == 1), 'Metric change - monthly'] = float('nan')
    plot_df.loc[plot_df['Metric'] == 'Waitlist figure', 'Metric change - monthly'] = float('nan')
    plot_df['Metric change - monthly (per cent)'] = plot_df['Metric change - monthly'] / plot_df['Value'].shift(1) * 100
    plot_df['Metric change - prior year'] = plot_df.groupby(['Category', 'Metric'])['Value'].diff(12)
    plot_df.loc[(plot_df['Metric'] == 'Difference - financial year to date') & (plot_df['Date'].dt.month == 7), 'Metric change - prior year'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - financial year to date (per cent)') & (plot_df['Date'].dt.month == 7), 'Metric change - prior year'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - calendar year to date') & (plot_df['Date'].dt.month == 1), 'Metric change - prior year'] = float('nan')
    plot_df.loc[(plot_df['Metric'] == 'Difference - calendar year to date (per cent)') & (plot_df['Date'].dt.month == 1), 'Metric change - prior year'] = float('nan')
    plot_df.loc[plot_df['Metric'] == 'Waitlist figure', 'Metric change - prior year'] = float('nan')
    plot_df['Metric change - prior year (per cent)'] = plot_df['Metric change - prior year'] / plot_df['Value'].shift(12) * 100
    cols = plot_df.columns.tolist()
    ids =["Date", "Category", "Group", "Count", "Estimate flag - Waitlist figure", "Estimate flag - prior month", "Estimate flag - prior year", "Metric"]
    values = [col for col in cols if col not in ids]
    plot_df = plot_df.melt(id_vars=ids, value_vars=values, var_name="Value type", value_name="#")
    plot_df = plot_df.dropna(subset=['#'])
    plot_df = plot_df.rename(columns={'#': 'Value'})
    plot_df.to_csv(save_to[:-4] + '__plotting.csv', index=False)
    return plot_df

# Main execution
file_path = '/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend.csv'
population_file_path = '/Users/yhanalucas/Desktop/Dash/Data/Population/Population_all_agesNoSex.csv'
save_to = '/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend_long.csv'
save_latest_to = '/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend_long_latest.csv'

if __name__ == "__main__":
    df = load_data(file_path)
    df_long = convert_to_long_form(df)
    df_long = gap_filler(df_long)
    df_long = calculate_12_month_average(df_long)
    population = population_to_monthly(population_file_path, df_long)
    df_long = add_population(df_long, population)
    df_long = month_diff(df_long)
    df_long = year_diff(df_long)
    df_long = calculate_cydiff(df_long)
    df_long = FYtdchange(df_long)
    df_long, df_long_latest = save_and_pass(df_long, save_to, save_latest_to)
    plot_df = final_long(df_long, save_to)
    print(df_long_latest)
    print(df_long)
    print(plot_df)







