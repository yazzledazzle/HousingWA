import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Waitlist_data import *

st.set_page_config(page_title='Movement charts', page_icon=':chart_with_upwards_trend:')


Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()
Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
datemax = Waitlist_trend['Date'].max()
lastyear = datemax - pd.DateOffset(years=1)
daterange = sorted(Waitlist_trend['Date'].unique())



Waitlist_trend["Total_Applications_Monthly_Change"] = Waitlist_trend["total_applications"] - Waitlist_trend["total_applications"].shift(1)
Waitlist_trend["Total_Individuals_Monthly_Change"] = Waitlist_trend["total_individuals"] - Waitlist_trend["total_individuals"].shift(1)

Waitlist_trend["Total_Applications_Percent_Change"] = (Waitlist_trend["Total_Applications_Monthly_Change"] / Waitlist_trend["total_applications"].shift(1)) * 100
Waitlist_trend["Total_Individuals_Percent_Change"] = (Waitlist_trend["Total_Individuals_Monthly_Change"] / Waitlist_trend["total_individuals"].shift(1)) * 100

Waitlist_trend["Priority_Applications_Monthly_Change"] = Waitlist_trend["priority_applications"] - Waitlist_trend["priority_applications"].shift(1)
Waitlist_trend["Priority_Individuals_Monthly_Change"] = Waitlist_trend["priority_individuals"] - Waitlist_trend["priority_individuals"].shift(1)

Waitlist_trend["Priority_Applications_Percent_Change"] = (Waitlist_trend["Priority_Applications_Monthly_Change"] / Waitlist_trend["priority_applications"].shift(1)) * 100
Waitlist_trend["Priority_Individuals_Percent_Change"] = (Waitlist_trend["Priority_Individuals_Monthly_Change"] / Waitlist_trend["priority_individuals"].shift(1)) * 100


# Date formatting and range slider
select_date_slider = st.select_slider('**Select date range:**', options=daterange, value=(lastyear, datemax),
                                        format_func=lambda x: pd.Timestamp(x).strftime('%b %y'))
startgraph, endgraph = list(select_date_slider)[0], list(select_date_slider)[1]


plot = st.button('Get graph')


if plot:
    Waitlist_trend = Waitlist_trend[(Waitlist_trend['Date'] >= startgraph) & (Waitlist_trend['Date'] <= endgraph)]

    #2 columns, 2 charts in each
    col1, col2 = st.columns(2)

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=Waitlist_trend['Date'], y=Waitlist_trend['Total_Applications_Monthly_Change'], name='Total applications monthly change'))
    fig1.update_layout(title='Total applications monthly change')
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=Waitlist_trend['Date'], y=Waitlist_trend['Total_Individuals_Monthly_Change'], name='Total individuals monthly change'))
    fig2.update_layout(title='Total individuals monthly change')
    col2.plotly_chart(fig2, use_container_width=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=Waitlist_trend['Date'], y=Waitlist_trend['Priority_Applications_Monthly_Change'], name='Priority applications monthly change'))
    fig3.update_layout(title='Priority applications monthly change')
    col1.plotly_chart(fig3, use_container_width=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=Waitlist_trend['Date'], y=Waitlist_trend['Priority_Individuals_Monthly_Change'], name='Priority individuals monthly change'))
    fig4.update_layout(title='Priority individuals monthly change')
    col2.plotly_chart(fig4, use_container_width=True)



