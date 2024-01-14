import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('DATA\PROCESSED DATA\SHS\Long_Form\SHS_Total_Clients_Long_Form.csv')

df['MEASURE'] = df['MEASURE'].fillna('Persons')  # Replace NaN in MEASURE with 'Persons'

#Date is yyyy-mm-dd
df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d', errors='coerce')
#Date to mmm-yy
df['DATE'] = df['DATE'].dt.strftime('%b-%y')

df_total = df.drop(columns=['AGE GROUP'])

#pivot STATE
df_total = df_total.pivot_table(index=['DATE', 'MEASURE'], columns='STATE', values='VALUE', aggfunc='sum').reset_index()
st.write(df_total)

