import pandas as pd
import plotly.graph_objects as go   
from Waitlist_datav2 import *
from assets import *

Waitlist_trend, Waitlist_trend_monthly_change, _, _ = Waitlist_datav2()  
print(Waitlist_trend_monthly_change.columns)

def gap_filler(data, series):
    missing_dates = []
    for i in range(len(data)-1):
            if data['Date'].iloc[i] + pd.DateOffset(days=1) + pd.offsets.MonthEnd(0) != data['Date'].iloc[i+1]:    
                gap = round((data['Date'].iloc[i+1] - data['Date'].iloc[i]).days / 30) - 1
                diff = data[series].iloc[i+1] - data[series].iloc[i]
                for j in range(gap):
                    missing_date = data['Date'].iloc[i] + pd.DateOffset(days=1) + pd.offsets.MonthEnd(0)
                    proxy_value = round(data[series].iloc[i] + (diff / (gap+1)))
                    missing_dates.append(missing_date)
                    new_row = {'Date': missing_date, series: proxy_value}
                    data = pd.concat([data, pd.DataFrame(new_row, index=[0])], ignore_index=True)
    data = data.sort_values(by=['Date'])
    data = data.reset_index(drop=True)
    return data, missing_dates

def format_yticks(data, y0):
    max = data.max()
    if y0 == 0:
        min_y = 0
        if max > 10000:
            step = 5000
            max_y = max + (step - (max % step)) + step/5
        elif max > 5000:
            step = 2000
            max_y = max + (step - (max % step)) + step/2
        elif max > 2500:
            step = 1000
            max_y = max + (step - (max % step))
    else:
        min = data.min()
        if max > 5000:
            if max < 10000:
                step = 500
            else:
                step = 1000
        else:
            step = 250
        min_y = min - (min % step)
        max_y = max + (step - (max % step)) + step/3
    ytickvals = list(range(int(min_y), int(max_y) + step, step))
    y_intercept = data.iloc[0]
    if y_intercept not in ytickvals:
        ytickvals.append(y_intercept)
    ytickvals.sort()
    yticktext = []
    for val in ytickvals:
        if val == y_intercept:
            yticktext.append('')
        elif val % 1000 == 0:
            yticktext.append(f"{val // 1000}k")
        elif val % 500 == 0:
            yticktext.append(f"{val / 1000:.1f}k")
        elif val % 250 == 0:
            yticktext.append(f"{val / 1000:.2f}k")
        else:
            yticktext.append('-')
    return ytickvals, yticktext, min_y, max_y

def create_annotations(data, series):
    max_val = data[series].max()
    max_date = data[data[series] == max_val]['Date'].iloc[0]
    min_val = data[series].min()
    earliest_date = data['Date'].iloc[0]
    min_date = data[data[series] == min_val]['Date'].iloc[0]
    latest_val = data[series].iloc[-1]
    latest_date = data['Date'].iloc[-1]
    
    annotations = {}
    if max_date == latest_date:
        annotations['max_latest'] = dict(
            x=max_date,
            y=max_val,
            text=f"Peak: {max_val:,.0f} <br> ({max_date.strftime('%b %y')})",
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            ax=-40,
            ay=60,
            font=dict(
                family='Tahoma',
                size=12,
                color='white'
            ),
            bordercolor='red',
            borderwidth=1,
            borderpad=2,
            bgcolor='maroon'
        )
    elif max_date == earliest_date:
        annotations['max_earliest'] = dict(
            x=max_date,
            y=max_val,
            text=f"Peak: {max_val:,.0f} <br> ({max_date.strftime('%b %y')})",
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            ax=60,
            ay=60,
            font=dict(
                family='Tahoma',
                size=12,
                color='white'
            ),
            bordercolor='red',
            borderwidth=1,
            borderpad=2,
            bgcolor='maroon'
        )
    else:
        annotations['max'] = dict(
            x=max_date,
            y=max_val,
            text=f"Peak: {max_val:,.0f} <br> ({max_date.strftime('%b %y')})",
            showarrow=True,
            arrowhead=1,
            arrowsize=1,
            ax=0,
            ay=60,
            font=dict(
                family='Tahoma',
                size=12,
                color='white'
            ),
            bordercolor='red',
            borderwidth=1,
            borderpad=2,
            bgcolor='maroon'
        )
    if min_date == earliest_date:
       annotations['min_earliest'] = dict(
            x=min_date,
            y=min_val,
            text=f"Low: {min_val:,.0f} <br> ({min_date.strftime('%b %y')})",
            showarrow=True,
            arrowsize=1,
            arrowhead=1,
            ax=50,
            ay=50,
            font=dict(
                family='Tahoma',
                size=12,
                color='black'
            ),
            bordercolor='darkgreen',
            borderwidth=1,
            borderpad=2,
            bgcolor='lightgreen'
        )
    elif min_date == latest_date:
        annotations['min_latest'] = dict(
            x=min_date,
            y=min_val,
            text=f"Low: {min_val:,.0f} <br> ({min_date.strftime('%b %y')})",
            showarrow=True,
            arrowsize=1,
            arrowhead=1,
            ax=-40,
            ay=20,
            font=dict(
                family='Tahoma',
                size=12,
                color='black'
            ),
            bordercolor='darkgreen',
            borderwidth=1,
            borderpad=2,
            bgcolor='lightgreen'
        )
    else:
        annotations['min'] = dict(
            x=min_date,
            y=min_val,
            text=f"Low: {min_val:,.0f} <br> ({min_date.strftime('%b %y')})",
            showarrow=True,
            arrowsize=1,
            arrowhead=1,
            ax=20,
            ay=20,
            font=dict(
                family='Tahoma',
                size=12,
                color='black'
            ),
            bordercolor='darkgreen',
            borderwidth=1,
            borderpad=2,
            bgcolor='lightgreen'
        )
    if latest_date == min_date:
        return annotations
    elif latest_date == max_date:
        return annotations
    else:
        annotations['latest'] = dict(
            x=latest_date,
            y=latest_val,
            text=f"Latest: {latest_val:,.0f} <br> ({latest_date.strftime('%b %y')})",
            showarrow=True,
            arrowsize=1,
            arrowhead=1,
            ax=-40,
            ay=20,
            font=dict(
                family='Tahoma',
                size=12,
                color='black'
            ),
            bordercolor='darkblue',
            borderwidth=1,
            borderpad=2,
            bgcolor='powderblue'
        )
    
    return annotations

def get_xticks(data):
    dates = data.unique()
    xtickvals = dates.tolist()            
    xticktext = []
    for date in xtickvals:
        if date.month == 3:
            date = date.strftime('%b %y')
            xticktext.append(date)
        elif date.month == 6:
            date = date.strftime('%b %y')
            xticktext.append(date)
        elif date.month == 9:
            date = date.strftime('%b %y')
            xticktext.append(date)
        elif date.month == 12:
            date = date.strftime('%b %y')
            xticktext.append(date)
        elif date == dates.max():
            date = date.strftime('%b %y')
            xticktext.append(date)
        else:
            xticktext.append('-')
    return xtickvals, xticktext
        
def charts(data):
    data['Date'] = pd.to_datetime(data['Date'], format='%b %y')
    filtered_data = data[data['Date'] > '2021-08-01']
    charts = [
        {
            'series': 'priority_applications',
            'label': 'Priority Applications',
            'color': 'darkorange',
            'fillcolor': 'rgb(245, 66, 66)',
            'marker_color': 'maroon'
        },
        {
            'series': 'total_applications',
            'label': 'Total Applications',
            'color': 'navy',
            'fillcolor': 'rgb(66, 194, 245)',
            'marker_color': 'royalblue'
        },
        {
            'series': 'priority_individuals',
            'label': 'Priority Individuals',
            'color': 'violet',
            'fillcolor': 'rgb(245, 66, 245)',
            'marker_color': 'darkviolet'
        },
        {
            'series': 'total_individuals',
            'label': 'Total Individuals',
            'color': 'darkseagreen',
            'fillcolor': 'lightgreen',
            'marker_color': 'darkgreen'
        }
    ]
    return charts, filtered_data
    
def plot_line_12m(charts, filtered_data):  
    charts, filtered_data = charts(Waitlist_trend)
    filtered_data = filtered_data[filtered_data['Date'] > filtered_data['Date'].max() - pd.DateOffset(months=14)]
    figs = {}

    for chart in charts:
        series_data = filtered_data[['Date', chart['series']]]
        series_data = series_data.dropna()
        chart_data, missing_dates = gap_filler(series_data, chart['series'])
        chart_data['Date'] = pd.to_datetime(chart_data['Date'], format='%b %y')
        
        fig = go.Figure()

        xtickvals, xticktext = get_xticks(chart_data['Date'])
        ytickvals, yticktext, _, max_y = format_yticks(chart_data[chart['series']], 0)
        
        chart_data_markers = chart_data[1:]
        chart_data_markers = chart_data_markers[~chart_data_markers['Date'].isin(missing_dates)]
        
        fig.add_trace(go.Scatter(
            x=chart_data['Date'],
            y=chart_data[chart['series']],
            name=chart['label'],
            mode='lines',
            line=dict(width=1, color=chart['color'])
        ))

        fig.add_trace(go.Scatter(
            x=chart_data_markers['Date'],
            y=chart_data_markers[chart['series']],
            name=chart['label'],
            mode='markers',
            marker=dict(color=chart['marker_color'], size=3)
        ))

        fig.update_layout(
            width=600,
            height=500,
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=xtickvals,
                ticktext=xticktext, 
                tickangle=45,
                tickfont=dict(
                    family='Tahoma',
                    size=12
                ),
                showline=True,
                linewidth=2,
                linecolor='grey',
            ),
            yaxis=dict(
                range=[0, max_y],
                tickvals=ytickvals,
                ticktext=yticktext,
                showline=True,
                linewidth=2,
                linecolor='grey',
                tickfont=dict(
                    family='Tahoma',
                    size=12
                )),
            plot_bgcolor='white')
        
        annotations = create_annotations(chart_data, chart['series'])
        for annotation in annotations.values():
            fig.add_annotation(annotation)

        figs[str(chart['series']) + '_12mline'] = fig

        fig.write_image(f"assets/{chart['series']}.png")

    return figs['priority_applications_12mline'], figs['total_applications_12mline'], figs['priority_individuals_12mline'], figs['total_individuals_12mline']

def plot_monthly_change(charts, monthly_change):
    charts, monthly_change = charts(Waitlist_trend_monthly_change)
    #filter data to only include data from last 12 months
    monthly_change = monthly_change[monthly_change['Date'] > monthly_change['Date'].max() - pd.DateOffset(days=364)]
    #create bar chart for chart in charts, showing monthly change (may be positive or negative), treat x axis as categorical
    figs = {}

    for chart in charts:
        mc_data = monthly_change[monthly_change['Category'] == chart['series']]
        mc_data = mc_data.dropna(subset=['M Delta'])
        #sort by date
        mc_data = mc_data.sort_values(by=['Date'], ascending=True)
        mc_data = mc_data.reset_index(drop=True)
        #date to string 
        mc_data['Date'] = mc_data['Date'].dt.strftime('%b %y')
        mc_data['color'] = mc_data['M Delta'].apply(lambda x: 'green' if x < 0 else 'red')
        mc_data['textcolor'] = mc_data['M Delta'].apply(lambda x: 'white' if x < 0 else 'black')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=mc_data['M Delta'],
            name=chart['label'],
            marker_color=mc_data['color'],
            text=mc_data['Date'],
            textposition='outside',
            textfont=dict(
                family='Tahoma',
                size=12
            )
        ))

        fig.add_trace(go.Bar(
            y=mc_data['M Delta'],
            name=chart['label'],
            marker_color=mc_data['color'],
            text=mc_data['M Delta'],
            textposition='inside',
            textfont=dict(
                family='Tahoma',
                size=12,
                color=mc_data['textcolor']
            )
        ))
        

        fig.update_layout(
            width=600,
            height=500, barmode = 'overlay',
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            plot_bgcolor='white')

        figs[str(chart['series']) + '_change'] = fig
        fig.write_image(f"assets/{chart['series']}" + "_mc.png")


    return figs['priority_applications_mc'], figs['total_applications_mc'], figs['priority_individuals_mc'], figs['total_individuals_mc']

priority_applications_mc, total_applications_mc, priority_individuals_mc, total_individuals_mc = plot_monthly_change(charts, Waitlist_trend_monthly_change)