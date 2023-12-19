import pandas as pd
import streamlit as st
import plotly.graph_objects as go

OWNdata = pd.read_csv('https://github.com/yazzledazzle/HousingWA/blob/b34d682e5176ff5299efddb46fc3545891c54707/Data/Public_housing/Stock.csv')
rogshousing = pd.read_csv("https://github.com/yazzledazzle/HousingWA/blob/b34d682e5176ff5299efddb46fc3545891c54707/Data/ROGS/rogs-202306-partg-section18-housing-dataset.csv", encoding='latin-1')

st.markdown('## NOTE: Some measures work, others still in progress')
col1, col2 = st.columns(2)
with col1: 
    measure = st.selectbox('Measure', rogshousing['Measure'].unique())
    filtered_data=rogshousing[rogshousing['Measure']==measure]
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

with col2:
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)
#plot x=Year, y=WA
regions = ['NSW', 'Vic', 'Qld', 'WA', 'SA','Tas', 'ACT', 'NT', 'Total', 'Aust']
fig=go.Figure()
for region in regions:
    fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data[region], mode='lines+markers', name=region))
fig.update_layout(title_text=f'{measure} - {desc1} {desc2}', yaxis=dict(title=filtered_data['Unit'].unique()[0]))
st.plotly_chart(fig, use_container_width=True)