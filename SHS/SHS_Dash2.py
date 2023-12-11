
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read the data
df = pd.read_csv('/Users/yhanalucas/Desktop/Dash/Data/SHS/WithPopulation/SHS_Reasons_WithPopulation.csv')


app = dash.Dash(__name__)

# Define regions
regions = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']

# App layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='group-dropdown',
            options=[{'label': val, 'value': val} for val in ['All'] + df['GROUP'].unique().tolist()],
            value='All',
            clearable=False
        ),
        dcc.Dropdown(
            id='measure-dropdown',
            options=[
                {'label': 'Count', 'value': 'Count'},
                {'label': 'Per 10,000 Population', 'value': 'Per 10k'}
            ],
            value='Count',
            clearable=False
        )
    ], style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='bar-chart')
    ], style={'width': '49%', 'display': 'inline-block'})
])

# Callback for updating the graph
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-chart', 'clickData'),
     Input('group-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_graph(click_data, group_value, measure_value):
    df_filtered = df.copy()

    if measure_value == 'Per 10k':
        for region in regions:
            df_filtered[region + '_PER_10k'] = df_filtered[region] / (df_filtered[region + '_POPULATION'] / 10000)
    
    if group_value != 'All':
        df_filtered = df_filtered[df_filtered['GROUP'] == group_value]

    # Check if no region is clicked on the bar chart
    if click_data is None or 'y' not in click_data['points'][0]:
        y_axis = [region + ('_PER_10k' if measure_value == 'Per 10k' else '') for region in regions]
        return px.bar(df_filtered, x='DATE', y=y_axis, title='Stacked Bar Chart', labels={'value': measure_value})

    # Get clicked region from the bar chart
    curve_idx = click_data['points'][0]['curveNumber']
    clicked_region = regions[curve_idx] + ('_PER_10k' if measure_value == 'Per 10k' else '')

    return px.bar(df_filtered, x='DATE', y=clicked_region, title=f'Bar Chart for {clicked_region}', labels={'value': measure_value})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
