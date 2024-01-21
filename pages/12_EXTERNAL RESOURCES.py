import streamlit as st
import pandas as pd

external = pd.read_excel('assets/External.xlsx', sheet_name='Sheet1')

#button that points to , text = By-name list
st.markdown(f'<h3><a href ="https://www.endhomelessnesswa.com/bynamelist-datapage">Visit by-name list site </a></h3>', unsafe_allow_html=True)

for i in external.index:
    file = 'assets/' + external['File'][i]
    #display file - png 
    st.markdown(f'<h3>2023 housing affordability charts from Anglicare WA</h3>', unsafe_allow_html=True)
    st.markdown(f'<h5>{external["caption"][i]}</h5>', unsafe_allow_html=True)
    st.image(file, use_column_width=True)
    st.markdown(f'<a href="{external["Reference link"][i]}">Source: {external["Reference text"][i]}</a>', unsafe_allow_html=True)



