import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.markdown(f'Source: <a href="https://www.pc.gov.au/ongoing/report-on-government-services/2023/housing-and-homelessness/homelessness-services">Report on Government Services 2023, Part G, Section 19 - Homelessness Services</a>', unsafe_allow_html=True)


df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G19.csv', encoding='latin-1')
df['Year'] = df['Year'].astype(str)

df = df.rename(columns={'Aust': 'National'})
regions = ['National', 'WA', 'Vic', 'Qld', 'SA', 'NSW', 'Tas', 'NT', 'ACT']
#df long = melt on regions, value_name='Value', var_name='Region'
cols = df.columns.tolist()
#remove regions from cols
for region in regions:
    cols.remove(region)
dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')

#filter out measure = Rate of homeless people, Composition of support provided, Access of selected equity groups, Addressing client needs, Achievement of employment; education and/or training on exit, Achievement of income on exit,Clients at risk of homelessness who avoided homelessness,Support periods in which clients at risk of homelessness avoided homelessness,Achievement of independent housing on exit,Clients who return to homelessness after achieving housing, Clients who experience persistent homelessness
df = df[df['Measure'] != 'Rate of homeless people']
df = df[df['Measure'] != 'Composition of support provided']
df = df[df['Measure'] != 'Access of selected equity groups']
df = df[df['Measure'] != 'Addressing client needs']
df = df[df['Measure'] != 'Achievement of employment; education and/or training on exit']
df = df[df['Measure'] != 'Achievement of income on exit']
df = df[df['Measure'] != 'Clients at risk of homelessness who avoided homelessness']
df = df[df['Measure'] != 'Support periods in which clients at risk of homelessness avoided homelessness']
df = df[df['Measure'] != 'Achievement of independent housing on exit']
df = df[df['Measure'] != 'Clients who return to homelessness after achieving housing']
df = df[df['Measure'] != 'Clients who experience persistent homelessness']



select_measure = st.selectbox('Select measure', df['Measure'].unique())

df = df[df['Measure'] == select_measure]
df['Year'] = df['Year'].astype(str)

if select_measure == "Recurrent expenditure":
    
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Region series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)
    ytitle = df['Unit'].unique()[0] + ' (' + df['Year_Dollars'].unique()[0] + ')'
    showas = st.radio('Show as', ['Total', 'Per person in population'], index=0, horizontal=True)
    if showas == 'Total':
        dfRE = df[df['Description2'] == 'Total recurrent real expenditure']
        charttitle = 'Total recurrent real expenditure'
    if showas == 'Per person in population':
        dfRE = df[df['Description2'] == 'Real expenditure per person in the residential population']
        charttitle = 'Real expenditure per person in the residential population'
    fig = go.Figure()
    for region in regions:
        fig.add_trace(go.Bar(x=dfRE['Year'], y=dfRE[region], name=region))
    fig.update_layout(barmode='group', title='Recurrent expenditure - homelessness services', xaxis_title="Year", yaxis_title=ytitle)
    st.plotly_chart(fig)


if select_measure == "Unmet need":
    filter1 = st.selectbox('Select filter', ['Accommodation services', 'Services other than accommodation'], index=0, key='filter1')
    
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Region series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)
    if filter1 == 'Accommodation services':
        df_fig2 = df[df['Description1'] == 'Average daily unassisted requests']
        df_fig2 = df_fig2.sort_values(by=['Year'], ascending=True)
        df_fig2 = df_fig2[df_fig2['Description2'] == 'Accommodation services']
        fig2 = go.Figure()
        for region in regions:
            fig2.add_trace(go.Bar(x=df_fig2['Year'], y=df_fig2[region], name=region))
        fig2.update_layout(barmode='group', title='Average daily unassisted requests', xaxis_title="Year", yaxis_title='Number')
        st.plotly_chart(fig2)
        df_fig1 = df[df['Description1'] == 'Accommodation services']
        #sort Year ascending
        df_fig1 = df_fig1.sort_values(by=['Year'], ascending=True)
        for Desc2 in df_fig1['Description2'].unique().tolist():
            fig1 = go.Figure()
            df_fig1_fil = df_fig1[df_fig1['Description2'] == Desc2]
            for region in regions:
                fig1.add_trace(go.Bar(x=df_fig1_fil['Year'], y=df_fig1_fil[region], name=region))
            fig1.update_layout(barmode='group', title=Desc2, xaxis_title="Year", yaxis_title='Number')
            st.plotly_chart(fig1)
    if filter1 == 'Services other than accommodation':
        df_fig2 = df[df['Description1'] == 'Average daily unassisted requests']
        df_fig2 = df_fig2.sort_values(by=['Year'], ascending=True)
        df_fig2 = df_fig2[df_fig2['Description2'] == 'Services other than accommodation']
        fig2 = go.Figure()
        for region in regions:
            fig2.add_trace(go.Bar(x=df_fig2['Year'], y=df_fig2[region], name=region))
        fig2.update_layout(barmode='group', title='Average daily unassisted requests', xaxis_title="Year", yaxis_title='Number')
        st.plotly_chart(fig2)
        df_fig1 = df[df['Description1'] == 'Services other than accommodation']
        #sort Year ascending
        df_fig1 = df_fig1.sort_values(by=['Year'], ascending=True)
        for Desc2 in df_fig1['Description2'].unique().tolist():
            fig1 = go.Figure()
            df_fig1_fil = df_fig1[df_fig1['Description2'] == Desc2]
            for region in regions:
                fig1.add_trace(go.Bar(x=df_fig1_fil['Year'], y=df_fig1_fil[region], name=region))
            fig1.update_layout(barmode='group', title=Desc2, xaxis_title="Year", yaxis_title='Number')
            st.plotly_chart(fig1)


            