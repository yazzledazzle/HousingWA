import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.markdown(f'Source: <a href="https://www.pc.gov.au/ongoing/report-on-government-services/2023/housing-and-homelessness/housing">Report on Government Services 2023, Part G, Section 18 - Housing</a>', unsafe_allow_html=True)


OWNdata = pd.read_csv('DATA/SOURCE DATA/Public housing/Stock.csv')
rogshousing = pd.read_csv("DATA/SOURCE DATA/ROGS and SHS/ROGS G18.csv", encoding='latin-1')

#remove Measure values Descriptive data, Survey response rates, Self-reported benefits of living in social housing - Public housing, Self-reported benefits of living in social housing - SOMIH, Self-reported benefits of living in social housing - Community housing
rogshousing = rogshousing[rogshousing['Measure'] != 'Descriptive data']
rogshousing = rogshousing[rogshousing['Measure'] != 'Survey response rates']
rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - Public housing']
rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - SOMIH']
rogshousing = rogshousing[rogshousing['Measure'] != 'Self-reported benefits of living in social housing - Community housing']



col1, col2 = st.columns(2)
with col1: 
    measure = st.selectbox('Measure', rogshousing['Measure'].unique())
    filtered_data=rogshousing[rogshousing['Measure']==measure]
    if measure == 'Recurrent expenditure':
        filtered_data = filtered_data[filtered_data['Housing_Type'] != 'Community housing']
        filtered_data = filtered_data[filtered_data['Housing_Type'].notna()]
        filtered_data = filtered_data[filtered_data['Housing_Type'] != 'Indigenous community housing']

with col1:
    housing_type = st.selectbox('Housing type', filtered_data['Housing_Type'].unique())
    filtered_data=filtered_data[filtered_data['Housing_Type']==housing_type]
with col2:
    desc1 = st.selectbox('Description1', filtered_data['Description1'].unique())
    filtered_data=filtered_data[filtered_data['Description1']==desc1]
    desc2 = st.selectbox('Description2', filtered_data['Description2'].unique())
    filtered_data=filtered_data[filtered_data['Description2']==desc2]
with col1:
    if len(filtered_data['Description3'].unique()) > 1:
        desc3 = st.selectbox('Description3', filtered_data['Description3'].unique())
        filtered_data=filtered_data[filtered_data['Description3']==desc3]
with col2:
    if len(filtered_data['Description4'].unique()) > 1:
        desc4 = st.selectbox('Description4', filtered_data['Description4'].unique())
        filtered_data=filtered_data[filtered_data['Description4']==desc4]
with col1:
    if len(filtered_data['Description5'].unique()) > 1:
        desc5 = st.selectbox('Description5', filtered_data['Description5'].unique())
        filtered_data=filtered_data[filtered_data['Description5']==desc5]
with col2:
    if len(filtered_data['Description6'].unique()) > 1:
        desc6 = st.selectbox('Description6', filtered_data['Description6'].unique())
        filtered_data=filtered_data[filtered_data['Description6']==desc6]
with col1:
    chart_type = st.radio('Chart type', ['Line chart', 'Bar chart'])
with col2:
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

if len(filtered_data['Total'].unique()) > 1:
    regions = ['Total', 'WA','NSW', 'Vic', 'Qld', 'WA', 'SA','Tas', 'ACT', 'NT']
else:
    regions = ['Aust', 'WA', 'NSW', 'Vic', 'Qld', 'SA','Tas', 'ACT', 'NT']



fig=go.Figure()

if chart_type == 'Line chart':
    for region in regions:
        fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data[region], name=region, mode='lines+markers'))
    fig.update_layout(title_text=f'{measure} - {desc1} {desc2}', yaxis=dict(title=filtered_data['Unit'].unique()[0]), xaxis=dict(title='Year'))

else:
    for region in regions:
        fig.add_trace(go.Bar(x=filtered_data['Year'], y=filtered_data[region], name=region))
    fig.update_layout(title_text=f'{measure} - {desc1} {desc2}', yaxis=dict(title=filtered_data['Unit'].unique()[0]), xaxis=dict(title='Year'), barmode='group')
st.plotly_chart(fig, use_container_width=True)