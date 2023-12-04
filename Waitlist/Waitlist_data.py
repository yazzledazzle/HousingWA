import pandas as pd
import streamlit as st

def Waitlist_data():

    Waitlist_trend = pd.read_csv('/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend.csv')
    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%Y-%m-%d')
    #sort by date ascending
    Waitlist_trend = Waitlist_trend.sort_values(by='Date', ascending=True)

    #calculate 12 month rolling average for each column of data - total_applications, total_individuals, priority_applications, priority_individuals
    Waitlist_trend['total_applications_12m_rolling'] = Waitlist_trend['total_applications'].rolling(window=12).mean()
    Waitlist_trend['total_individuals_12m_rolling'] = Waitlist_trend['total_individuals'].rolling(window=12).mean()
    Waitlist_trend['priority_applications_12m_rolling'] = Waitlist_trend['priority_applications'].rolling(window=12).mean()
    Waitlist_trend['priority_individuals_12m_rolling'] = Waitlist_trend['priority_individuals'].rolling(window=12).mean()

    #create a new dataframe with the latest data point for each column
    Waitlist_latest = Waitlist_trend.tail(1)

    #create a new dataframe with the data point from 1 month prior to the latest data point for each column
    Waitlist_1m_ago = Waitlist_trend.tail(2).head(1)

    #create a new dataframe with the data point from 12 months prior to the latest data point for each column, checking date column and then subtracting 12 months
    Waitlist_12m_ago = Waitlist_trend[Waitlist_trend['Date'] == Waitlist_latest['Date'].iloc[0] - pd.DateOffset(months=12)]


    return Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago


