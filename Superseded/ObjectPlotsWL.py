st.title('Waitlist')
select = st.selectbox('Category', ['Applications', 'Individuals'])
if select == 'Applications':
    axis2 = st.selectbox('Second axis', ['Proportion of Waitlist that is priority', 'Average Number Of Individuals Per Application', 'None'])
else:
    axis2 = st.selectbox('Second axis', ['per 10 000', 'Percentage of population', 'None'])

fig = go.Figure()
if select == 'Applications':
    fig.add_trace(go.Scatter(x=TotalApplications['Date'], y=TotalApplications['Value'], mode='lines+markers', name='Total applications'))
    fig.add_trace(go.Scatter(x=NonpriorityApplications['Date'], y=NonpriorityApplications['Value'], mode='lines+markers', name='Non-priority applications', fill='tozeroy'))
    fig.add_trace(go.Scatter(x=PriorityApplications['Date'], y=PriorityApplications['Value'], mode='lines+markers', name='Priority applications', fill='tozeroy'))
    fig.update_layout(yaxis=dict(title='Applications'))
    if axis2 == 'Proportion of Waitlist that is priority':
        fig.add_trace(go.Scatter(x=ProportionPriorityApplications['Date'], y=ProportionPriorityApplications['Value'],mode='lines', name='Proportion priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Proportion priority (%)'), showlegend=True, title_text='Waitlist applications and priority percentage')
    elif axis2 == 'Average Number Of Individuals Per Application':
        fig.add_trace(go.Scatter(x=AveragePersonsTotal['Date'], y=AveragePersonsTotal['Value'],mode='lines', name='Avg persons -total', yaxis='y2'))
        fig.add_trace(go.Scatter(x=AveragePersonsNonpriority['Date'], y=AveragePersonsNonpriority['Value'],mode='lines', name='Avg persons - priority', yaxis='y2'))
        fig.add_trace(go.Scatter(x=AveragePersonsPriority['Date'], y=AveragePersonsPriority['Value'],mode='lines', name='Avg persons - non-priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Average persons'), showlegend=True, title_text='Waitlist applications and average persons per application')
    else:
        fig.update_layout(showlegend=True, title_text='Waitlist applications')
else:
    fig.add_trace(go.Scatter(x=TotalIndividuals['Date'], y=TotalIndividuals['Value'], mode='lines+markers', name='Total individuals'))
    fig.add_trace(go.Scatter(x=NonpriorityIndividuals['Date'], y=NonpriorityIndividuals['Value'], mode='lines+markers', name='Non-priority individuals', fill='tozeroy'))
    fig.add_trace(go.Scatter(x=PriorityIndividuals['Date'], y=PriorityIndividuals['Value'], mode='lines+markers', name='Priority individuals', fill='tozeroy'))
    fig.update_layout(yaxis=dict(title='Individuals'))
    if axis2 == 'per 10 000':
        fig.add_trace(go.Scatter(x=TotalIndividuals['Date'], y=TotalIndividuals['per 10 000'],mode='lines', name='per 10 000 - total', yaxis='y2'))
        fig.add_trace(go.Scatter(x=NonpriorityIndividuals['Date'], y=NonpriorityIndividuals['per 10 000'],mode='lines', name='per 10 000 - non-priority', yaxis='y2'))
        fig.add_trace(go.Scatter(x=PriorityIndividuals['Date'], y=PriorityIndividuals['per 10 000'],mode='lines', name='per 10 000 - priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='per 10 000 residents'), showlegend=True, title_text='Waitlist individuals and rate per 10 000 residents')
    elif axis2 == 'Percentage of population':
        fig.add_trace(go.Scatter(x=TotalIndividuals['Date'], y=TotalIndividuals['percentage of population'], mode='lines+markers', name='% population - total', yaxis='y2'))
        fig.add_trace(go.Scatter(x=NonpriorityIndividuals['Date'], y=NonpriorityIndividuals['percentage of population'], mode='lines+markers', name='% population- non-priority', yaxis='y2'))
        fig.add_trace(go.Scatter(x=PriorityIndividuals['Date'], y=PriorityIndividuals['percentage of population'], mode='lines+markers', name='% population - priority', yaxis='y2'))
        fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='% population'), showlegend=True, title_text='Waitlist individuals and percentage of population')
    else:
        fig.update_layout(showlegend=True, title_text='Waitlist individuals')



st.plotly_chart(fig)