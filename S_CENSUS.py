import streamlit as st
from DATA_SCRIPTS.CENSUS_DFs import *
import plotly.express as px
import plotly.graph_objects as go

def streamlit(total_data, objects_dict, description):
    st.title('Census Data')
    st.sidebar.title('Select dataset')
    dataset = st.sidebar.selectbox('Dataset', list(description.keys()))
    objects_list = objects_dict[description[dataset]]
    if dataset:
        st.write(description[dataset])
        if 'STATE' in objects_dict[description[dataset]]:
            state_list = total_data[description[dataset]]['STATE'].unique()
            #get index of Western Australia
            state_list = list(state_list)
            state_list.remove('Western Australia')
            state_list.insert(0, 'Western Australia')
            state_list.insert(1, 'All')
            state = st.sidebar.selectbox('State', state_list)
            show = st.sidebar.button('Go')
        if show:
            if state:
                if state == 'All':
                    df = total_data[description[dataset]].drop(columns=['STATE'])
                    objects_list.remove('STATE')
                    group_list = objects_list.copy()
                    group_list.insert(0, 'CENSUS_YEAR')
                    df = df.groupby(group_list).sum().reset_index()
                    #set    CENSUS_YEAR as object
                    df['CENSUS_YEAR'] = df['CENSUS_YEAR'].astype('object')
                else:
                    df = total_data[description[dataset]][total_data[description[dataset]]['STATE'] == state]
                    objects_list.remove('STATE')
                if len(objects_list) == 1: 
                    fig = go.Figure()
                    for year in df['CENSUS_YEAR'].unique():
                        fig.add_trace(go.Bar(x=df[objects_list[0]].unique(), y=df[df['CENSUS_YEAR'] == year]['TOTAL'], name=year))
                    fig.update_layout(barmode='group')
                    st.plotly_chart(fig)
                else:
                    st.write('Pending grouping')
            else:
                st.write('Select State')
        else:
            if len(objects_list) == 1: 
                    fig = go.Figure()
                    for year in df['CENSUS_YEAR'].unique():
                        fig.add_trace(go.Bar(x=df[objects_list[0]].unique(), y=df[df['CENSUS_YEAR'] == year]['TOTAL'], name=year))
                    fig.update_layout(barmode='group')
                    st.plotly_chart(fig)
            else:
                st.write('Pending grouping')
    else:
        st.write('Select dataset')
        return

dataframes, homeless_data, total_data, objects_dict, numeric_dict, description = get_data(path_to_dir, find_csv_filenames(path_to_dir), description_file)
streamlit(total_data, objects_dict, description)

