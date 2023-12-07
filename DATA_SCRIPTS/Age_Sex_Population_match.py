import pandas as pd

#import Data/CSV/Population_State_Sex_Age.csv
Population_State_Sex_Age = pd.read_csv('DATA\Population\Population_State_Sex_Age.csv')
#date is dd-mm-yyyy
Population_State_Sex_Age['Date'] = pd.to_datetime(Population_State_Sex_Age['Date'], format='%d-%m-%Y')
# Set a multi-level index
Population_State_Sex_Age.set_index(['Date', 'Age group', 'Sex'], inplace=True)
# Pivot the DataFrame on 'Region'
Population_State_Sex_Age = Population_State_Sex_Age.pivot_table(index=["Date", "Sex", "Age group"], columns="Region", values="Population", aggfunc="sum")
# Reset the index to retain 'Age group', 'Sex', and 'Date' as columns
Population_State_Sex_Age.reset_index(inplace=True)
#sort by Date ascending
Population_State_Sex_Age = Population_State_Sex_Age.sort_values(by='Date', ascending=True)
#rename columns NSW to NSW_Population, Vic to Vic_Population, Qld to Qld_Population, WA to WA_Population, SA to SA_Population, Tas to Tas_Population, ACT to ACT_Population, NT to NT_Population, National to National_Population
Population_State_Sex_Age = Population_State_Sex_Age.rename(columns={'NSW': 'NSW_Population', 'Vic': 'Vic_Population', 'Qld': 'Qld_Population', 'WA': 'WA_Population', 'SA': 'SA_Population', 'Tas': 'Tas_Population', 'ACT': 'ACT_Population', 'NT': 'NT_Population', 'National': 'National_Population'})

def group_age(age_group):
    # Check if age_group ends with a '+'
    if age_group.endswith('+'):
        # Extract just the number part and convert to integer
        lower_age_limit = int(age_group[:-1])
    elif age_group == 'All ages':
        return age_group
    else:
        # Extract the lower age limit from the age group string
        lower_age_limit = int(age_group.split('-')[0])
    if lower_age_limit >= 65:
        return '65+'
    else:
        return age_group  # Keep other age groups unchanged

# Apply the grouping function to the 'Age group' column
Population_State_Sex_Age['Age group'] = Population_State_Sex_Age['Age group'].apply(group_age)

Population_State_Sex_Age = Population_State_Sex_Age.groupby(['Age group', 'Sex', 'Date']).agg({
    'NSW_Population': 'sum',
    'Vic_Population': 'sum',
    'Qld_Population': 'sum',
    'WA_Population': 'sum',
    'SA_Population': 'sum',
    'Tas_Population': 'sum',
    'ACT_Population': 'sum',
    'NT_Population': 'sum',
    'National_Population': 'sum'
}).reset_index()

#save to CSV Population_State_Sex_Age_to_65+.csv in Data/CSV folder
Population_State_Sex_Age.to_csv('DATA\Population\Population_State_Sex_Age_to_65+.csv', index=False)