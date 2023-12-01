import streamlit as st
import pandas as pd
from Waitlist_data import *
import plotly.graph_objects as go

Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()

def change_color(val):
    """Returns color string for positive or negative values."""
    if val > 0:
        return "red"
    else:
        return "green"

def calc_and_write_waitlist(Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago):
    latest_total_applications = Waitlist_latest['total_applications'].iloc[0]
    latest_total_individuals = Waitlist_latest['total_individuals'].iloc[0]
    latest_priority_applications = Waitlist_latest['priority_applications'].iloc[0]
    latest_priority_individuals = Waitlist_latest['priority_individuals'].iloc[0]

    col1, col2 = st.columns(2)

    latest_date = Waitlist_latest['Date'].iloc[0]
        #markdown header 2 - As at {latest_date} format dd mmm yyyy
    col1.markdown(f'### As at {latest_date.strftime("%d %b %Y")}:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    if not pd.isnull(Waitlist_latest['total_applications'].iloc[0]):   
        #markdown header 3 - Total applications: {latest_total_applications}
        col1.markdown(f'**Total applications:** {int(latest_total_applications):,}')
        month_change_total_applications = latest_total_applications - Waitlist_1m_ago['total_applications'].iloc[0]
        month_change_total_applications_pc = round((month_change_total_applications / Waitlist_1m_ago['total_applications'].iloc[0]) * 100, 1)
        #annual change in total applications
        year_change_total_applications = latest_total_applications - Waitlist_12m_ago['total_applications'].iloc[0]
        year_change_total_applications_pc = round((year_change_total_applications / Waitlist_12m_ago['total_applications'].iloc[0]) * 100, 1)

    if not pd.isnull(Waitlist_latest['total_individuals'].iloc[0]):
    #markdown header 3 - Total individuals: {latest_total_individuals}
        col2.markdown(f'**Total individuals:** {int(latest_total_individuals):,}')
        month_change_total_individuals = latest_total_individuals - Waitlist_1m_ago['total_individuals'].iloc[0]
        month_change_total_individuals_pc = round((month_change_total_individuals / Waitlist_1m_ago['total_individuals'].iloc[0]) * 100, 1)
        #annual change in total individuals
        year_change_total_individuals = latest_total_individuals - Waitlist_12m_ago['total_individuals'].iloc[0]
        year_change_total_individuals_pc = round((year_change_total_individuals / Waitlist_12m_ago['total_individuals'].iloc[0]) * 100, 1)

    if not pd.isnull(Waitlist_latest['priority_applications'].iloc[0]):   
        #markdown header 3 - Priority applications: {latest_priority_applications}
        col1.markdown(f'**Priority applications:** {int(latest_priority_applications):,}')
        month_change_priority_applications = latest_priority_applications - Waitlist_1m_ago['priority_applications'].iloc[0]
        month_change_priority_applications_pc = round((month_change_priority_applications / Waitlist_1m_ago['priority_applications'].iloc[0]) * 100, 1)
        #annual change in priority applications
        year_change_priority_applications = latest_priority_applications - Waitlist_12m_ago['priority_applications'].iloc[0]
        year_change_priority_applications_pc = round((year_change_priority_applications / Waitlist_12m_ago['priority_applications'].iloc[0]) * 100, 1)
        #markdown header 3 - Priority individuals: {latest_priority_individuals}
    if not pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
        col2.markdown(f'**Priority individuals:** {int(latest_priority_individuals):,}')
        month_change_priority_individuals = latest_priority_individuals - Waitlist_1m_ago['priority_individuals'].iloc[0]
        month_change_priority_individuals_pc = round((month_change_priority_individuals / Waitlist_1m_ago['priority_individuals'].iloc[0]) * 100, 1)
        #annual change in priority individuals
        year_change_priority_individuals = latest_priority_individuals - Waitlist_12m_ago['priority_individuals'].iloc[0]
        year_change_priority_individuals_pc = round((year_change_priority_individuals / Waitlist_12m_ago['priority_individuals'].iloc[0]) * 100, 1)

    #if any are null
    if pd.isnull(Waitlist_latest['total_applications'].iloc[0]) or pd.isnull(Waitlist_latest['total_individuals'].iloc[0]) or pd.isnull(Waitlist_latest['priority_applications'].iloc[0]) or pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
    #markdown header 2 - Latest data at other dates
        col1.markdown('### Latest data where at other dates:')
        col2.markdown(f'### </br>', unsafe_allow_html=True)

        if pd.isnull(Waitlist_latest['total_applications'].iloc[0]):
            #filter for non null values for total applications 
            Waitlist_trend = Waitlist_trend[Waitlist_trend['total_applications'].notnull()]
            #find latest non null value for total applications and corresponding date
            latest_total_applications = Waitlist_trend.tail(1)['total_applications'].iloc[0]
            latest_total_applications_date = Waitlist_trend.tail(1)['Date'].iloc[0]
            #find previous month
            latest_total_applications_1m_ago = Waitlist_trend.tail(2).head(1)['total_applications'].iloc[0]
            #find 12 months ago
            latest_total_applications_12m_ago = Waitlist_trend[Waitlist_trend['Date'] == latest_total_applications_date - pd.DateOffset(months=12)]['total_applications'].iloc[0]
            month_change_total_applications = latest_total_applications - latest_total_applications_1m_ago
            month_change_total_applications_pc = round((month_change_total_applications / latest_total_applications_1m_ago) * 100, 1)
            #annual change in total applications
            year_change_total_applications = latest_total_applications - latest_total_applications_12m_ago
            year_change_total_applications_pc = round((year_change_total_applications / latest_total_applications_12m_ago) * 100, 1)
            #markdown header 3 - Total applications: {latest_total_applications} as at {latest_total_applications_date}
            col1.markdown(f'**Total applications:** {int(latest_total_applications):,} as at {latest_total_applications_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['total_individuals'].iloc[0]):
            #find latest non null value for total individuals and corresponding date
            latest_total_individuals = Waitlist_trend[Waitlist_trend['total_individuals'].notnull()].tail(1)['total_individuals'].iloc[0]
            latest_total_individuals_date = Waitlist_trend[Waitlist_trend['total_individuals'].notnull()].tail(1)['Date'].iloc[0]
            latest_total_individuals_1m_ago = Waitlist_trend[Waitlist_trend['total_individuals'].notnull()].tail(2).head(1)['total_individuals'].iloc[0]
            latest_total_individuals_12m_ago = Waitlist_trend[Waitlist_trend['total_individuals'].notnull()][Waitlist_trend['Date'] == latest_total_individuals_date - pd.DateOffset(months=12)]['total_individuals'].iloc[0]
            month_change_total_individuals = latest_total_individuals - latest_total_individuals_1m_ago
            month_change_total_individuals_pc = round((month_change_total_individuals / latest_total_individuals_1m_ago) * 100, 1)
            #annual change in total individuals
            year_change_total_individuals = latest_total_individuals - latest_total_individuals_12m_ago
            year_change_total_individuals_pc = round((year_change_total_individuals / latest_total_individuals_12m_ago) * 100, 1)
            #markdown header 3 - Total individuals: {latest_total_individuals} as at {latest_total_individuals_date}
            col2.markdown(f'**Total individuals:** {int(latest_total_individuals):,} as at {latest_total_individuals_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['priority_applications'].iloc[0]):
            #find latest non null value for priority applications and corresponding date
            latest_priority_applications = Waitlist_trend[Waitlist_trend['priority_applications'].notnull()].tail(1)['priority_applications'].iloc[0]
            latest_priority_applications_date = Waitlist_trend[Waitlist_trend['priority_applications'].notnull()].tail(1)['Date'].iloc[0]
            latest_total_individuals_1m_ago = Waitlist_trend[Waitlist_trend['priority_applications'].notnull()].tail(2).head(1)['priority_applications'].iloc[0]
            latest_total_individuals_12m_ago = Waitlist_trend[Waitlist_trend['priority_applications'].notnull()][Waitlist_trend['Date'] == latest_priority_applications_date - pd.DateOffset(months=12)]['priority_applications'].iloc[0]
            month_change_priority_applications = latest_priority_applications - latest_total_individuals_1m_ago
            month_change_priority_applications_pc = round((month_change_priority_applications / latest_total_individuals_1m_ago) * 100, 1)
            #annual change in priority applications
            year_change_priority_applications = latest_priority_applications - latest_total_individuals_12m_ago
            year_change_priority_applications_pc = round((year_change_priority_applications / latest_total_individuals_12m_ago) * 100, 1)
            #markdown header 3 - Priority applications: {latest_priority_applications} as at {latest_priority_applications_date}
            col1.markdown(f'**Priority applications:** {int(latest_priority_applications):,} as at {latest_priority_applications_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
            #find latest non null value for priority individuals and corresponding date
            latest_priority_individuals = Waitlist_trend[Waitlist_trend['priority_individuals'].notnull()].tail(1)['priority_individuals'].iloc[0]
            latest_priority_individuals_date = Waitlist_trend[Waitlist_trend['priority_individuals'].notnull()].tail(1)['Date'].iloc[0]
            latest_priority_individuals_1m_ago = Waitlist_trend[Waitlist_trend['priority_individuals'].notnull()].tail(2).head(1)['priority_individuals'].iloc[0]
            latest_priority_individuals_12m_ago = Waitlist_trend[Waitlist_trend['priority_individuals'].notnull()][Waitlist_trend['Date'] == latest_priority_individuals_date - pd.DateOffset(months=12)]['priority_individuals'].iloc[0]
            month_change_priority_individuals = latest_priority_individuals - latest_priority_individuals_1m_ago
            month_change_priority_individuals_pc = round((month_change_priority_individuals / latest_priority_individuals_1m_ago) * 100, 1)
            #annual change in priority individuals
            year_change_priority_individuals = latest_priority_individuals - latest_priority_individuals_12m_ago
            year_change_priority_individuals_pc = round((year_change_priority_individuals / latest_priority_individuals_12m_ago) * 100, 1)
            #markdown header 3 - Priority individuals: {latest_priority_individuals} as at {latest_priority_individuals_date}
            col2.markdown(f'**Priority individuals:** {int(latest_priority_individuals):,} as at {latest_priority_individuals_date.strftime("%d %b %Y")}')



    # Updating display for monthly changes
    col1.markdown('### Monthly changes:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    col1.markdown(f'**Total applications:** <font color="{change_color(month_change_total_applications)}">{int(month_change_total_applications):,} ({month_change_total_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Total individuals:** <font color="{change_color(month_change_total_individuals)}">{int(month_change_total_individuals):,} ({month_change_total_individuals_pc}%)</font>', unsafe_allow_html=True)
    col1.markdown(f'**Priority applications:** <font color="{change_color(month_change_priority_applications)}">{int(month_change_priority_applications):,} ({month_change_priority_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Priority individuals:** <font color="{change_color(month_change_priority_individuals)}">{int(month_change_priority_individuals):,} ({month_change_priority_individuals_pc}%)</font>', unsafe_allow_html=True)

    # Updating display for annual changes
    col1.markdown('### Annual changes:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    col1.markdown(f'**Total applications:** <font color="{change_color(year_change_total_applications)}">{int(year_change_total_applications):,} ({year_change_total_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Total individuals:** <font color="{change_color(year_change_total_individuals)}">{int(year_change_total_individuals):,} ({year_change_total_individuals_pc}%)</font>', unsafe_allow_html=True)
    col1.markdown(f'**Priority applications:** <font color="{change_color(year_change_priority_applications)}">{int(year_change_priority_applications):,} ({year_change_priority_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Priority individuals:** <font color="{change_color(year_change_priority_individuals)}">{int(year_change_priority_individuals):,} ({year_change_priority_individuals_pc}%)</font>', unsafe_allow_html=True)

