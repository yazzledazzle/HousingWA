import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

source = pd.read_csv('DATA/SOURCE DATA/Public housing/Waitlist_breakdowns.csv')
st.markdown(f'Source: <a href="https://www.parliament.wa.gov.au/Parliament/Pquest.nsf/(SearchResultsAllDesc)?SearchView&Query=(Housing%20waitlist)&Start=1&SearchOrder=4&SearchMax=1000">Parliamentary questions</a>', unsafe_allow_html=True)


data = source.copy()
#filter data for Item = Dwelling need | New tenancies by region
data = data[(data['Item'] == 'Dwelling need') | (data['Item'] == 'New tenancies by region') | (data['Item'] == 'Waiting time by region') | (data['Item'] == 'Waiting time by dwelling need')]

#for columns in DATA, if column name is 'Date', convert to datetime
if 'Date' in data.columns:
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

#create separate dataframe for each Category in column 'Category'

col1, col2 = st.columns(2)
with col1:
    view = st.selectbox('Dataset', data['Item'].unique())
with col2:
    filtered_data = data[data['Item'] == view]
    categories = filtered_data['Category'].unique()     
    categories = ['All'] + list(categories)
    category = st.selectbox('Category', categories)
with col1:
    if category != 'All':
        filtered_data = filtered_data[filtered_data['Category'] == category]
    subcategories = filtered_data['Subcategory'].unique()
    if len(filtered_data['Subcategory'].unique()) > 1:
        subcategory = st.selectbox('Subcategory', subcategories)
    else:
        subcategory = filtered_data['Subcategory'].unique()[0]
with col2:
    filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
    if len(filtered_data['Region'].unique()) > 1:
        region = st.selectbox('Region', ['All'] + list(filtered_data['Region'].unique()), index=0)  # Include 'All' option in region selectbox
        if region != 'All':    
            filtered_data = filtered_data[filtered_data['Region'] == region]

latest_date = filtered_data['Date'].max()
#convert to dd mmmm yy
latest_date = latest_date.strftime('%d %B %Y')
with col2:
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)


if view == 'Dwelling need':
    datalabels = st.radio('Data labels on bars', ['On', 'Off'], index=1, key='datalabels', horizontal=True)
    if category == 'All':
        dwellingdata = data[data['Item'] == 'Dwelling need']
        categories = dwellingdata['Category'].unique()
        for category in categories:
            st.markdown('**{view} for {category} {subcategory} at {latest_date}**'.format(view=view, category=category, subcategory=subcategory, latest_date=latest_date), unsafe_allow_html=True)
            #filter data to only include latest date
            pie1 = filtered_data[filtered_data['Date'] == latest_date]
            piecat = pie1[pie1['Category'] == category]
            #pie chart of Value by Detail
            fig = px.pie(piecat, values='Value', names='Detail')
            #label Value and %
            if datalabels == 'On':
                fig.update_traces(texttemplate='%{value:,.0f} (%{percent})', textposition='inside')
            st.plotly_chart(fig)
        for category in categories:
            st.markdown(f'**Dwelling demand by {category} over time**', unsafe_allow_html=True)
            fig2cat = filtered_data[filtered_data['Category'] == category]
            fig2 = go.Figure()
            for Detail in filtered_data['Detail'].unique():
                fig2filtered_data = fig2cat[fig2cat['Detail'] == Detail]
                fig2filtered_data['Date'] = fig2filtered_data['Date'].dt.strftime('%d %B %Y')
                fig2.add_trace(go.Bar(x=fig2filtered_data['Date'], y=fig2filtered_data['Value'], name=Detail))
            if datalabels == 'On':
                fig2.update_traces(texttemplate='%{y:.0f}', textposition='inside')
            #barmode stack
            fig2.update_layout(barmode='stack', yaxis=dict(title=f'{subcategory}'))
            st.plotly_chart(fig2, use_container_width=True)
        for category in categories:
            st.markdown(f'**Dwelling types needed by {category} - point in time comparison**', unsafe_allow_html=True)
            fig3 = go.Figure()
            cat = filtered_data[filtered_data['Category'] == category]
            dates = cat['Date'].unique()
            for date in dates:
                fig3filtered_data = cat[cat['Date'] == date]
                date = date.strftime('%d %B %Y')
                fig3.add_trace(go.Bar(x=fig3filtered_data['Detail'], y=fig3filtered_data['Value'], name=date))
            if datalabels == 'On':
                fig3.update_traces(texttemplate='%{y:.0f}', textposition='inside')
            fig3.update_layout(yaxis=dict(title=f'{subcategory}'))
            st.plotly_chart(fig3)
    else:
        st.markdown('**{view} for {category} {subcategory} at {latest_date}**'.format(view=view, category=category, subcategory=subcategory, latest_date=latest_date), unsafe_allow_html=True)
        #filter data to only include latest date
        filtered_filtered_data = filtered_data[filtered_data['Date'] == latest_date]
        #pie chart of Value by Detail
        fig = px.pie(filtered_data, values='Value', names='Detail')
        st.plotly_chart(fig)
        #bar chart of Value by Date, stack by Detail
        fig2 = go.Figure()
        for Detail in filtered_data['Detail'].unique():
            fig2filtered_data = filtered_data[filtered_data['Detail'] == Detail]
            fig2filtered_data['Date'] = fig2filtered_data['Date'].dt.strftime('%d %B %Y')
            fig2.add_trace(go.Bar(x=fig2filtered_data['Date'], y=fig2filtered_data['Value'], name=Detail))
            #label data inside top bar
        if datalabels == 'On':
            fig2.update_traces(texttemplate='%{y:.0f}', textposition='inside')
        #barmode stack
        fig2.update_layout(barmode='stack')

        st.plotly_chart(fig2, use_container_width=True)

        fig3 = go.Figure()
        dates = filtered_data['Date'].unique()
        for date in dates:
            fig3filtered_data = filtered_data[filtered_data['Date'] == date]
            #convert date to string
            date = date.strftime('%d %B %Y')
            fig3.add_trace(go.Bar(x=fig3filtered_data['Detail'], y=fig3filtered_data['Value'], name=date))
        if datalabels == 'On':
            fig3.update_traces(texttemplate='%{y:.0f}', textposition='inside')
        st.plotly_chart(fig3)
       

elif view == 'New tenancies by region':
    datalabels = st.radio('Data labels on bars', ['On', 'Off'], index=1, key='datalabels', horizontal=True)
    dates = filtered_data['Date'].unique()
    if len(dates) < 2:
        st.markdown('Single data point only')
        #clean = data but drop Subcategory, Detail, Item, Newtenanciestime
        date = filtered_data['Date'].unique()[0]
        clean =data[data['Item'] == view]
        clean = clean.drop(columns=['Subcategory', 'Detail', 'Item', 'Newtenanciestime', 'Date'], axis=1)
        #Date to string
        date = date.strftime('%d %B %Y')
        #if string in Category contains Priority, change to Priority, else Total
        clean['Category'] = clean['Category'].str.contains('Priority')
        clean['Category'] = clean['Category'].replace(True, 'Priority')
        clean['Category'] = clean['Category'].replace(False, 'Total')
        #print clean
        #create Priority and Total columns for each Region
        clean = clean.pivot_table(index='Region', columns='Category', values='Value', aggfunc='sum')
    
        #create WA total row
        clean.loc['WA total'] = clean.sum()    

        clean['Priority %'] = clean['Priority'] / clean['Total'] * 100
        #proportion priority to .1f
        clean['Priority %'] = clean['Priority %'].round(1)
        #get data for item = Region need
        region_need = source[source['Item'] == 'Region need']

        region_dates = region_need['Date'].unique()

        #pick latest date
        latest_date = region_dates.max()
        #filter data to only include latest date
        region_need = region_need[region_need['Date'] == latest_date]

        #if category string contains Priority, change to Priority, else Total
        region_need['Category'] = region_need['Category'].str.contains('Priority')
        region_need['Category'] = region_need['Category'].replace(True, 'Priority')
        region_need['Category'] = region_need['Category'].replace(False, 'Total')
        
        #filter for Subcategory = Applications
        region_need = region_need[region_need['Subcategory'] == 'Applications']
        #drop Subcategory, Detail, Item, Newtenanciestime, Date
        region_need = region_need.drop(columns=['Subcategory', 'Detail', 'Item', 'Newtenanciestime', 'Date'], axis=1)
        #pivot table
        region_need = region_need.pivot_table(index='Region', columns='Category', values='Value', aggfunc='sum')
        #create WA total row
        region_need.loc['WA total'] = region_need.sum()
        region_need['Priority %'] = region_need['Priority'] / region_need['Total'] * 100
        #proportion priority to .1f
        region_need['Priority %'] = region_need['Priority %'].round(1)
        #merge clean and region_need
        clean = pd.merge(clean, region_need, on='Region', suffixes=('', ' waitlist'))
        clean[f'% housed - Priority'] = clean['Priority'] / clean['Priority waitlist'] * 100
        clean[f'% housed - Priority'] = clean[f'% housed - Priority'].round(1)

        clean[f'% housed - Total'] = clean['Total'] / clean['Total waitlist'] * 100
        clean[f'% housed - Total'] = clean[f'% housed - Total'].round(1)
        # regionfigdata = clean but region as column not index
        regionfigdata = clean.reset_index()
        regionfig = go.Figure()
        regionfig.add_trace(go.Bar(x=regionfigdata['Region'], y=regionfigdata[f'% housed - Priority'], name=f'% housed - Priority'))
        regionfig.add_trace(go.Bar(x=regionfigdata['Region'], y=regionfigdata[f'% housed - Total'], name=f'% housed - Total'))
        regionfig.update_layout(barmode='group', yaxis=dict(title='%'), title_text = f'Percentage of waitlist at {latest_date} housed in 12months to to {date} - group by region')
        #data labels inside top bar
        if datalabels == 'On':
            regionfig.update_traces(texttemplate='%{y:.1f}', textposition='inside')
        st.plotly_chart(regionfig)
        regionlist = list(regionfigdata['Region'].unique())
        # plot a version with region as traces and % housed categories as y groups
        housed = regionfigdata[['Region', '% housed - Priority', '% housed - Total']]
        #transpose housed
        housed = housed.T
        #reset index
        housed = housed.reset_index()
        #row 0 as column names
        housed.columns = housed.iloc[0]
        #drop row 0
        housed = housed.drop(0)
        #rename Region to Category
        housed = housed.rename(columns={'Region': 'Category'})

        regionfig2 = go.Figure()
        for region in regionlist:
            regionfig2.add_trace(go.Bar(x=housed['Category'], y=housed[region], name=region))
        regionfig2.update_layout(barmode='group', yaxis=dict(title='%'), title_text = f'Percentage of waitlist at {latest_date} housed in 12 months to {date} - group by applicant type')
        if datalabels == 'On':
            regionfig2.update_traces(texttemplate='%{y:.1f}', textposition='inside')
        st.plotly_chart(regionfig2)



        st.write(housed)

        st.write(clean)
    else:
        for region in filtered_data['Region'].unique():
            st.markdown(f'**New tenancies in {region}**', unsafe_allow_html=True)
            regionchart = go.Figure()
            region_filtered_data = filtered_data[filtered_data['Region'] == region]
            region_filtered_data['Date'] = region_filtered_data['Date'].dt.strftime('%d %B %Y')
            regionchart.add_trace(go.Bar(x=region_filtered_data['Date'], y=region_filtered_data['Value'], name=region))
            regionchart.update_layout(yaxis=dict(title='New tenancies'))
            st.plotly_chart(regionchart, use_container_width=True)

elif view == 'Waiting time by dwelling need':
    #if Category contains Priority, change to Priority, else Total
    filtered_data['Category'] = filtered_data['Category'].str.contains('Priority')
    filtered_data['Category'] = filtered_data['Category'].replace(True, 'Priority Waitlist')
    filtered_data['Category'] = filtered_data['Category'].replace(False, 'Total Waitlist')
    #if len Subcategory >1 selectbox
    if len(filtered_data['Subcategory'].unique()) > 1:
        #selectbox Subcategory
        subcategory = st.selectbox('Metric', filtered_data['Subcategory'].unique())
        #filter data to only include selected Subcategory
        filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
        #drop Subcategory
        filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
    else:
        #drop Subcategory
        filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
    #drop Item, Newtenanciestime, Region
    filtered_data = filtered_data.drop(columns=['Item', 'Newtenanciestime', 'Region'], axis=1)
    #pivot table
    #round value to .0f
    filtered_data['Value'] = filtered_data['Value'].round(0)
    #date as string
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%d %B %Y')
    dwellingwait = go.Figure()
    if len(filtered_data['Date'].unique()) ==1:
        date = filtered_data['Date'].unique()[0]
        for category in filtered_data['Category'].unique():
            categorydata = filtered_data[filtered_data['Category'] == category]
            dwellingwait.add_trace(go.Bar(x=categorydata['Detail'], y=categorydata['Value'], name=category))
        dwellingwait.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {date}')
        st.plotly_chart(dwellingwait, use_container_width=True)
    else:
        if category != 'All':
            for date in filtered_data['Date'].unique():
                datefiltered_data = filtered_data[filtered_data['Date'] == date]
                dwellingwait.add_trace(go.Bar(x=datefiltered_data['Detail'], y=datefiltered_data['Value'], name=date))
            dwellingwait.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {category}', showlegend=True)
        else:
            for cat in filtered_data['Category'].unique():
                catwaitdwellfig = go.Figure()
                catfiltered_data = filtered_data[filtered_data['Category'] == cat]
                for date in catfiltered_data['Date'].unique():
                    datefiltered_data = catfiltered_data[catfiltered_data['Date'] == date]
                    catwaitdwellfig.add_trace(go.Bar(x=datefiltered_data['Detail'], y=datefiltered_data['Value'], name=date))
                catwaitdwellfig.update_layout(barmode='group', yaxis=dict(title='Waiting time (weeks)'), title_text = f'Waiting time by dwelling need - {subcategory} - {cat}', showlegend=True)
                st.plotly_chart(catwaitdwellfig, use_container_width=True)
    
    
    whenjoinorhouse = filtered_data.copy()
    #add column Forecast house date = today + weeks(Value)
    whenjoinorhouse['Forecast house date'] = pd.to_datetime(whenjoinorhouse['Date']) + pd.to_timedelta(whenjoinorhouse['Value'], unit='w')
    #add column Backcast apply date = today - weeks(Value)
    whenjoinorhouse['Backcast apply date'] = pd.to_datetime(whenjoinorhouse['Date']) - pd.to_timedelta(whenjoinorhouse['Value'], unit='w')
    #set columns to string 
    whenjoinorhouse['Forecast house date'] = whenjoinorhouse['Forecast house date'].dt.strftime('%d %B %Y')
    whenjoinorhouse['Backcast apply date'] = whenjoinorhouse['Backcast apply date'].dt.strftime('%d %B %Y')
    st.write(whenjoinorhouse)

elif view == 'Waiting time by region':
    #repeat similar to above
    #if Category contains Priority, change to Priority, else Total
    filtered_data['Category'] = filtered_data['Category'].str.contains('Priority')
    filtered_data['Category'] = filtered_data['Category'].replace(True, 'Priority Waitlist')
    filtered_data['Category'] = filtered_data['Category'].replace(False, 'Total Waitlist')
    #if len Subcategory >1 selectbox
    if len(filtered_data['Subcategory'].unique()) > 1:
        #selectbox Subcategory
        subcategory = st.selectbox('Metric', filtered_data['Subcategory'].unique())
        #filter data to only include selected Subcategory
        filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
        #drop Subcategory
        filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)
    else:
        #drop Subcategory
        filtered_data = filtered_data.drop(columns=['Subcategory'], axis=1)

    #drop Item, Newtenanciestime, Detail
    filtered_data = filtered_data.drop(columns=['Item', 'Newtenanciestime', 'Detail'], axis=1)
    #pivot table
    #round value to .0f
    filtered_data['Value'] = filtered_data['Value'].round(0)
    #forecast house date = today + weeks(Value)
    filtered_data['Forecast house date'] = pd.to_datetime(filtered_data['Date']) + pd.to_timedelta(filtered_data['Value'], unit='w')
    #backcast apply date = today - weeks(Value)
    filtered_data['Backcast apply date'] = pd.to_datetime(filtered_data['Date']) - pd.to_timedelta(filtered_data['Value'], unit='w')
    #set columns to string
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%d %B %Y')
    filtered_data['Forecast house date'] = filtered_data['Forecast house date'].dt.strftime('%d %B %Y')
    filtered_data['Backcast apply date'] = filtered_data['Backcast apply date'].dt.strftime('%d %B %Y')
    st.write(filtered_data)

