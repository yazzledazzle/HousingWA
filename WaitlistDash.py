import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from Waitlist_data import *
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__)

# Mock dataset
Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()
Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
datemax = Waitlist_trend['Date'].max()
daterange = sorted(Waitlist_trend['Date'].unique())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(fluid=True, style={'fontFamily': 'Tahoma'}, children=[
    dbc.Row([
        # Sidebar
        dbc.Col([
            dcc.Checklist(
                id='count-selection',
                options=[{'label': 'Applications', 'value': 'Applications'},
                         {'label': 'Individuals', 'value': 'Individuals'}],
                value=['Applications', 'Individuals']
            ),
            dcc.Checklist(
                id='category-selection',
                options=[{'label': 'Total', 'value': 'Total'},
                         {'label': 'Priority', 'value': 'Priority'}],
                value=['Total', 'Priority']
            ),
            dcc.RadioItems(
                id='plot-style-selection',
                options=[{'label': 'Line', 'value': 'Line'},
                        {'label': 'Bar', 'value': 'Bar'}],
                value='Line',
                inline=True
            ),
            dcc.Checklist(
                id='rolling-check',
                options=[{'label': 'Include 12 month rolling average line', 'value': 'rolling'}],
                value=['rolling']
            ),
            dcc.RangeSlider(
                id='date-slider',
                marks={i: {'label': pd.Timestamp(date).strftime('%b %y') if i % 4 == 0 else '', 'style': {'transform': 'rotate(-45deg)'}}
                       for i, date in enumerate(daterange[::3])},
                min=0,
                max=(len(daterange) - 1) // 3,
                value=[(len(daterange) - 12) // 3, (len(daterange) - 1) // 3]
            ),
        ], width=3),

        # Main content
        dbc.Col([
            dcc.Graph(id='main-graph')
        ], width=9),
    ]),
])

@app.callback(
    Output('plot-style-selection', 'options'),
    Input('count-selection', 'value')
)
def adjust_plot_options(count_of):
    options = [{'label': 'Line', 'value': 'Line'}]
    if not (set(['Applications', 'Individuals']) <= set(count_of)):
        options.append({'label': 'Bar', 'value': 'Bar'})
    return options

@app.callback(
    Output('main-graph', 'figure'),
    Input('count-selection', 'value'),
    Input('category-selection', 'value'),
    Input('plot-style-selection', 'value'),
    Input('rolling-check', 'value'),
    Input('date-slider', 'value')
)
def update_figure(count_of, show_categories, plot_style, rolling, date_range):
    start_date = daterange[int(date_range[0]*3)]
    end_date = daterange[int(date_range[1]*3)]

    filtered_data = Waitlist_trend[(Waitlist_trend['Date'] >= start_date) & (Waitlist_trend['Date'] <= end_date)]
    fig = go.Figure()

    data_configs = [
        # Priority Applications
    {
        'count': 'applications',
        'category': 'priority',
        'label': 'Priority Applications',
        'color': 'maroon',
        'rolling_color': 'plum',
        'rolling_col_label': '12month rolling average (priority applications)',
        'rolling_col_name': 'priority_applications_12m_rolling'
    },
    # Priority Individuals
    {
        'count': 'individuals',
        'category': 'priority',
        'label': 'Priority Individuals',
        'color': 'violet',
        'rolling_color': 'palevioletred',
        'rolling_col_label': '12month rolling average (priority individuals)',
        'rolling_col_name': 'priority_individuals_12m_rolling',
        'yaxis': 'y2' if len(show_categories) == 2 else 'y'
    },
    # Total Applications
    {
        'count': 'applications',
        'category': 'total',
        'label': 'Total Applications',
        'color': 'navy',
        'rolling_color': 'lightblue',
        'rolling_col_label': '12month rolling average (total applications)',
        'rolling_col_name': 'total_applications_12m_rolling'
    },
    # Total Individuals
    {
        'count': 'individuals',
        'category': 'total',
        'label': 'Total Individuals',
        'color': 'darkseagreen',
        'rolling_color': 'lightgreen',
        'rolling_col_label': '12month rolling average (total individuals)',
        'rolling_col_name': 'total_individuals_12m_rolling',
        'yaxis': 'y2' if len(show_categories) == 2 else 'y'
    }
    ]

    for config in data_configs:
        if config['category'] in show_categories and config['count'] in count_of:
            hover_text = '%{x} ' + config['label'] + '<br>' + '<b> %{y:,.0f}'
            if plot_style == "Line":
                fig.add_trace(go.Scatter(
                    x=filtered_data['Date'],
                    y=filtered_data[config['label']],
                    mode='lines',
                    name=config['label'],
                    line=dict(color=config['color']),
                    yaxis=config['yaxis'],
                    hovertemplate= hover_text + '<extra></extra>'
                ))
                if 'rolling' in rolling:
                    fig.add_trace(go.Scatter(
                        x=filtered_data['Date'],
                        y=filtered_data[config['rolling_col_name']],
                        mode='lines',
                        name=config['rolling_col_label'],
                        line=dict(color=config['rolling_color'], dash='dash'),
                        yaxis=config['yaxis'],
                        hovertemplate= hover_text + '<extra></extra>'
                    ))
            else:  # Bar chart
                fig.add_trace(go.Bar(
                    x=filtered_data['Date'],
                    y=filtered_data[config['label']],
                    name=config['label'],
                    marker_color=config['color'],
                    hover_text = '%{x} ' + config['label'] + '<br>' + '<b> %{y:,.0f}',
                    hovertemplate= hover_text + '<extra></extra>'
                ))
                fig.update_layout(barmode='stack')


    # Legend adjustments
    fig.update_layout(legend=dict(orientation="v", yanchor="top", y=1.1, xanchor="left", x=1.02))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
