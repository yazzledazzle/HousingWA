import streamlit as st
import pandas as pd


def change_color(val):
    """Returns color string for positive or negative values."""
    if val > 0:
        return "red"
    else:
        return "green"

def write_latest_Waitlist():

    col1, col2 = st.columns(2)

    latest_date = Waitlist_latest['Date'].iloc[0]
        #markdown header 2 - As at {latest_date} format dd mmm yyyy
    col1.markdown(f'### As at {latest_date.strftime("%d %b %Y")}:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    if not pd.isnull(Waitlist_latest['total_applications'].iloc[0]):   
        #markdown header 3 - Total applications: {latest_total_applications}
        col1.markdown(f'**Total applications:** {int(latest_total_applications):,}')

    if not pd.isnull(Waitlist_latest['total_individuals'].iloc[0]):
    #markdown header 3 - Total individuals: {latest_total_individuals}
        col2.markdown(f'**Total individuals:** {int(latest_total_individuals):,}')
        

    if not pd.isnull(Waitlist_latest['priority_applications'].iloc[0]):   
        #markdown header 3 - Priority applications: {latest_priority_applications}
        col1.markdown(f'**Priority applications:** {int(latest_priority_applications):,}')
       
    if not pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
        col2.markdown(f'**Priority individuals:** {int(latest_priority_individuals):,}')
        
    #if any are null
    if pd.isnull(Waitlist_latest['total_applications'].iloc[0]) or pd.isnull(Waitlist_latest['total_individuals'].iloc[0]) or pd.isnull(Waitlist_latest['priority_applications'].iloc[0]) or pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
    #markdown header 2 - Latest data at other dates
        col1.markdown('### Latest data where at other dates:')
        col2.markdown(f'### </br>', unsafe_allow_html=True)

        if pd.isnull(Waitlist_latest['total_applications'].iloc[0]):
            
            col1.markdown(f'**Total applications:** {int(latest_total_applications):,} as at {latest_total_applications_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['total_individuals'].iloc[0]):
           
            #markdown header 3 - Total individuals: {latest_total_individuals} as at {latest_total_individuals_date}
            col2.markdown(f'**Total individuals:** {int(latest_total_individuals):,} as at {latest_total_individuals_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['priority_applications'].iloc[0]):
            
            col1.markdown(f'**Priority applications:** {int(latest_priority_applications):,} as at {latest_priority_applications_date.strftime("%d %b %Y")}')
        if pd.isnull(Waitlist_latest['priority_individuals'].iloc[0]):
           
            col2.markdown(f'**Priority individuals:** {int(latest_priority_individuals):,} as at {latest_priority_individuals_date.strftime("%d %b %Y")}')



    # Updating display for monthly changes
    col1.markdown('### Monthly changes:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    col1.markdown(f'**Total applications:** <font color="{change_color(month_change_total_applications)}">{int(month_change_total_applications):,} ({month_change_total_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Total individuals:** <font color="{change_color(month_change_total_individuals)}">{int(month_change_total_individuals):,} ({month_change_total_individuals_pc}%)</font>', unsafe_allow_html=True)
    col1.markdown(f'**Priority applications:** <font color="{change_color(month_change_priority_applications)}">{int(month_change_priority_applications):,} ({month_change_priority_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Priority individuals:** <font color="{change_color(month_change_priority_individuals)}">{int(month_change_priority_individuals):,} ({month_change_priority_individuals_pc}%)</font>', unsafe_allow_html=True)

    # Updating display for annual changes
    col1.markdown('### Annual changes:')
    col2.markdown(f'### </br>', unsafe_allow_html=True)
    col1.markdown(f'**Total applications:** <font color="{change_color(year_change_total_applications)}">{int(year_change_total_applications):,} ({year_change_total_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Total individuals:** <font color="{change_color(year_change_total_individuals)}">{int(year_change_total_individuals):,} ({year_change_total_individuals_pc}%)</font>', unsafe_allow_html=True)
    col1.markdown(f'**Priority applications:** <font color="{change_color(year_change_priority_applications)}">{int(year_change_priority_applications):,} ({year_change_priority_applications_pc}%)</font>', unsafe_allow_html=True)
    col2.markdown(f'**Priority individuals:** <font color="{change_color(year_change_priority_individuals)}">{int(year_change_priority_individuals):,} ({year_change_priority_individuals_pc}%)</font>', unsafe_allow_html=True)

