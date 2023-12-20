
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Read the data
df = pd.read_csv('Data/SHS/Long_Form/SHS_Reasons_Long_Form.csv') 

# Data preprocessing
df['MEASURE'] = df['MEASURE'].fillna('Persons')  # Replace NaN in MEASURE with 'Persons'
df = df.rename(columns={'REASON FOR SEEKING ASSISTANCE': 'REASON'})  # Rename column for ease of use
df = df[df['GROUP'] != 'Total']  # Drop rows where Group is 'Total'
df = df.drop_duplicates()  # Drop duplicate rows

#value is float
df['VALUE'] = df['VALUE'].astype(float)
#if MEASURE is per 10k, .2f, else, ,.0f
df['VALUE'] = df.apply(lambda x: "{:.2f}".format(x['VALUE']) if x['MEASURE'] == 'Per 10,000 population' else "{:.0f}".format(x['VALUE']), axis=1)


#MAKE STATE COLUMN STRINGS ALL CAPS
df['STATE'] = df['STATE'].str.upper()

# Define regions
regions = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']

# Streamlit app layout
st.title("SHS Clients by Reason for Seeking Assistance")

# Widgets for user input
col1, col2 = st.columns(2)
with col1: 
    group_set = st.radio('Client Group Filter:', ['On', 'Off'], index=1, horizontal=True)

    if group_set == 'On':
        groups = st.multiselect("Select Group", options=df['GROUP'].unique().tolist(), default='Accommodation')
        df_filtered = df[df['GROUP'].isin(groups)]
        
    else:
        df_grouped = df.drop(columns=['GROUP', 'SEX'])  # Drop 'GROUP' and 'SEX' columns
        df_grouped = df_grouped.groupby(['STATE', 'DATE', 'MEASURE', 'REASON']).sum().reset_index()  # Group and sum
        df_filtered = df_grouped
        
    reasonfilter = st.radio('Reason Filtering:', ['Top 3', 'Selection'], index=0, horizontal=True)
    if reasonfilter == 'Top 3':
        df_latest_date = df_filtered[df_filtered['DATE'] == df_filtered['DATE'].max()]
        df_reason_check = df_latest_date.groupby('REASON').sum().reset_index().sort_values(by='VALUE', ascending=False)
        top_reasons = df_reason_check['REASON'].head(3).tolist()
        df_filtered = df_filtered[df_filtered['REASON'].isin(top_reasons)]
    else:
        selected_reasons = st.multiselect('Select Reasons', options=df['REASON'].unique().tolist(), default='Accommodation')
        df_filtered = df_filtered[df_filtered['REASON'].isin(selected_reasons)]

with col2:
    # Measures selection
    measures = df_filtered['MEASURE'].unique().tolist()
    measure = st.selectbox("Primary Axis", options=measures, index=0)
    second_measure = st.selectbox("Second Axis", options=[m for m in measures if m != measure], index=0)

    regions = st.multiselect("Select Regions", options=regions, default=regions)
chart = go.Figure()

for region in regions:
    df_region1 = df_filtered[df_filtered['STATE'] == region]
    df_measure1 = df_region1[df_region1['MEASURE'] == measure]
    #name1 = state + measure
    name1 = region + ' ' + measure
    #name2 = state + second_measure
    name2 = region + ' ' + second_measure
    #group by Date and sum Value
    #drop Measure, Region, Reason, Month, State
    df_measure1 = df_measure1.drop(columns=['MEASURE', 'STATE', 'REASON', 'MONTH', 'STATE'])
    if 'GROUP' in df_measure1.columns:
       df_measure1 = df_measure1.drop(columns=['GROUP'])
    df_measure1 = df_measure1.groupby(['DATE']).sum().reset_index()
        #DATE TO DATETIME
    df_measure1['DATE'] = pd.to_datetime(df_measure1['DATE'])
    chart.add_trace(go.Scatter(x=df_measure1['DATE'], y=df_measure1['VALUE'], name=name1))
    df_region2 = df_filtered[df_filtered['STATE'] == region]
    df_measure2 = df_region2[df_region2['MEASURE'] == second_measure]
    #drop Measure, Region, Reason, Month, State
    if 'GROUP' in df_measure2.columns:
       df_measure2 = df_measure2.drop(columns=['GROUP'])
    df_measure2 = df_measure2.drop(columns=['MEASURE', 'STATE', 'REASON', 'MONTH', 'STATE'])
    df_measure2 = df_measure2.groupby(['DATE']).sum().reset_index()
    #DATE TO DATETIME
    df_measure2['DATE'] = pd.to_datetime(df_measure2['DATE'])
    chart.add_trace(go.Scatter(x=df_measure2['DATE'], y=df_measure2['VALUE'], name=name2, yaxis='y2', line=dict(dash='dash')))
# Add title and axis labels
y1title = str(measure)
y2title = str(second_measure)
#if 'proportion' in y1title:
if y1title.startswith('proportion'):
    y1title = '%'
if y2title.startswith('proportion'):
    y2title = '%'
chart.update_layout(title_text='SHS Clients by State', xaxis_title='Date', yaxis_title=y1title, legend_title='State', yaxis2=dict(title=y2title, overlaying='y', side='right'))
#MOVE LEGEND FURTHER AWAY FROM CHART
chart.update_layout(legend=dict(
    yanchor="bottom",
    y=0.01,
    xanchor="left",
    x=1.2
))

st.plotly_chart(chart)
