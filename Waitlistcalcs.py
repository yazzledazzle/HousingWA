import pandas as pd
from pandas.tseries.offsets import DateOffset

def load_data(file_path):
    return pd.read_csv(file_path)

def convert_to_long_form(df):
    df_long = df.melt(id_vars=["Date"], 
                      var_name="Metric", 
                      value_name="Value")
    df_long['Date'] = pd.to_datetime(df_long['Date'])
    return df_long

def calculate_12_month_average(df_long):
    def average_last_12_months(row):
        start_date = row['Date'] - DateOffset(years=1) + DateOffset(days=1)
        end_date = row['Date']
        filtered_df = df_long[(df_long['Date'] >= start_date) & (df_long['Date'] <= end_date) & (df_long['Metric'] == row['Metric'])]
        return filtered_df['Value'].sum() / len(filtered_df)

    df_long['12_Month_Avg'] = df_long.apply(average_last_12_months, axis=1)
    return df_long

def calculate_month_change(df_long):
    df_long['Month_Change'] = df_long.groupby('Metric')['Value'].diff().shift(-1)
    return df_long

# Main execution
file_path = '/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend.csv'
df = load_data(file_path)
df_long = convert_to_long_form(df)
df_long = calculate_12_month_average(df_long)
df_long = calculate_month_change(df_long)

# Displaying the final DataFrame
print(df_long)
