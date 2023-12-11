from Waitlistcalcs import *

# Main execution
file_path = 'DATA\Public_housing\Waitlist_trend.csv'
population_file_path = 'DATA\Population\Population_all_agesNoSex.csv'
save_to = 'DATA\Public_housing\Waitlist_trend_long.csv'
save_latest_to = 'DATA\Public_housing\Waitlist_trend_long_latest.csv'

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
