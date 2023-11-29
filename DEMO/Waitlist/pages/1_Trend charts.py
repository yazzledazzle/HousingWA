import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Waitlist_data import *

st.set_page_config(page_title='Trend charts', page_icon=':chart_with_upwards_trend:')

# User selection of data to graph
st.subheader('Select data to graph:')
# Create a multiselect box with the options 'Applications', 'Individuals', and 'Both'.
count_of= st.multiselect('**Choose count type/s to plot:**', ['Applications', 'Individuals'], default=['Applications', 'Individuals'])

# Define a callback function that updates the values of `Show_Applications` and `Show_Individuals` based on the selected options.
def update_count_selection(count_of):
    Show_Applications = 'Applications' in count_of
    Show_Individuals = 'Individuals' in count_of
    return Show_Applications, Show_Individuals

# Call the callback function to update the values of `Show_Applications` and `Show_Individuals`.
Show_Applications, Show_Individuals = update_count_selection(count_of)

show_categories = st.multiselect('**Choose category/ies to plot:**', ['Total', 'Priority'], default=['Total', 'Priority'])

def update_category_selection(show_categories):
    Show_Total = 'Total' in show_categories
    Show_Priority = 'Priority' in show_categories
    return Show_Total, Show_Priority

Show_Total, Show_Priority = update_category_selection(show_categories)

col1, col2, col3 = st.columns(3)

if Show_Applications and Show_Individuals:
    Plot_style = col1.radio(label='**Graph settings:**', options=['Line', 'Bar'], horizontal=True, disabled=True,
                            help='Bar plot and monthly changes not available when both Applications and Individuals selected')
else:
    Plot_style = col1.radio(label='**Graph settings:**', options=['Line', 'Bar'], horizontal=True)

col2.markdown('<br>', unsafe_allow_html=True)
monthly_counts_selected = col2.checkbox("Plot monthly counts", value=True)
monthly_changes_selected = col2.checkbox("Plot monthly changes", disabled=Show_Applications and Show_Individuals)
col3.markdown('<br>', unsafe_allow_html=True)
Show_Rolling = col3.checkbox('Include 12 month rolling average line', value=True)



# Date formatting and range slider
Waitlist_trend, Waitlist_latest, Waitlist_1m_ago, Waitlist_12m_ago = Waitlist_data()
Waitlist_trend['Date'] = pd.to_datetime(Waitlist_trend['Date'], format='%b %y')
datemax = Waitlist_trend['Date'].max()
lastyear = datemax - pd.DateOffset(years=1)
daterange = sorted(Waitlist_trend['Date'].unique())

select_date_slider = st.select_slider('**Select date range:**', options=daterange, value=(lastyear, datemax),
                                        format_func=lambda x: pd.Timestamp(x).strftime('%b %y'))
startgraph, endgraph = list(select_date_slider)[0], list(select_date_slider)[1]

# Graph plots on button click only
if not count_of or not show_categories:
    plot = st.button('Get graph', disabled=True, help='Select data to graph',)
else:
    plot = st.button('Get graph')


if plot:
    Waitlist_trend = Waitlist_trend[(Waitlist_trend['Date'] >= startgraph) & (Waitlist_trend['Date'] <= endgraph)]
    fig = go.Figure()

    # Define configurations for applications and individuals with new colors
    data_configs = [
        # Priority Applications
    {
        'name': 'applications',
        'label': 'Priority Applications',
        'color': 'maroon',
        'rolling_color': 'plum',
        'category': 'priority',
        'yaxis': 'y',
        'rolling_col_label': '12month rolling average (priority applications)',
        'rolling_col_name': 'priority_applications_12m_rolling'
    },
    # Priority Individuals
    {
        'name': 'individuals',
        'label': 'Priority Individuals',
        'color': 'violet',
        'rolling_color': 'palevioletred',
        'category': 'priority',
        'yaxis': 'y2' if Show_Applications else 'y',
        'rolling_col_label': '12month rolling average (priority individuals)',
        'rolling_col_name': 'priority_individuals_12m_rolling'
    },
    # Total Applications
    {
        'name': 'applications',
        'label': 'Total Applications',
        'color': 'navy',
        'rolling_color': 'lightblue',
        'category': 'total',
        'yaxis': 'y',
        'rolling_col_label': '12month rolling average (total applications)',
        'rolling_col_name': 'total_applications_12m_rolling'
    },
    # Total Individuals
    {
        'name': 'individuals',
        'label': 'Total Individuals',
        'color': 'darkseagreen',
        'rolling_color': 'lightgreen',
        'category': 'total',
        'yaxis': 'y2' if Show_Applications else 'y',
        'rolling_col_label': '12month rolling average (total individuals)',
        'rolling_col_name': 'total_individuals_12m_rolling'
    }
    ]

    # Bar/Scatter Plots
    for config in data_configs:
        if config['name'] == 'applications' and not Show_Applications:
            continue
        if config['name'] == 'individuals' and not Show_Individuals:
            continue

        # Check category-based condition
        if config['category'] == 'total' and not Show_Total:
            continue
        if config['category'] == 'priority' and not Show_Priority:
            continue

        column_name = config['category'] + "_" + config['name']

        # Define the hover template
        if Plot_style == 'Bar':
            if Show_Total and Show_Priority:
                hover_text = (
                    '%{x}' +  
                    config['name'] + '<br>' +
                    'Priority: <b>' + Waitlist_trend[('priority_' + config['name'])].apply('{:,.0f}'.format) + '<br>'
                    '</b>Total: <b>' + Waitlist_trend[('total_' + config['name'])].apply('{:,.0f}'.format)
                )
            elif Show_Total:
                hover_text = '%{x}' + config['name'] + '<br>' + 'Total: <b> %{y:,.0f}'  # Include the Date
            elif Show_Priority:
                hover_text = '%{x}<br>' + config['name'] + '<br>' + 'Priority:<b> %{y:,.0f}'  # Include the Date
            else:
                hover_text = '%{x}<br>' + '%{y:,.0f}'  # default, with Date included
        else:
            hover_text = '%{x} ' + column_name + '<br>' + '<b> %{y:,.0f}'


        # Bar plotting with the conditional hover template
        if Plot_style == 'Bar':
            # For priority bars, we plot them directly
            if config['category'] == 'priority':
                y_value = Waitlist_trend[config['category'] + "_" + config['name']]
            # For total bars, if we also have priority, then we subtract priority from total to avoid double counting
            elif config['category'] == 'total' and Show_Priority:
                y_value = Waitlist_trend['total_' + config['name']] - Waitlist_trend['priority_' + config['name']]
            else:
                y_value = Waitlist_trend['total_' + config['name']]

            fig.add_trace(go.Bar(
                x=Waitlist_trend['Date'],
                y=y_value,
                name=config['label'],
                marker_color=config['color'],
                yaxis=config['yaxis'],
                hovertemplate=hover_text + '<extra></extra>',  # Add '<extra></extra>' to hide extra hover info
            ))
            fig.update_layout(barmode='stack')
        else:
            fig.add_trace(go.Scatter(
                x=Waitlist_trend['Date'],
                y=Waitlist_trend[column_name],
                name=config['label'],
                line=dict(color=config['color'], width=2),
                yaxis=config['yaxis'],
                hovertemplate=hover_text + '<extra></extra>',  # Add '<extra></extra>' to hide extra hover info
            ))
            #if yaxis='y2', then move y2 axis to the right side
            if config['yaxis'] == 'y2':
                fig.update_layout(yaxis2=dict(overlaying='y', side='right', tickformat=",.0f"))



    # Rolling Average Plots
    if Show_Rolling:
        for config in data_configs:
            if config['name'] == 'applications' and not Show_Applications:
                continue
            if config['name'] == 'individuals' and not Show_Individuals:
                continue
            if config['category'] == 'total' and not Show_Total:
                continue
            if config['category'] == 'priority' and not Show_Priority:
                continue

            fig.add_trace(go.Scatter(
                x=Waitlist_trend['Date'],
                y=Waitlist_trend[config['rolling_col_name']],
                name=config['rolling_col_label'],
                line=dict(color=config['rolling_color'], width=2, dash='dot'),
                yaxis=config['yaxis'],
                hoverinfo='none',
                marker_opacity=0
            ))

    

    fig.update_layout(
    xaxis_tickangle=-45,
    xaxis=dict(tickvals=Waitlist_trend['Date'], tickformat='%b %y'),  # Show all x-axis labels
    yaxis=dict(tickformat=",.0f"),  # Formatting y-axis labels with no decimal places
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

    st.plotly_chart(fig, use_container_width=True)

