import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pandas.tseries.offsets import MonthEnd

# Load your data
df = pd.read_csv('/Users/yhanalucas/Desktop/Dash/Data/SHS/Long_Form/SHS_Reasons_Long_Form.csv')

df['MEASURE'] = df['MEASURE'].fillna('Count')
#VALUE DISPLAY AS ,.0F
df['VALUE'] = df['VALUE'].apply(lambda x: '{:,.0f}'.format(x))


app = dash.Dash(__name__)

# Extracting unique values for states, measures, and groups
states = ['Compare all'] + df['STATE'].unique().tolist()
measures = df['MEASURE'].unique().tolist()
groups = df['GROUP'].unique().tolist()

# Default values
default_state = 'WA'
default_measure = measures[0]

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in states],
            value=default_state,  # Default value set to 'All'
            clearable=False
        ),
        dcc.Dropdown(
            id='measure-dropdown',
            options=[{'label': measure, 'value': measure} for measure in measures],
            value=default_measure,  # Default measure
            clearable=False
        ),
        dcc.Dropdown(
            id='group-dropdown',
            options=[{'label': group, 'value': group} for group in groups],
            value=groups[0],  # Default group
            clearable=False
        )
    ], style={'width': '25%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='bar-chart')
    ], style={'width': '70%', 'display': 'inline-block'})
], style={'font-family': 'Tahoma'})  # Setting font to Tahoma

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('group-dropdown', 'value')]
)
def update_graph(selected_state, selected_measure, selected_group):
    # Filter and prepare data for plotting
    if selected_state == 'Compare all':
        df['DATE'] = pd.to_datetime(df['DATE'])
        df_filtered = df[df['DATE'] >= ((df['DATE']) - MonthEnd(1))]

        # Group by state and date, then aggregate values
        df_grouped = df_filtered[(df_filtered['STATE'] != 'National') & 
                                 (df_filtered['MEASURE'] == selected_measure) & 
                                 (df_filtered['GROUP'] == selected_group)].groupby(['STATE', 'DATE']).agg({'VALUE': 'sum'}).reset_index()

        # Sort the data to maintain consistent ordering
        df_grouped.sort_values(by=['STATE', 'DATE'], inplace=True)

        # Create the figure
        fig = go.Figure()

        # Plot each state's data as a separate trace
        for state in df_grouped['STATE'].unique():
            # Filter the grouped data for the current state
            state_data = df_grouped[df_grouped['STATE'] == state]
            # Create the x values as a list of tuples (state, date)
            x_values = list(zip([state]*len(state_data), state_data['DATE'].dt.strftime('%Y-%m')))
            # Add a bar trace for the current state
            fig.add_trace(go.Bar(
                x=x_values,
                y=state_data['VALUE'],
                name=state
            ))

        # Update the layout to support multi-category axes
        fig.update_layout(
            barmode='group',
            xaxis={'type': 'multicategory', 'categoryorder': 'array', 'categoryarray': x_values},
            xaxis_tickangle=-45,
            title=f'Comparison of All States - {selected_group} - {selected_measure}'
        )

    else:
        # Standard plot for a single state
        df_filtered = df[(df['STATE'] == selected_state) & 
                         (df['MEASURE'] == selected_measure) & 
                         (df['GROUP'] == selected_group)]
        fig = px.bar(df_filtered, x='DATE', y='VALUE', title=f'{selected_state} - {selected_group} - {selected_measure}', barmode='group')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
       

