import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('DATA/PROCESSED DATA/ROGS/ROGS G19.csv', encoding='latin-1')
df['Year'] = df['Year'].astype(str)


st.markdown(f'Source: <a href="https://www.pc.gov.au/ongoing/report-on-government-services/2023/housing-and-homelessness/homelessness-services">Report on Government Services 2023, Part G, Section 19 - Homelessness Services</a>', unsafe_allow_html=True)


