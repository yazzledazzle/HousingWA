import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from Waitlist_data import *
from assets import *

# Initialize the Dash app
app = dash.Dash(__name__)

def format_ticks(data, step=250):
    max_val = max(data)
    min_val = (min(data) // step) * step  
    
    tickvals = list(range(int(min_val), int(max_val) + step, step))
    
    ticktext = []
    for val in tickvals:
        if val % 1000 == 0:
            ticktext.append(f"{val // 1000}k")
        elif val % 500 == 0:
            ticktext.append(f"{val / 1000:.1f}k")
        else:
            ticktext.append(f"{val / 1000:.2f}k")
    return tickvals, ticktext



def plot_waitlist():
    Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()
    #create table Latest_total with columns RowName, Value, MonthChange, YearChange, 12mAverageChange
    Latest_total = pd.DataFrame(columns=['AtDate', 'Value', 'MonthChange', 'YearChange'])
    Latest_total_pc = pd.DataFrame(columns=['AtDate', 'Value', 'MonthChange%', 'YearChange%'])
    #create table Latest_priority with columns RowName, Value, MonthChange, YearChange, 12mAverageChange
    Latest_priority = pd.DataFrame(columns=['AtDate', 'Value', 'MonthChange', 'YearChange'])

    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
    filtered_data = Waitlist_trend[Waitlist_trend['Date'] > Waitlist_trend['Date'].max() - pd.DateOffset(months=12)]
    charts = [
        {
            'series': 'priority_applications',
            'label': 'Priority Applications',
            'color': 'maroon',
        },
        {
            'series': 'total_applications',
            'label': 'Total Applications',
            'color': 'navy',
        },
        {
            'series': 'priority_individuals',
            'label': 'Priority Individuals',
            'color': 'violet',
        },
        {
            'series': 'total_individuals',
            'label': 'Total Individuals',
            'color': 'darkseagreen',
        }
    ]

    figs = {}

    for chart in charts:
        fig = go.Figure()
        
        hover_text = '%{x} ' + chart['label'] + '<br>' + '<b> %{y:,.0f}'
        fig.add_trace(go.Bar(
            x=filtered_data['Date'],
            y=filtered_data[chart['series']],
            name=chart['label'],
            marker_color=chart['color'],
            hovertemplate=hover_text + '<extra></extra>'
        ))
        
        min_y_value = (filtered_data[chart['series']].min() // 250) * 250
        max_y_value = ((filtered_data[chart['series']].max() + 149) // 250) * 250
        tickvals, ticktext = format_ticks(filtered_data[chart['series']])

        
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ), 
            barmode='stack', 
            xaxis=dict(
                tickvals=filtered_data['Date'],
                tickformat="%b %y", showline=True
            ),
            yaxis=dict(
                range=[min_y_value, max_y_value], tickvals=tickvals, ticktext=ticktext, showline=True
                ),
            margin=dict(
                l=50,
                r=20,
                pad=4
            ),
            #add axis lines and grid lines
        )
        
        figs[chart['series']] = fig

    return figs['priority_applications'], figs['total_applications'], figs['priority_individuals'], figs['total_individuals']

priority_applicationsFig, total_applicationsFig, priority_individualsFig, total_individualsFig = plot_waitlist()


app.layout = html.Div(className='page', children=[
    html.Div(className="header-section", children=[
        html.Div(className="logo-container", children=[
            html.Img(src='assets/Logo.png', className='logo')
        ]),
        html.Div(children=[
            html.Div("DATA UPDATE", className="header-text-line1"),
            html.Div("Waitlist Data", className="header-text-line2"),
        ])
    ]),
    
    html.Div(className="content-section", children=[
        # Wait Turn section
        html.Div(className="wait-turn-section chart-section", children=[
            html.Div("Wait Turn", className="section-title"),
            html.Div(className='chart-containers', children=[
                dcc.Graph(figure=total_applicationsFig),
                dcc.Graph(figure=total_individualsFig)
            ]),
        ]),
        
        # Priority section
        html.Div(className='priority-section chart-section', children=[
            html.Div('Priority', className='section-title'),
            html.Div(className='chart-containers', children=[
                dcc.Graph(figure=priority_applicationsFig),
                dcc.Graph(figure=priority_individualsFig),
            ]),
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

