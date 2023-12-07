import pandas as pd
import plotly.graph_objects as go
import numpy as np

plot_df = pd.read_csv('/Users/yhanalucas/Desktop/Dash/Data/Public_housing/Waitlist_trend_long_plotting.csv')

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

def create_annotations(data):
    max_val = data['Value'].max()
    max_date = data[data['Value'] == max_val]['Date'].iloc[0]
    min_val = data['Value'].min()
    earliest_date = data['Date'].iloc[0]
    min_date = data[data['Value'] == min_val]['Date'].iloc[0]
    latest_val = data['Value'].iloc[-1]
    latest_date = data['Date'].iloc[-1]
    Annotations_count = 0
    Annotations_dict = {}
    
    class Annotation:
        def __init__(self, x, y, text, showarrow, arrowhead, arrowsize, ax, ay, font, bordercolor, borderwidth, borderpad, bgcolor):
            self.x = x
            self.y = y
            self.text = text
            self.showarrow = showarrow
            self.arrowhead = arrowhead
            self.arrowsize = arrowsize
            self.ax = ax
            self.ay = ay
            self.font = font
            self.bordercolor = bordercolor
            self.borderwidth = borderwidth
            self.borderpad = borderpad
            self.bgcolor = bgcolor

    if max_date == latest_date:
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
            x=max_date,
            y=max_val,
            text=f"Latest value is peak: {max_val:,.0f} <br> ({max_date.strftime('%b %y')})",
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
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
        return Annotations_dict
    elif latest_date == max_date:
        return Annotations_dict
    else:
        Annotations_count += 1
        Annotations_dict[Annotations_count] = Annotation(
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
    
    return Annotations_dict

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
        
def chartconfigs(plot_df):
    plot_df['Date'] = pd.to_datetime(plot_df['Date'], format='%Y-%m-%d')
    filtered_data = plot_df[plot_df['Date'] > '2021-08-01']
    charts = [
        {
            'Category': 'Priority Applications',
            'color': 'darkorange',
            'fillcolor': 'rgb(245, 66, 66)',
            'marker_color': 'maroon'
        },
        {
            'Category': 'Total Applications',
            'color': 'navy',
            'fillcolor': 'rgb(66, 194, 245)',
            'marker_color': 'royalblue'
        },
        {
            'Category': 'Priority Individuals',
            'color': 'violet',
            'fillcolor': 'rgb(245, 66, 245)',
            'marker_color': 'darkviolet'
        },
        {
            'Category': 'Total Individuals',
            'color': 'darkseagreen',
            'fillcolor': 'lightgreen',
            'marker_color': 'darkgreen'
        }
    ]
    return charts, filtered_data
    
def plot_line_12m(charts, filtered_data, save_name):
    filtered_data = filtered_data.copy()  
    if save_name != 'Log Line':
        filtered_data = filtered_data[filtered_data['Date'] > filtered_data['Date'].max() - pd.offsets.MonthEnd(12)]
    figs = {}

    for chart in charts:
        chart_data = filtered_data[filtered_data['Category'] == chart['Category']]
        chart_data = chart_data[chart_data['Metric'] == 'Waitlist figure']
        chart_data = chart_data[chart_data['Value type'] == 'Value']
        chart_data = chart_data.drop(columns=['Metric', 'Value type', 'Category'])
        chart_data['Date'] = pd.to_datetime(chart_data['Date'], format='%b %y')
        
        fig = go.Figure()            
        xtickvals, xticktext = get_xticks(chart_data['Date'])
        if save_name != 'Log Line':

            ytickvals, yticktext, _, max_y = format_yticks(chart_data['Value'], 0)
        
        chart_data_markers = chart_data[1:]
        missing_dates = chart_data[chart_data['Estimate flag - Waitlist figure'] == 'Y']['Date'].tolist()
        chart_data_markers = chart_data_markers[~chart_data_markers['Date'].isin(missing_dates)]
        
        fig.add_trace(go.Scatter(
            x=chart_data['Date'],
            y=chart_data['Value'],
            name=chart['Category'],
            mode='lines',
            line=dict(width=1, color=chart['color'])
        ))

        fig.add_trace(go.Scatter(
            x=chart_data_markers['Date'],
            y=chart_data_markers['Value'],
            name=chart['Category'],
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
            plot_bgcolor='white')

        if save_name != 'Log Line':
                fig.update_layout(
                    title= str(chart['Category']) + ' - 12 Month Trend',
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
                )))
        else:
            fig.update_layout(
                title = str(chart['Category']) + ' - log scale',
                yaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='grey',
                showticklabels=False))

        name = save_name + ' - ' + str(chart['Category'])
        figs[name] = fig
        fig.write_image(f"assets/charts/{name}.png")

    return

def plot_monthly_change(charts, filtered_data, save_name):
    
    monthly_change_chart_data = filtered_data.copy()
    monthly_change_chart_data = monthly_change_chart_data[monthly_change_chart_data['Date'] > monthly_change_chart_data['Date'].max() - pd.offsets.MonthEnd(12)]
    monthly_change_chart_data = monthly_change_chart_data[monthly_change_chart_data['Metric'] == 'Difference - Prior month']
    monthly_change_chart_data = monthly_change_chart_data[monthly_change_chart_data['Value type'] == 'Value']
    monthly_change_chart_data = monthly_change_chart_data.drop(columns=['Metric', 'Value type'])
    monthly_change_chart_data['Date'] = pd.to_datetime(monthly_change_chart_data['Date'], format='%Y-%m-%d')
    figs = {}

    for chart in charts:
        mc_data = monthly_change_chart_data[monthly_change_chart_data['Category'] == chart['Category']]
        mc_data = mc_data.drop(columns=['Category'])
        mc_data = mc_data.sort_values(by=['Date'], ascending=True)
        mc_data = mc_data.reset_index(drop=True)
        mc_data['Date'] = mc_data['Date'].dt.strftime('%b %y')
        mc_data['color'] = mc_data['Value'].apply(lambda x: 'green' if x < 0 else 'red')
        mc_data['textcolor'] = mc_data['Value'].apply(lambda x: 'white' if x < 0 else 'black')

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=mc_data['Value'],
            name=chart['Category'],
            marker_color=mc_data['color'],
            text=mc_data['Date'],
            textposition='outside',
            textfont=dict(
                family='Tahoma',
                size=12
            )
        ))

        fig.add_trace(go.Bar(
            y=mc_data['Value'],
            name=chart['Category'],
            marker_color=mc_data['color'],
            text=mc_data['Value'],
            textposition='inside',
            textfont=dict(
                family='Tahoma',
                size=12,
                color=mc_data['textcolor']
            )
        ))
        

        fig.update_layout(
            title= str(chart['Category']) + ' - Monthly Change',
            width=600,
            height=500, barmode = 'overlay',
            showlegend=False,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            plot_bgcolor='white')

        name = save_name + ' - ' + str(chart['Category'])
        figs[name] = fig
        fig.write_image(f"assets/charts/{name}.png")

    return

def bar_all_time(charts, filtered_data, save_name):
    figs = {}

    for chart in charts:
        chart_data = filtered_data[filtered_data['Category'] == chart['Category']]
        chart_data = chart_data[chart_data['Metric'] == 'Waitlist figure']
        chart_data = chart_data[chart_data['Value type'] == 'Value']
        chart_data = chart_data.drop(columns=['Metric', 'Value type', 'Category'])
        chart_data['Date'] = pd.to_datetime(chart_data['Date'], format='%b %y')

        # Convert 'Value' column to numeric type
        chart_data['Value'] = pd.to_numeric(chart_data['Value'], errors='coerce')
        chart_data['BarColor'] = 'skyblue'
 
        for row in chart_data.index:
            if chart_data.at[row, 'Estimate flag - Waitlist figure'] == 'Y':
                chart_data.at[row, 'BarColor'] = 'rgb(120, 122, 120)'
            elif chart_data.at[row, 'Value'] == chart_data['Value'].max():
                chart_data.at[row, 'BarColor'] = 'rgb(255, 18, 18)'
            elif chart_data.at[row, 'Value'] == chart_data['Value'].min():
                chart_data.at[row, 'BarColor'] = 'rgb(80, 255, 54)'
            elif chart_data.at[row, 'Value'] > chart_data.at[row - 1, 'Value']:
                chart_data.at[row, 'BarColor'] = 'rgb(181, 51, 51)'
            elif chart_data.at[row, 'Value'] < chart_data.at[row - 1, 'Value']:
                chart_data.at[row, 'BarColor'] = 'rgb(57, 120, 44)'
            else:
                chart_data.at[row, 'BarColor'] = 'rgb(41, 99, 138)'

        fig = go.Figure()

        xtickvals, xticktext = get_xticks(chart_data['Date'])
        ytickvals, yticktext, min_y, max_y = format_yticks(chart_data['Value'], chart_data['Value'].min())

        for group in chart_data['BarColor'].unique():
             fig.add_trace(go.Bar(
                x=chart_data[chart_data['BarColor'] == group]['Date'],
                y=chart_data[chart_data['BarColor'] == group]['Value'],
                name=chart['Category'],
                marker_color=group))
             



        fig.update_layout(
            barmode='stack',
            title= str(chart['Category']) + ' - cheeky bar',
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
                range=[min_y, max_y],
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
        


        annotations = create_annotations(chart_data)
        for Annotation in annotations.values():
            #add text to chart, underneath
            print(Annotation.text)
            

        name = save_name + ' - ' + str(chart['Category'])
        figs[name] = fig
        fig.write_image(f"assets/charts/{name}.png")


    return

charts, filtered_data = chartconfigs(plot_df)
plot_line_12m(charts, filtered_data, save_name='Line')
plot_monthly_change(charts, filtered_data, save_name='Monthly Change')
bar_all_time(charts, filtered_data, save_name='Cheeky')

log = filtered_data.copy()
log['Value'] = np.log(log['Value'])
log['Value'] = log['Value'].replace([np.inf, -np.inf], np.nan)
plot_line_12m(charts, log, save_name='Log Line')
