import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table as dt
import pandas as pd
import plotly.graph_objects as go   
from Waitlist_data import *
from Waitlist_latest_report import *
from assets import *



# Initialize the Dash app
app = dash.Dash(__name__)

Waitlist_latest_report, Waitlist_latest_report_pc_pt = Create_waitlist_latest_reports()
Waitlist_total_report = Waitlist_latest_report[Waitlist_latest_report['Group'] == 'Total']
Waitlist_priority_report = Waitlist_latest_report[Waitlist_latest_report['Group'] == 'Priority']

def get_notes(df):
    df = df.dropna(axis=1, how='all')
    notecheckdf = df
    notecheckdf = notecheckdf.drop(columns=['Date', '#', 'Prior month', 'Prior year', 'Rolling average', 'Prior year end'])
    note_print = []
    note_columns = [col for col in notecheckdf.columns if 'Note' in col]
    for col in note_columns:
        for i in range(len(notecheckdf)):
            if notecheckdf['Group'][i] == 'Total':
                notecheckdf[col][i] = notecheckdf[col][i].replace('for total_applications ', '*')
                notecheckdf[col][i] = notecheckdf[col][i].replace('for total_individuals ', '*')
            else:
                notecheckdf[col][i] = notecheckdf[col][i].replace('for priority_applications ', '*')
                notecheckdf[col][i] = notecheckdf[col][i].replace('for priority_individuals ', '*')
        if len(notecheckdf[col].unique()) == 1:
            note_print.append(notecheckdf[col].unique()[0])
        else:
            for i in range(len(notecheckdf)):
                notecheckdf[col][i] = notecheckdf[col][i].replace('*', ' for ' + notecheckdf['Count'][i])
                note_print.append(notecheckdf[col][i])
    note_print = [i.replace('*', '') for i in note_print]
    
    if len(note_print) == 0:
        return df
    elif len(note_print) == 1:
        notes = html.Div("Notes: </b>" + note_print[0], className="notes")
        return df, notes 
    else:
        #as above but with /b line breaks after each note
        notes = html.Div([html.Div("Notes: </b>" + note_print[i] + "</b>", className="notes") for i in range(len(note_print))])
        return df, notes 

def table(df):
    note_columns = [col for col in df.columns if 'Note' in col]
    unique_dates = df['Date'].unique()
    if len(unique_dates) == 1:
        date = unique_dates[0]
        df = df.rename(columns={'Count': f'At {date}'})
        df = df.drop(columns=['Date', 'Group'])
        df = df.drop(columns=note_columns)
    else:
        df[''] = df['Count'] + ' - at ' + df['Date']
        df = df.drop(columns=['Count', 'Date', 'Group'])
        df = df.drop(columns=note_columns)
    columns = [col for col in df.columns]
    return dt.DataTable(
      id='table',
      columns=[{"name": i, "id": i} for i in columns],
      data=df.to_dict(orient='records'),
      style_cell={'textAlign': 'center'},
      style_header={'backgroundColor': '#ccc', 'fontWeight': 'bold'},
      style_data={'backgroundColor': '#fff'},
    )

def format_yticks(data, step=250):
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

def get_xticks(data):
    dates = data.unique()
    tickvals = []
    for date in dates:
        if date == dates.min():
            tickvals.append(date)
        elif date.month == 3:
            tickvals.append(date)
        elif date.month == 6:
            tickvals.append(date)
        elif date.month == 9:
            tickvals.append(date)
        elif date.month == 12:
            tickvals.append(date)
        elif date == dates.max():
            tickvals.append(date)
        else:
            continue
    return tickvals



def plot_waitlist():
    Waitlist_trend, Waitlist_trend_rolling_average, Waitlist_trend_monthly_change, Waitlist_trend_yearly_change, Waitlist_trend_end_last_year = Waitlist_data()
    Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
    filtered_data = Waitlist_trend[Waitlist_trend['Date'] > '2021-08-01']
    charts = [
        {
            'series': 'priority_applications',
            'label': 'Priority Applications',
            'color': 'maroon',
            'fillcolor': 'rgb(245, 66, 66)'
        },
        {
            'series': 'total_applications',
            'label': 'Total Applications',
            'color': 'navy',
            'fillcolor': 'rgb(66, 194, 245)'
        },
        {
            'series': 'priority_individuals',
            'label': 'Priority Individuals',
            'color': 'violet',
            'fillcolor': 'rgb(245, 66, 245)'
        },
        {
            'series': 'total_individuals',
            'label': 'Total Individuals',
            'color': 'darkseagreen',
            'fillcolor': 'rgb(31, 222, 168)'
        }
    ]

    figs = {}

    for chart in charts:
        fig = go.Figure()

        hover_text = '%{x} ' + chart['label'] + '<br>' + '<b> %{y:,.0f}'
        fig.add_trace(go.Scatter(
            x=filtered_data['Date'],
            y=filtered_data[chart['series']],
            name=chart['label'],
            marker_color=chart['color'],
            line=dict(width=3),
            fillcolor=chart['fillcolor'],
            mode='lines',
            hovertemplate=hover_text + '<extra></extra>'
        ))
        

        
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ), 
            xaxis=dict(
                tickvals=filtered_data['Date'],
                tickformat="%b %y", showline=True
            ),
            
            yaxis=dict(
                #range=[min_y_value, max_y_value], tickvals=tickvals, ticktext=ticktext, 
                showline=True
                ),
            margin=dict(
                l=50,
                r=20,
                pad=4
            ),
        )
        
        figs[chart['series']] = fig

    return figs['priority_applications'], figs['total_applications'], figs['priority_individuals'], figs['total_individuals']

priority_applicationsFig, total_applicationsFig, priority_individualsFig, total_individualsFig = plot_waitlist()
wait_turn_df, wait_turn_notes = get_notes(Waitlist_total_report)




app.layout = html.Div(className='page-portrait', children=[
    html.Div(className="header-first-page-container", children=[
        html.Div(className="logo-header-container", children=[
            html.Img(src='assets/Logo.png', className='logo-header')
        ]),
        html.Div(children=[
            html.Div("DATA UPDATE", className="H2-right"),
            html.Div("Waitlist Data", className="H1-right"),
        ])
    ]),
    html.Div(table(Waitlist_total_report), className="table-container"),
    dcc.Graph(id='total_applicationsFig', figure=total_applicationsFig),
    dcc.Graph(id='total_individualsFig', figure=total_individualsFig),
])



if __name__ == '__main__':
    app.run_server(debug=True)

