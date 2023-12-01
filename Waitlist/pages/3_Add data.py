import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(page_title='Add data', page_icon=':plus-sign:')
Waitlist_trend = pd.read_csv('Data/CSV/Public_housing/Waitlist_trend.csv')
if 'data' not in st.session_state:
    data = pd.DataFrame({'Date':[],'total_applications':[],'total_individuals':[],'priority_applications':[],'priority_individuals':[]})
    st.session_state.data = data
data = st.session_state.data


def update_fields():
    row = pd.DataFrame({'Date':[st.session_state.Date],
            'total_applications':[st.session_state.total_applications],
            'total_individuals':[st.session_state.total_individuals],
            'priority_applications':[st.session_state.priority_applications],
            'priority_individuals':[st.session_state.priority_individuals]})
    st.session_state.data = pd.concat([st.session_state.data, row])

    
    if 'Date' in Waitlist_trend['Date'].tolist():
        check_and_overwrite(Waitlist_trend, row)
    else:
        append_new_data(Waitlist_trend, row)


def check_and_overwrite(Waitlist_trend, row):
    if row['total_applications'] != Waitlist_trend['total_applications']:
        if Waitlist_trend['total_applications'] == 0:
            Waitlist_trend['total_applications'] = row['total_applications']
        else:
            total_applications_current = Waitlist_trend['total_applications']
            total_applications_new = row['total_applications']
            st.write(f'Current dataset has a recorded value of {total_applications_current} total applications on this date. Do you want to overwrite this value with {total_applications_new}?')
            overwrite_total_applications = st.button('Yes, overwrite', key='overwrite_total_applications')
            if overwrite_total_applications:
                Waitlist_trend['total_applications'] = row['total_applications']
    if row['total_individuals'] != Waitlist_trend['total_individuals']:
        if Waitlist_trend['total_individuals'] == 0:
            Waitlist_trend['total_individuals'] = row['total_individuals']
        else:
            total_individuals_current = Waitlist_trend['total_individuals']
            total_individuals_new = row['total_individuals']
            st.write(f'Current dataset has a recorded value of {total_individuals_current} total individuals on this date. Do you want to overwrite this value with {total_individuals_new}?')
            overwrite_total_individuals = st.button('Yes, overwrite', key='overwrite_total_individuals')
            if overwrite_total_individuals:
                Waitlist_trend['total_individuals'] = row['total_individuals']
    if row['priority_applications'] != Waitlist_trend['priority_applications']:
        if Waitlist_trend['priority_applications'] == 0:
            Waitlist_trend['priority_applications'] = row['priority_applications']
        else:
            priority_applications_current = Waitlist_trend['priority_applications']
            priority_applications_new = row['priority_applications']
            st.write(f'Current dataset has a recorded value of {priority_applications_current} priority applications on this date. Do you want to overwrite this value with {priority_applications_new}?')
            overwrite_priority_applications = st.button('Yes, overwrite', key='overwrite_priority_applications')
            if overwrite_priority_applications:
                Waitlist_trend['priority_applications'] = row['priority_applications']
    if row['priority_individuals'] != Waitlist_trend['priority_individuals']:
        if Waitlist_trend['priority_individuals'] == 0:
            Waitlist_trend['priority_individuals'] = row['priority_individuals']
        else:
            priority_individuals_current = Waitlist_trend['priority_individuals']
            priority_individuals_new = row['priority_individuals']
            st.write(f'Current dataset has a recorded value of {priority_individuals_current} priority individuals on this date. Do you want to overwrite this value with {priority_individuals_new}?')
            overwrite_priority_individuals = st.button('Overwrite', key='overwrite_priority_individuals')
            if overwrite_priority_individuals:
                Waitlist_trend['priority_individuals'] = row['priority_individuals']
    Waitlist_trend.to_csv('Data/CSV/Public_housing/Waitlist_trend.csv', index=False)
    st.write('Data saved')

def append_new_data(Waitlist_trend, row):
    #convert row to dataframe

    new_row = pd.DataFrame({'Date':row['Date'],
            'total_applications':row['total_applications'],
            'total_individuals':row['total_individuals'],
            'priority_applications':row['priority_applications'],
            'priority_individuals':row['priority_individuals']})
    #format new row Date as %y-%m-%d no time
    new_row['Date'] = pd.to_datetime(new_row['Date']).dt.strftime('%Y-%m-%d')
    #concatenate new row to Waitlist_trend
    Waitlist_trend = pd.concat([Waitlist_trend, new_row])
    Waitlist_trend.to_csv('Data/CSV/Public_housing/Waitlist_trend_update.csv', index=False)
    st.write('Data saved')

dfForm = st.form(key='dfForm')
with dfForm:
    Date = st.date_input('Date', key='Date', max_value=pd.Timestamp(datetime.date.today()))
    dfColumns = st.columns(4)
    with dfColumns[0]:
        st.number_input('Total applications', step=100, min_value=0, key='total_applications')
    with dfColumns[1]:
        st.number_input('Total individuals', step=100, min_value=0, key='total_individuals')
    with dfColumns[2]:
        st.number_input('Priority applications', step=100, min_value=0, key='priority_applications')
    with dfColumns[3]:
        st.number_input('Priority individuals', step=100, min_value=0, key='priority_individuals')
    save = st.form_submit_button(on_click=update_fields)