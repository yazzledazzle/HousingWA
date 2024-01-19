import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

data = pd.read_csv('DATA/PROCESSED DATA/PUBLIC HOUSING/Waitlist_trend_long.csv')
#make Date column datetime
data['Date'] = pd.to_datetime(data['Date'])
latest_date = data['Date'].max()
latest_date = pd.to_datetime(latest_date, format='%Y-%m-%d').strftime('%B %Y')
st.markdown(f'Source: <a href="https://www.parliament.wa.gov.au/Parliament/Pquest.nsf/(SearchResultsAllDesc)?SearchView&Query=(Housing%20waitlist)&Start=1&SearchOrder=4&SearchMax=1000">Parliamentary questions - last updated {latest_date} </a>', unsafe_allow_html=True)


class WaitlistTrend:
    def __init__(self, Date, Category, Subcategory, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value, FontColor):
        self.Date = Date
        self.Category = Category
        self.Subcategory = Subcategory
        self.Metric = Metric
        self.MetricDetail = MetricDetail
        self.MetricAs = MetricAs
        self.MetricCalc = MetricCalc
        self.MetricCalcAs = MetricCalcAs
        self.Estimate = Estimate
        self.Value = Value
        self.FontColor = FontColor

waitlist_trend = [] 
for index, row in data.iterrows():
    trend = WaitlistTrend(
        Date = row['Date'],
        Category = row['Description1'],
        Subcategory = row['Description2'],
        Metric = row['Description3'],
        MetricDetail = row['Description4'],
        MetricAs = row['Description5'],
        MetricCalc = row['Description6'],
        MetricCalcAs = row['Description7'],
        Estimate = row['Estimate'],
        Value = row['Value'],
        FontColor = "red" if row['Value'] > 0 else "green"

    )
    waitlist_trend.append(trend)   
col1, col2, col3 = st.columns(3)

with col1:
    select = st.selectbox('Category', ['Applications', 'Individuals'])

with col2:
    if select == 'Applications':
        axis2 = st.selectbox('Second axis', ['Proportion of Waitlist that is priority', 'Average Number Of Individuals Per Application', 'None'])
    else:
        axis2 = st.selectbox('Second axis', ['per 10 000', 'Percentage of population', 'None'])

with col3:
    st.markdown(f'</br>', unsafe_allow_html=True)
    Show_Rolling = col3.checkbox('Include 12 month rolling average line')
    graph_type = col3.radio('Display', ['Priority & total', 'Priority & non-priority'], horizontal=True)

dates = [x.Date for x in waitlist_trend]
dates = pd.DataFrame(columns=['Date'], data=dates)
#set to datetime
dates['Date'] = pd.to_datetime(dates['Date'])
max_date = dates['Date'].max()
if graph_type == 'Priority & non-priority':
    min_date = '2021-09-30'
    min_date = pd.to_datetime(min_date)
else:
    min_date = dates['Date'].min()
daterange = dates[(dates['Date'] >= min_date) & (dates['Date'] <= max_date)]
#sort and drop duplicates
daterange = daterange.sort_values(by=['Date'], ascending=True)
daterange = daterange.drop_duplicates(subset=['Date'], keep='first')

st.markdown("**Select date range:**")
select_date_slider= st.select_slider('', options=daterange, value=(min_date, max_date), format_func=lambda x: x.strftime('%b %y'))
startgraph, endgraph = list(select_date_slider)[0], list(select_date_slider)[1]
#filter data based on date range
waitlist_trend = [x for x in waitlist_trend if x.Date >= startgraph and x.Date <= endgraph]

waitlist_totalapp = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_totalapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_totalapp])
waitlist_priorityapp = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_priorityapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_priorityapp])
waitlist_nonpriorityapp = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_nonpriorityapp = pd.DataFrame.from_records([s.__dict__ for s in waitlist_nonpriorityapp])
waitlist_totalind = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_totalind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_totalind])
waitlist_priorityind = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_priorityind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_priorityind])
waitlist_nonpriorityind = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_nonpriorityind = pd.DataFrame.from_records([s.__dict__ for s in waitlist_nonpriorityind])
waitlist_proportionpriority = [x for x in waitlist_trend if x.Category == 'Proportion Priority' and x.Subcategory == 'Applications' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_proportionpriority = pd.DataFrame.from_records([s.__dict__ for s in waitlist_proportionpriority])
waitlist_averageperapptot = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Total' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_averageperapptot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperapptot])
waitlist_averageperapppri = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Priority' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_averageperapppri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperapppri])
waitlist_averageperappnon = [x for x in waitlist_trend if x.Category == 'Average Number Of Individuals Per Application' and x.Subcategory == 'Nonpriority' and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
waitlist_averageperappnon = pd.DataFrame.from_records([s.__dict__ for s in waitlist_averageperappnon])
waitlist_per10000tot = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
waitlist_per10000tot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000tot])
waitlist_per10000pri = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
waitlist_per10000pri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000pri])
waitlist_per10000non = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
waitlist_per10000non = pd.DataFrame.from_records([s.__dict__ for s in waitlist_per10000non])
waitlist_percentagetot = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
waitlist_percentagetot = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagetot])
waitlist_percentagepri = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
waitlist_percentagepri = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagepri])
waitlist_percentagenon = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
waitlist_percentagenon = pd.DataFrame.from_records([s.__dict__ for s in waitlist_percentagenon])
rolling_avgtotapp = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgtotapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgtotapp])
rolling_avgpriapp = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgpriapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgpriapp])
rolling_avgnonapp = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Applications' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgnonapp = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgnonapp])
rolling_avgtotind = [x for x in waitlist_trend if x.Category == 'Total' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgtotind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgtotind])
rolling_avgpriind = [x for x in waitlist_trend if x.Category == 'Priority' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgpriind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgpriind])
rolling_avgnonind = [x for x in waitlist_trend if x.Category == 'Nonpriority' and x.Subcategory == 'Individuals' and x.Metric == '12 month rolling average' and x.MetricDetail == '-'and x.MetricAs == 'Actual' and x.MetricCalc == '-']
rolling_avgnonind = pd.DataFrame.from_records([s.__dict__ for s in rolling_avgnonind])


fig = go.Figure()
if select == 'Applications':
    if graph_type == 'Priority & total':
        fig.add_trace(go.Scatter(x=waitlist_totalapp['Date'], y=waitlist_totalapp['Value'], mode='lines+markers', name='Total applications', fill='tonexty'))
        fig.add_trace(go.Scatter(x=waitlist_priorityapp['Date'], y=waitlist_priorityapp['Value'], mode='lines+markers', name='Priority applications', line=dict(color='red'), fill='tozeroy', fillcolor='palevioletred'))
        if axis2 == 'Average Number Of Individuals Per Application':
            fig.add_trace(go.Scatter(x=waitlist_averageperapptot['Date'], y=waitlist_averageperapptot['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='Avg persons -total', yaxis='y2'))
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgtotapp['Date'], y=rolling_avgtotapp['Value'], mode='lines', line=dict(color='blue', width=2, dash='dot'), name='12 month rolling average - total'))
    else:
        fig.add_trace(go.Bar(x=waitlist_priorityapp['Date'], y=waitlist_priorityapp['Value'], name='Priority applications', marker_color='red'))
        fig.add_trace(go.Bar(x=waitlist_nonpriorityapp['Date'], y=waitlist_nonpriorityapp['Value'], name='Non-priority applications'))
        fig.add_trace(go.Scatter(x=waitlist_totalapp['Date'], y=waitlist_totalapp['Value'], mode='lines+markers', line=dict(color='black'), name='Total applications'))
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgnonapp['Date'], y=rolling_avgnonapp['Value'], mode='lines', line=dict(color='blue', width=2, dash='dot'), name='12 month rolling average - total'))
        fig.update_layout(barmode='stack')
        if axis2 == 'Average Number Of Individuals Per Application':
            fig.add_trace(go.Scatter(x=waitlist_averageperapptot['Date'], y=waitlist_averageperappnon['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='Avg persons -total', yaxis='y2'))
    if Show_Rolling:
        fig.add_trace(go.Scatter(x=rolling_avgpriapp['Date'], y=rolling_avgpriapp['Value'], mode='lines', line=dict(color='maroon', width=2, dash='dot'), name='12 month rolling average - priority'))
    fig.update_layout(yaxis=dict(title='Applications'))
    if axis2 == 'Proportion of Waitlist that is priority':
        fig.add_trace(go.Scatter(x=waitlist_proportionpriority['Date'], y=waitlist_proportionpriority['Value'], mode='lines',  line=dict(color='maroon', dash='dash', width=2), name='Proportion priority',  yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Proportion priority (%)'), showlegend=True, title_text='Waitlist applications and priority percentage')
    elif axis2 == 'Average Number Of Individuals Per Application':
        fig.add_trace(go.Scatter(x=waitlist_averageperapppri['Date'], y=waitlist_averageperapppri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='Avg persons - priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Average persons'), showlegend=True, title_text='Waitlist applications and average persons per application')
    else:
        fig.update_layout(showlegend=True, title_text='Waitlist applications')
else:
    if graph_type == 'Priority & total':
        fig.add_trace(go.Scatter(x=waitlist_totalind['Date'], y=waitlist_totalind['Value'], mode='lines+markers', name='Total individuals', fill='tonexty'))
        fig.add_trace(go.Scatter(x=waitlist_priorityind['Date'], y=waitlist_priorityind['Value'], mode='lines+markers', line=dict(color='red'), name='Priority individuals', fill='tozeroy', fillcolor='palevioletred'))
        fig.update_layout(yaxis=dict(title='Individuals'))
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgtotind['Date'], y=rolling_avgtotind['Value'], mode='lines', line=dict(color='royalblue', width=2, dash='dot'), name='12 month rolling average - total'))
        if axis2 == 'per 10 000':
            fig.add_trace(go.Scatter(x=waitlist_per10000tot['Date'], y=waitlist_per10000tot['Value'], mode='lines', line=dict(color='navy', width=2), name='per 10 000 - total', yaxis='y2'))
        elif axis2 == 'Percentage of population':
            fig.add_trace(go.Scatter(x=waitlist_percentagetot['Date'], y=waitlist_percentagetot['Value'], line=dict(color='navy', width=2), mode='lines+markers', name='% population - total', yaxis='y2'))
    else:
        fig.add_trace(go.Bar(x=waitlist_priorityind['Date'], y=waitlist_priorityind['Value'], name='Priority individuals', marker_color='red'))
        fig.add_trace(go.Bar(x=waitlist_nonpriorityind['Date'], y=waitlist_nonpriorityind['Value'], name='Non-priority individuals'))
        fig.add_trace(go.Scatter(x=waitlist_totalind['Date'], y=waitlist_totalind['Value'], mode='lines+markers', line=dict(color='black'), name='Total individuals'))
        fig.update_layout(barmode='stack')
        if Show_Rolling:
            fig.add_trace(go.Scatter(x=rolling_avgnonind['Date'], y=rolling_avgnonind['Value'], mode='lines', line=dict(color='royalblue', width=2, dash='dot'), name='12 month rolling average - total'))
        if axis2 == 'per 10 000':
            fig.add_trace(go.Scatter(x=waitlist_per10000non['Date'], y=waitlist_per10000non['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='per 10 000 - total', yaxis='y2'))
        elif axis2 == 'Percentage of population':
            fig.add_trace(go.Scatter(x=waitlist_percentagenon['Date'], y=waitlist_percentagenon['Value'], mode='lines', line=dict(color='navy', dash='dash', width=2), name='% population - total', yaxis='y2'))
    fig.update_layout(yaxis=dict(title='Individuals'))
    if Show_Rolling:
        fig.add_trace(go.Scatter(x=rolling_avgpriind['Date'], y=rolling_avgpriind['Value'], mode='lines', line=dict(color='maroon', width=2, dash='dot'), name='12 month rolling average - priority'))
    if axis2 == 'per 10 000':
        fig.add_trace(go.Scatter(x=waitlist_per10000pri['Date'], y=waitlist_per10000pri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='per 10 000 - priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='per 10 000 residents'), showlegend=True, title_text='Waitlist individuals and rate per 10 000 residents')
    elif axis2 == 'Percentage of population':
        fig.add_trace(go.Scatter(x=waitlist_percentagepri['Date'], y=waitlist_percentagepri['Value'], mode='lines', line=dict(color='maroon', dash='dash', width=2), name='% population - priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='% population'), showlegend=True, title_text='Waitlist individuals and percentage of population')
    else:
        fig.update_layout(showlegend=True, title_text='Waitlist individuals')

fig.update_layout(
    xaxis=dict(
        tickformat="%b %y",  # Format for mmm yy
        tick0=waitlist_totalapp['Date'].min(),  # Starting point
        dtick="M3"  # Interval of 3 months
    ),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.1  # Adjust these values to move the legend further away
    ),
)

#4 columns
col1, col2, col3 = st.columns(3)
with col3:
    st.markdown('<table style="background-color: yellow; font-weight: bold; font-style: italic"><tr><td>Series can be toggled on/off by clicking on the legend</td></tr></table>', unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)
