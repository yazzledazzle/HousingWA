import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('Data/SHS/Long_Form/SHS_Total_Client_Groups_Long_Form.csv')
df['DATE'] = pd.to_datetime(df['DATE'])
df['MEASURE'] = df['MEASURE'].astype(str)
df['CLIENT GROUP'] = df['CLIENT GROUP'].astype(str)
filtered_df = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'nan')]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Clear Selection', id='clear-button', n_clicks=0),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-chart', 'clickData'),
     Input('clear-button', 'n_clicks')])
def update_pie_chart(clickData, n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'] == 'clear-button.n_clicks':
        fig = px.pie(filtered_df, values='VALUE', names='CLIENT GROUP')
    else:
        clicked_group = clickData['points'][0]['label']
        updated_df = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'nan') & (df['CLIENT GROUP'] == clicked_group)]
        fig = px.pie(updated_df, values='VALUE', names='CLIENT GROUP')
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('pie-chart', 'clickData'))
def update_bar_chart(clickData):
    if clickData is not None:
        clicked_group = clickData['points'][0]['label']
        updated_df = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'nan') & (df['CLIENT GROUP'] == clicked_group)]

        # Rolling average calculation
        updated_df['Rolling Avg'] = updated_df['VALUE'].rolling(window=12, min_periods=1).mean()
        
        # Filter for 'per 10k' measure and calculate rolling average
        df_per_10k = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'per 10k') & (df['CLIENT GROUP'] == clicked_group)]
        df_per_10k['Rolling Avg per 10k'] = df_per_10k['VALUE'].rolling(window=12, min_periods=1).mean()

        # Create bar chart
        fig = px.bar(updated_df, x='DATE', y='VALUE')

        # Add 12-month rolling average line
        fig.add_trace(go.Scatter(x=updated_df['DATE'], y=updated_df['Rolling Avg'], 
                                 mode='lines', name='12 Month Rolling Avg'))

        # Add lines for 'per 10k' measure
        fig.add_trace(go.Scatter(x=df_per_10k['DATE'], y=df_per_10k['VALUE'], 
                                 mode='lines', name='Per 10k', yaxis='y2'))

        # Add rolling average line for 'per 10k' measure
        fig.add_trace(go.Scatter(x=df_per_10k['DATE'], y=df_per_10k['Rolling Avg per 10k'], 
                                 mode='lines', name='Rolling Avg per 10k', line=dict(dash='dot'), yaxis='y2'))

        # Add a second y-axis for 'per 10k' data
        fig.update_layout(yaxis2=dict(title='Per 10k', overlaying='y', side='right'))

    else:
        fig = px.bar()

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
