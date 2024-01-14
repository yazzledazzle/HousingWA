import streamlit as st
import pandas as pd

update_log = pd.read_excel('DATA/SOURCE DATA/update_log.xlsx')

st.write('Update Log')
st.table(update_log)