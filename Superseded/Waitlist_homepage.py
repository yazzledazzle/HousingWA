import streamlit as st
from Waitlist_calc_write import *
import pandas as pd
import io

# Set page configuration
st.set_page_config(page_title='Waitlist', page_icon=':clipboard:')
st.sidebar.success('Navigate using buttons above')

calc_and_write_waitlist(Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago)

#button to download Waitlist_trend df as csv
buffer = io.BytesIO()
@st.cache_data
def convert_df(Waitlist_trend):
   return Waitlist_trend.to_csv().encode('utf-8')

csv = convert_df(Waitlist_trend)

st.markdown(f' </br>', unsafe_allow_html=True)

st.download_button(
   "Download CSV of data",
   csv,
   "Waitlist_trend.csv",
   "text/csv",
   key='download-csv'
)

