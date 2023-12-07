import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from Waitlist_data import *
from assets import *
from tabulate import tabulate

# Initialize the Dash app
app = dash.Dash(__name__)


def plot_waitlist():
    Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()
    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
    # filtered_data = last 12 months, based on date max
    filtered_data = Waitlist_trend[Waitlist_trend['Date'] > Waitlist_trend['Date'].max() - pd.DateOffset(months=12)]
    #make date format mmm yy 
    
    chart1_config = [
        {
            'series': 'priority_applications',
            'label': 'Priority Applications',
            'color': 'maroon',
            'rolling_color': 'plum',
            'rolling_col_label': '12month rolling average (priority applications)',
            'rolling_col_name': 'priority_applications_12m_rolling'
        },
        {
            'series': 'total_applications',
            'label': 'Total Applications',
            'color': 'navy',
            'rolling_color': 'lightblue',
            'rolling_col_label': '12month rolling average (total applications)',
            'rolling_col_name': 'total_applications_12m_rolling'
        }
        ]
    chart2_config = [
        {
            'series': 'priority_individuals',
            'label': 'Priority Individuals',
            'color': 'violet',
            'rolling_color': 'palevioletred',
            'rolling_col_label': '12month rolling average (priority individuals)',
            'rolling_col_name': 'priority_individuals_12m_rolling'
        },
        {
            'series': 'total_individuals',
            'label': 'Total Individuals',
            'color': 'darkseagreen',
            'rolling_color': 'lightgreen',
            'rolling_col_label': '12month rolling average (total individuals)',
            'rolling_col_name': 'total_individuals_12m_rolling'
        }
        ]

    WaitlistAppFig = go.Figure()

    for config in chart1_config:
        hover_text = '%{x} ' + config['label'] + '<br>' + '<b> %{y:,.0f}'
        WaitlistAppFig.add_trace(go.Bar(
        x=filtered_data['Date'],
        y=filtered_data[config['series']],
        name=config['label'],
        marker_color=config['color'],
        hovertemplate= hover_text + '<extra></extra>'
        ))

    WaitlistAppFig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
        xanchor="right",
    x=1
    ), barmode='stack', xaxis=dict(
            tickvals=filtered_data['Date'],
            tickformat="%b %y"
        )
    )



    WaitlistIndFig = go.Figure()

    for config in chart2_config:
        hover_text = '%{x} ' + config['label'] + '<br>' + '<b> %{y:,.0f}'
        WaitlistIndFig.add_trace(go.Bar(
        x=filtered_data['Date'],
        y=filtered_data[config['series']],
        name=config['label'],
        marker_color=config['color'],
        hovertemplate= hover_text + '<extra></extra>'
        ))

        # Legend adjustments
    WaitlistIndFig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
        xanchor="right",
    x=1
    ), barmode='stack', xaxis=dict(
            tickvals=filtered_data['Date'],
            tickformat="%b %y"
        )
    )




    return WaitlistAppFig, WaitlistIndFig

WaitlistAppFig, WaitlistIndFig = plot_waitlist()


app.layout = html.Div(children=[
    # Header section
    html.Div([
        html.Div(html.Img(src='assets/logo.png'), className="logo_header"),
        html.Div(html.H1('Housing report'), className="title_header"),
    ], className="header_background"),
    
    # Content section
    html.Div([
        # Waitlist applications header and chart
        html.H2('Waitlist applications'),
        dcc.Graph(figure=WaitlistAppFig),

        # Waitlist individuals header and chart
        html.H2('Waitlist individuals'),
        dcc.Graph(figure=WaitlistIndFig)
    ]),
], className="page")


if __name__ == '__main__':
    app.run_server(debug=True)
