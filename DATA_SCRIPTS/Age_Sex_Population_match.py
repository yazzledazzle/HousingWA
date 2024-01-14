import pandas as pd

source_pop_file = 'DATA/SOURCE DATA/Population/Population_State_Sex_Age.csv'

def new_pop_file(file):
    Population_State_Sex_Age = pd.read_csv(file)
    #only keep columns 'SEX: Sex', 'AGE: Age', 'TIME PERIOD: Time Period', 'REGION: Region', 'OBS_VALUE'
    Population_State_Sex_Age = Population_State_Sex_Age()
    Population_State_Sex_Age['Date'] = pd.to_datetime(Population_State_Sex_Age['Date'], format='%d-%m-%Y')
    Population_State_Sex_Age.set_index(['Date', 'Age group', 'Sex'], inplace=True)
    Population_State_Sex_Age = Population_State_Sex_Age.pivot_table(index=["Date", "Sex", "Age group"], columns="Region", values="Population", aggfunc="sum")
    Population_State_Sex_Age.reset_index(inplace=True)
    Population_State_Sex_Age = Population_State_Sex_Age.sort_values(by='Date', ascending=True)
    Population_State_Sex_Age = Population_State_Sex_Age.rename(columns={'NSW': 'NSW_Population', 'Vic': 'Vic_Population', 'Qld': 'Qld_Population', 'WA': 'WA_Population', 'SA': 'SA_Population', 'Tas': 'Tas_Population', 'ACT': 'ACT_Population', 'NT': 'NT_Population', 'National': 'National_Population'})

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

    Population_State_Sex_Age.to_csv('DATA/PROCESSED DATA/Population/Population_State_Sex_Age_to_65+.csv', index=False)
    return

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

new_pop_file(source_pop_file)