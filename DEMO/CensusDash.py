import pandas as pd
from os import listdir
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html, dcc, Input, Output, State, callback

path_to_dir = '/Users/yhanalucas/Desktop/Dash/Data/Census/Multiyear'
description_file = '/Users/yhanalucas/Desktop/Dash/Data/census_file_details.csv'

def find_csv_filenames(path_to_dir, suffix='.csv'):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith( suffix )]

def get_data(path_to_dir, filenames, description_file):
    dataframes, homeless_data, total_data, objects_dict, numeric_dict, description = {}, {}, {}, {}, {}, {}
    description_df = pd.read_csv(description_file)
    for filename in filenames:
        key = filename.replace('_1621.csv', '')
        df = pd.read_csv(path_to_dir + '/' + filename)
        df['CENSUS_YEAR'] = df['CENSUS_YEAR'].astype('object')
        dataframes[key] = df
        homeless_data[key] = df.drop(columns=['TOTAL', 'NOT APPLICABLE'])
    for key in dataframes:
        objects = []
        numerics = []
        for column in dataframes[key].columns:
            if column in ['TOTAL', 'NOT APPLICABLE', 'CENSUS_YEAR']:
                continue
            elif dataframes[key][column].dtype == 'object':
                objects.append(column)

            elif dataframes[key][column].dtype in ['int64', 'float64']:
                numerics.append(column)
        objects_dict[key] = objects
        numeric_dict[key] = numerics
        description[description_df[description_df['FILE_NAME'] == key]['FILE_DESCRIPTION1'].values[0]] = key
        total_data[key] = dataframes[key].drop(columns=numerics)
    return dataframes, homeless_data, total_data, objects_dict, numeric_dict, description    
    
dataframes, homeless_data, total_data, objects_dict, numeric_dict, description = get_data(path_to_dir, find_csv_filenames(path_to_dir), description_file)



# Create a Dash application
app = dash.Dash(__name__)


app.layout = html.Div([
    # Census Data Header with white text
    html.Div([
        html.H1('Census Data', style={'font-family': 'Tahoma', 'color': 'white'})
    ], style={'width': '100%', 'background-color': 'rgb(34,17,97)'}),

    # Main content area with fixed background color
    html.Div([
        # Dropdowns centered on the left
        html.Div([
            html.Div([
                html.Br(),  # Add empty space before the first dropdown
                
                dcc.Dropdown(
                    id='dataset-dropdown',
                    options=[{'label': k, 'value': k} for k in description.keys()],
                    value=None,
                    style={'font-size': 'larger', 'font-family': 'Tahoma'}
                ),
                html.Div(id='dataset-description'),
                
                html.Br(),  # Add empty space before the second dropdown
                dcc.Dropdown(
                    id='state-dropdown',
                    style={'font-size': 'larger', 'font-family': 'Tahoma'}
                ),
                
                html.Button('Go', id='go-button', style={'font-size': 'larger', 'font-family': 'Tahoma'})
            ], style={'width': '100%', 'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column'}),
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'center'}),

        # Charts on the right
        html.Div([
            dcc.Graph(id='bar-chart'),
            dcc.Graph(id='pie-chart')
        ], style={'width': '67%', 'display': 'inline-block', 'vertical-align': 'top'})
    ], style={'background-color': 'rgb(34,17,97)'}),
], style={'background-color': 'rgb(34,17,97)', 'height': '100vh', 'width': '100vw'})



# Callback to update the dataset description
@app.callback(
    Output('dataset-description', 'children'),
    Input('dataset-dropdown', 'value')
)
def update_description(selected_dataset):
    return description.get(selected_dataset, '')

# Callback to update the state dropdown
@app.callback(
    Output('state-dropdown', 'options'),
    [Input('dataset-dropdown', 'value'), State('state-dropdown', 'value')]
)
def set_states_options(selected_dataset, selected_state):
    if selected_dataset:
        states = total_data[description[selected_dataset]]['STATE'].unique()
        states = ['All'] + sorted(set(states) - {'Western Australia'}) + ['Western Australia']
        return [{'label': state, 'value': state} for state in states]
    return []

# Callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('go-button', 'n_clicks')],
    [State('dataset-dropdown', 'value'), State('state-dropdown', 'value')]
)
def update_bar_chart(n_clicks, selected_dataset, selected_state):
    if n_clicks and selected_dataset and selected_state:
        df = total_data[description[selected_dataset]]
        if selected_state != 'All':
            df = df[df['STATE'] == selected_state]
        objects_list = objects_dict[description[selected_dataset]]
        if 'STATE' in objects_list:
            objects_list.remove('STATE')
        # Logic for creating the bar chart
        fig = go.Figure()
        for year in df['CENSUS_YEAR'].unique():
            fig.add_trace(go.Bar(x=df[objects_list[0]].unique(), y=df[df['CENSUS_YEAR'] == year]['TOTAL'], name=year))
        fig.update_layout(barmode='group')
        return fig
    return go.Figure()

# Callback to update the pie chart based on click data from the bar chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('bar-chart', 'clickData')],
    [State('dataset-dropdown', 'value'), State('state-dropdown', 'value')]
)
def display_click_data(clickData, selected_dataset, selected_state):
    if clickData and selected_dataset and selected_state:
        dataset_key = description[selected_dataset]
        df = homeless_data[dataset_key]
        objects_list = objects_dict[dataset_key]
        filtered_df = df[df[objects_list[0]] == clickData['points'][0]['label']]
        print(filtered_df)
        if selected_state != 'All':
            filtered_df = filtered_df[filtered_df['STATE'] == selected_state]
        #melt filtered_df, numeric_dict[dataset_key] = value columns
        filtered_df = filtered_df.melt(id_vars=['CENSUS_YEAR', 'STATE', objects_list[0]], value_vars=numeric_dict[dataset_key], var_name='Group', value_name='Count')
    

        bar2 = go.Figure()
        for year in filtered_df['CENSUS_YEAR'].unique():
            bar2.add_trace(go.Bar(x=filtered_df[filtered_df['CENSUS_YEAR'] == year]['Group'], y=filtered_df[filtered_df['CENSUS_YEAR'] == year]['Count'], name=year))
        bar2.update_layout(barmode='group')
        return bar2

    return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)
