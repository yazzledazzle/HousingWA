import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G.csv', encoding='latin-1')
df['Year'] = df['Year'].astype(str)


Population = pd.read_csv('DATA\PROCESSED DATA\Population\Population_State_Sex_Age_to_65+.csv')
#Population filter for All ages, Total, mm=06
Population['Date'] = pd.to_datetime(Population['Date'], format='%d/%m/%y', dayfirst=True, errors='coerce')

df = df.rename(columns={'Aust': 'National'})
regions = ['National', 'WA', 'Vic', 'Qld', 'SA', 'NSW', 'Tas', 'NT', 'ACT']




st.title = "Sector overview - Report on Government Services"

select_measure = st.selectbox('Select measure', df['Measure'].unique())

df = df[df['Measure'] == select_measure]
regions = st.multiselect('Select regions', regions, default=regions)

if select_measure == "Recurrent expenditure":
    ytitle = df['Unit'].unique()[0] + ' (' + df['Year_Dollars'].unique()[0] + ')'
    df = df[df['Description3'] == 'Total']
    CRA = df[df['Description2'] == 'Commonwealth Rent Assistance (CRA)']
    NHHA = df[df['Description2'] == 'Total NHHA related expenditure']

    #category bar chart, x=year, y=df[region] for region in regions, color=Description1, group
    fig = go.Figure()
    for region in regions:
        fig.add_trace(go.Bar(x=NHHA['Year'], y=NHHA[region], name=region))
    fig.update_layout(barmode='group', title='NHHA funding', xaxis_title="Year", yaxis_title=ytitle)
    st.plotly_chart(fig)

    fig2 = go.Figure()
    for region in regions:
        fig2.add_trace(go.Bar(x=CRA['Year'], y=CRA[region], name=region))
    fig2.update_layout(barmode='group', title='CRA funding', xaxis_title="Year", yaxis_title=ytitle)
    st.plotly_chart(fig2)


