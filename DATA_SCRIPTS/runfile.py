from Waitlistcalcs import *

# Main execution
file_path = 'DATA\SOURCE DATA\Public housing\Waitlist_trend.csv'
population_file_path = 'DATA\PROCESSED DATA\Population\Population_all_agesNoSex.csv'
save = 'DATA\PROCESSED DATA\PUBLIC HOUSING\Waitlist_trend_long.csv'
save_latest = 'DATA\PROCESSED DATA\PUBLIC HOUSING\Waitlist_trend_latest.csv'


if __name__ == "__main__":
    df = load_data(file_path)
    df_long = convert_to_long_form(df)
    df_long = gap_filler(df_long)
    df_long = nonpriority(df_long)
    df_long = calculate_priority_proportion(df_long)
    population = population_to_monthly(population_file_path, df_long)
    df_long = add_population(df_long, population)
    df_long = month_diff(df_long)
    df_long = year_diff(df_long)
    df_long = calculate_cydiff(df_long)
    df_long = calculate_12_month_average(df_long)
    df_long = FYtdchange(df_long)
    final_long(df_long, save_latest, save)
