import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Load and prepare the DataFrame
df = pd.read_csv('Data/SHS/Long_Form/SHS_Total_Client_Groups_Long_Form.csv')
df['DATE'] = pd.to_datetime(df['DATE'])
df['MEASURE'] = df['MEASURE'].astype(str)
df['CLIENT GROUP'] = df['CLIENT GROUP'].astype(str)

#ra_ref column is joined string of STATE, CLIENT GROUP, and MEASURE columns
df['ra_ref'] = df['STATE'] + '/' + df['CLIENT GROUP'] + '/' + df['MEASURE']
#for each unique ra_ref, calculate the rolling average
df['Rolling Avg'] = df.groupby(['ra_ref'])['VALUE'].rolling(12, min_periods=1).mean().reset_index(0,drop=True)

filtered_df = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'nan') & (df['CLIENT GROUP'] != 'Number of nights in short-term/emergency accommodation')]
print(filtered_df['CLIENT GROUP'].unique())


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
        #sort by date ascending 
        updated_df = updated_df.sort_values(by='DATE', ascending=True)
        df_per_10k = df[(df['STATE'] == 'WA') & (df['MEASURE'] == 'per 10k') & (df['CLIENT GROUP'] == clicked_group)]
        df_per_10k = df_per_10k.sort_values(by='DATE', ascending=True)
        #save to csv
        updated_df.to_csv('WIP/racheck.csv', index=False)
        df_per_10k.to_csv('WIP/racheck2.csv', index=False)
        # Create bar chart for clicked group
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=updated_df['DATE'], y=updated_df['VALUE'], mode='lines', name='Value', line=dict(color='royalblue')))

        # Add 12-month rolling average line
        fig.add_trace(go.Scatter(x=updated_df['DATE'], y=updated_df['Rolling Avg'], 
                                 mode='lines', name='12 Month Rolling Avg', line=dict(color='royalblue', dash='dash')))

        if not df_per_10k.empty:
            # Add lines for 'per 10k' measure and its rolling average
            fig.add_trace(go.Scatter(x=df_per_10k['DATE'], y=df_per_10k['VALUE'], 
                                     mode='lines', name='Per 10k', line = dict(color='darkorange'), yaxis='y2'))
            fig.add_trace(go.Scatter(x=df_per_10k['DATE'], y=df_per_10k['Rolling Avg'], 
                                     mode='lines', name='Rolling Avg per 10k', line=dict(dash='dash', color='darkorange'), yaxis='y2'))

            # Add a second y-axis for 'per 10k' data
            fig.update_layout(yaxis2=dict(title='Per 10k', overlaying='y', side='right', color='darkorange'))
        fig.update_layout(title=clicked_group, yaxis=dict(title='Clients', color='royalblue'))
    else:
        fig = px.bar()

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
