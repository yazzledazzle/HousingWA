import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G.csv', encoding='latin-1')
df['Year'] = df['Year'].astype(str)

st.markdown(f'Source: <a href="https://www.pc.gov.au/research/ongoing/report-on-government-services/2022/housing-and-homelessness">Report on Government Services 2023, Part G, Sector Overview</a>', unsafe_allow_html=True)

Population = pd.read_csv('DATA/PROCESSED DATA/Population/Population_State_Sex_Age_to_65+.csv')
#Population filter for All ages, Total, mm=06
Population['Date'] = pd.to_datetime(Population['Date'], format='%d/%m/%y', dayfirst=True, errors='coerce')

df = df.rename(columns={'Aust': 'National'})
regions = ['National', 'WA', 'Vic', 'Qld', 'SA', 'NSW', 'Tas', 'NT', 'ACT']
#df long = melt on regions, value_name='Value', var_name='Region'
cols = df.columns.tolist()
#remove regions from cols
for region in regions:
    cols.remove(region)
dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')

st.title = "Sector overview - Report on Government Services"

#filter out measure = Households residing in community housing
df = df[df['Measure'] != 'Households residing in community housing']

select_measure = st.selectbox('Select measure', df['Measure'].unique())

df = df[df['Measure'] == select_measure]
df['Year'] = df['Year'].astype(str)

if select_measure == "Recurrent expenditure":
    regions = st.multiselect('Select regions', regions, default=regions)
    ytitle = df['Unit'].unique()[0] + ' (' + df['Year_Dollars'].unique()[0] + ')'
    dfRE = df[df['Description3'] == 'Total']
    CRA = dfRE[dfRE['Description2'] == 'Commonwealth Rent Assistance (CRA)']
    NHHA = dfRE[dfRE['Description2'] == 'Total NHHA related expenditure']

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

if select_measure == "Low income rental households":
    regions = st.multiselect('Select regions', regions, default=regions)
    dfLIH = df[df['Uncertainty'].isna()]
    select_year = st.selectbox('Select year', dfLIH['Year'].unique())
    dfLIH = dfLIH[dfLIH['Year'] == select_year]
    ytitle1 = "Proportion"
    ytitle2 = "Number"
    dfLIH = dfLIH[dfLIH['Description3'] == 'Paying more than 30% of income on housing costs']
    dfProp = dfLIH[dfLIH['Description4'] == 'Proportion']
    dfNum = dfLIH[dfLIH['Description4'] == 'Number']
    fig = go.Figure()
    fig2 = go.Figure()
    for region in regions:
        fig.add_trace(go.Bar(x=dfProp['Description2'], y=dfProp[region], name=region))
        fig2.add_trace(go.Bar(x=dfNum['Description2'], y=dfNum[region], name=region))
    fig.update_layout(barmode='group', title='Proportion of low income rental households paying more than 30% of income on housing costs', xaxis_title="Remoteness", yaxis_title=ytitle1)
    fig2.update_layout(barmode='group', title='Number of low income rental households paying more than 30% of income on housing costs', xaxis_title="Remoteness", yaxis_title=ytitle2)
    st.plotly_chart(fig)
    st.plotly_chart(fig2)

if select_measure == "Housing affordability":
    ytitle = df['Description2'].unique()[0]
    charttitle = df['Description1'].unique()[0]
    compare = st.radio('Compare', ['States', 'Years', 'States & years'], horizontal=True)
    if compare == 'States':
        regions = st.multiselect('Select regions', regions, default=regions)
        select_year = st.selectbox('Select year', df['Year'].unique())
        dfHA = df[df['Year'] == select_year]
        fig = go.Figure()
        for region in regions:
            fig.add_trace(go.Bar(x=dfHA['Year'], y=dfHA[region], name=region))
        fig.update_layout(barmode='group', title=charttitle, xaxis_title="Year", yaxis_title=ytitle)
        st.plotly_chart(fig)
    if compare == 'Years':
        regions = st.selectbox('Select region', regions)
        years = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
        fig = go.Figure()
        for year in years:
            dfHA = df[df['Year'] == year]
            fig.add_trace(go.Bar(x=dfHA['Year'], y=dfHA[regions], name=year))
        fig.update_layout(barmode='group', title=charttitle, xaxis_title="Year", yaxis_title=ytitle)
        st.plotly_chart(fig)
    if compare == 'States & years':
        regions = st.multiselect('Select regions', regions, default=regions)
        years = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
        dfHA = df[df['Year'].isin(years)]
        dflong = pd.melt(dfHA, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')
        dflong = dflong[dflong['Region'].isin(regions)]
        #sort dflong by Year ascending
        dflong = dflong.sort_values(by=['Year'], ascending=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=[dflong['Region'],dflong['Year']], y=dflong['Value']))
        #add figure inside bar
        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
        fig.update_layout(barmode='group', title=charttitle, yaxis_title=ytitle)
        st.plotly_chart(fig)
if select_measure == "Housing composition by tenure type":
    df['Description4'] = df['Description4'].fillna(df['Description3'])
    compare = st.radio('Compare', ['States', 'Years', 'States & years'], horizontal=True)
    df = df[df['Description4'] != 'Total renters']
    df = df[df['Uncertainty'].isna()]
    #sort year ascending
    df = df.sort_values(by=['Year'], ascending=True)
    if compare == 'States':
        regions = st.multiselect('Select regions', regions, default=regions)
        select_year = st.selectbox('Select year', df['Year'].unique())
        df = df[df['Year'] == select_year]   
        fig = go.Figure()
        for region in regions:
            fig.add_trace(go.Bar(x=df['Description4'], y=df[region], name=region))
        fig.update_layout(barmode='group', title='Proportion of renters by tenure type', xaxis_title="Tenure type", yaxis_title="Proportion")
        st.plotly_chart(fig)
    if compare == 'Years':
        regions = st.selectbox('Select region', regions)
        years = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
        df = df[df['Year'].isin(years)]
        #Bar of Year as string category on x, y=df[region] for region, use px
        fig = px.bar(df, x='Year', y=regions, color='Description4', title='Proportion of renters by tenure type', barmode='group', labels={'Year': 'Year', regions: 'Proportion', 'Description4': 'Tenure type'})
        st.plotly_chart(fig)
    if compare == 'States & years':
        regions = st.multiselect('Select regions', regions, default=regions)
        years = st.multiselect('Select years', df['Year'].unique(), default=df['Year'].unique())
        df = df[df['Year'].isin(years)]
        dflong = pd.melt(df, id_vars=cols, value_vars=regions, var_name='Region', value_name='Value')
        #for year in years, filter dflong for year, plotly express bar, x=Region, y=Value, color=Region, facet_col=Year
        dflong['Year'] = dflong['Year'].astype(str)
        #dflong Region in regions
        dflong = dflong[dflong['Region'].isin(regions)]
        fig = px.bar(dflong, x='Year', y='Value', color='Description4', facet_col='Region', facet_col_wrap=1, title='Proportion of renters by tenure type', barmode='group', labels={'Region': 'Region', 'Value': '%'})
        #label y value inside bars
        fig.update_traces(texttemplate='%{y:.2s}', textposition='inside')
        #legend title Tenure type
        fig.update_layout(legend_title_text='Tenure type')
        #don't show fac
        st.plotly_chart(fig)

if select_measure == 'Income units receiving CRA':
    #fill blank Special_Need with 'No special need'
    df['Special_Need'] = df['Special_Need'].fillna('No special need')
    filter_for = st.selectbox('Filter for', df['Special_Need'].unique())
    df = df[df['Special_Need'] == filter_for]
    select = st.selectbox('Select', df['Description2'].unique())
    df = df[df['Description2'] == select]
    select_year = st.selectbox('Select year', df['Year'].unique())
    df = df[df['Year'] == select_year]
    regions = st.multiselect('Select regions', regions, default=regions)
    if len(df['Description4'].unique()) > 1:
        filter = st.selectbox('Filter', df['Description3'].unique())
        df = df[df['Description3'] == filter]
    df['Description4'] = df['Description4'].fillna(df['Description3'])
    dfProp = df[df['Unit'] == '%']
    dfNum = df[df['Unit'] == 'no.']
    fig = go.Figure()
    fig2 = go.Figure()
    for region in regions:
        fig.add_trace(go.Bar(x=dfProp['Description4'], y=dfProp[region], name=region))
        fig2.add_trace(go.Bar(x=dfNum['Description4'], y=dfNum[region], name=region))
    st.write(f'Proportion of income units receiving CRA - {filter_for}, {select}, {filter}')
    fig.update_layout(barmode='group',xaxis_title="Category", yaxis_title="Proportion")
    fig2.update_layout(barmode='group', xaxis_title="Category", yaxis_title="Number")
    st.plotly_chart(fig)
    st.write(f'Number of income units receiving CRA - {filter_for}, {select}, {filter}')
    st.plotly_chart(fig2)
    

               