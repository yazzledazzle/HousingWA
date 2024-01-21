import streamlit as st
import pandas as pd
import plotly.graph_objects as go


df_wa_total = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_WAtotals.csv')
df_wa_total['date'] = pd.to_datetime(df_wa_total['date'], format='%Y-%m-%d', errors='coerce')
df_wa_total = df_wa_total.sort_values(by='date', ascending=True)

fig = go.Figure()
for room_type in df_wa_total['room_type'].unique():
    df_room_type = df_wa_total[df_wa_total['room_type'] == room_type]
    fig.add_trace(go.Bar(x=df_room_type['date'], y=df_room_type['count_listings'], name=room_type))
fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
fig.update_layout(title='Number of Airbnb listings in WA by type', xaxis_title='', yaxis_title='Number of listings')
st.plotly_chart(fig)

df_full = pd.read_csv('DATA/PROCESSED DATA/Market and economy/Airbnb_full.csv')
df_full['ced&elec'] = df_full['ced'] + ' - ' + df_full['electorate']
print(df_full['ced&elec'].unique())
