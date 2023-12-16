import streamlit as st
import pandas as pd

Waitlist_trend_latest = pd.read_csv('DATA\Public_housing\Waitlist_trend_latest.csv')

class WaitlistUpdate:
    def __init__(self, Date, Category, Subcategory, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value, FontColor):
        self.Date = Date
        self.Category = Category
        self.Subcategory = Subcategory
        self.Metric = Metric
        self.MetricDetail = MetricDetail
        self.MetricAs = MetricAs
        self.MetricCalc = MetricCalc
        self.MetricCalcAs = MetricCalcAs
        self.Estimate = Estimate
        self.Value = Value
        self.FontColor = FontColor

waitlist_updates = []

for index, row in Waitlist_trend_latest.iterrows():
    update = WaitlistUpdate(
        Date = row['Date'],
        Category = row['Description1'],
        Subcategory = row['Description2'],
        Metric = row['Description3'],
        MetricDetail = row['Description4'],
        MetricAs = row['Description5'],
        MetricCalc = row['Description6'],
        MetricCalcAs = row['Description7'],
        Estimate = row['Estimate'],
        Value = row['Value'],
        FontColor = "red" if row['Value'] > 0 else "green"
    )
    waitlist_updates.append(update)

TotalApplications, TotalIndividuals, PriorityApplications, PriorityIndividuals, NonpriorityApplications, NonpriorityIndividuals, ProportionPriorityApplications, ProportionPriorityIndividuals, AveragePersonsTotal, AveragePersonsPriority, AveragePersonsNonpriority = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

categories = [(TotalApplications, 'Total', 'Applications'), 
              (TotalIndividuals, 'Total', 'Individuals'), 
              (PriorityApplications, 'Priority', 'Applications'), 
              (PriorityIndividuals, 'Priority', 'Individuals'),
                (NonpriorityApplications, 'Nonpriority', 'Applications'),
                (NonpriorityIndividuals, 'Nonpriority', 'Individuals'),
              (ProportionPriorityApplications, 'Proportion Priority', 'Applications'),
              (ProportionPriorityIndividuals, 'Proportion Priority', 'Individuals'),
                (AveragePersonsTotal, 'Average Number Of Individuals Per Application', 'Total'),
                (AveragePersonsPriority, 'Average Number Of Individuals Per Application', 'Priority'),
                (AveragePersonsNonpriority, 'Average Number Of Individuals Per Application', 'Nonpriority')
              ]
    
for category, cat1, cat2 in categories:
        category['Date'] = [x.Date for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2]
        category['Date'] = max(category['Date'])
        category['Value'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
        category['Prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Prior month change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
        category['Prior month change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
        category['Prior month change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior month' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
        category['Prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
        category['Prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Prior year change second order'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
        category['Prior year change second order %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
        category['Prior year change second order font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == 'prior year' and x.MetricAs == 'Actual' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
        category['Rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc == '-']
        category['Rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
        category['Rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Actual' and x.MetricCalc =='-']
        if cat2 == 'Individuals' and cat1 != 'Proportion Priority':
            category['per 10 000'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
            category['per 10 000 prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
            category['per 10 000 prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
            category['per 10 000 prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
            category['per 10 000 prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
            category['per 10 000 prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
            category['per 10 000 prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Number' and x.MetricAs == 'per 10 000' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
            category['per 10 000 rolling average'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
            category['per 10 000 rolling average difference'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
            category['per 10 000 rolling average difference %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'Percentage' and x.MetricCalc == '-']
            category['per 10 000 rolling average difference font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Difference' and x.MetricDetail == '12 month rolling average' and x.MetricAs == 'per 10 000' and x.MetricCalc == '-']
            category['percentage of population'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == '-']
            category['percentage of population prior month'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
            category['percentage of population prior month %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Percentage']
            category['percentage of population prior month font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior month' and x.MetricCalcAs == 'Actual']
            category['percentage of population prior year'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']
            category['percentage of population prior year %'] = [x.Value for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Percentage']
            category['percentage of population prior year font color'] = [x.FontColor for x in waitlist_updates if x.Category == cat1 and x.Subcategory == cat2 and x.Metric == 'Percentage of population' and x.MetricCalc == 'change from prior year' and x.MetricCalcAs == 'Actual']

#latest date is max of TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'], taken as datetime from yyyy-mm-dd, converted to dd mmmm yyyy
latest_date = max(TotalApplications['Date'], TotalIndividuals['Date'], PriorityApplications['Date'], PriorityIndividuals['Date'])
latest_date = pd.to_datetime(latest_date)
latest_date = latest_date.strftime('%d %B %Y')

#initialize streamlit
st.set_page_config(layout="wide")

st.markdown(f'## Latest waitlist data')
st.markdown(f'### As at ' + latest_date)
#two columns, heading2 on left  = Applications, heading2 on right = Individuals

st.markdown(f'''
<style>
    .custom-table {{
        width: 80%;
        border-collapse: separate;
    }}
    .custom-table th, .custom-table td {{
        font-family: Tahoma;
        text-align: center;
        border: none;
    }}
    .custom-table th {{
        background-color: transparent;
        border-bottom: none;
    }}
    .header-row {{
        font-weight: bold;
        background-color: transparent;
        border-bottom: 1px solid #d3d3d3;
    }}
    .data-row {{
        height: 1.2cm;
    }}
    .data-cell-total {{
        border-right: 3px dotted #d3d3d3;
        background-color: transparent;
    }}
            
    .data-cell-nonpriority {{
        background-color: #f0f0f0;
    }}
    
    .data-cell-priority {{
        background-color: #f7e7e6;
    }}
            
    .data-cell-proportion {{
        background-color: #f7f5e6;
        font-style: italic;
    }}

    .data-cell-total, .data-cell-priority, data-cell-nonpriority {{
        height: 0.8cm;
        width: 0.8cm;
    }}

    .header-cell-total {{
        border-right: 3px dotted #d3d3d3;
        background-color: transparent;
    }}
            
    .header-cell-priority {{
        background-color: #f7e7e6;
    }}
    
    .header-cell-proportion {{
        background-color: #f7f5e6;
            font-style: italic;
    }}
            
    .header-cell-nonpriority {{
        background-color: #f0f0f0;
    }}
            
    .header-cell-total, .header-cell-priority, .header-cell-nonpriority, .header-cell-proportion {{
        height: 1cm;
        width: 0.8cm;
        font-weight: bold;
        font-size: 14px;
    }}
    
    .header-applications {{
        background-color: #add8e6;
        font-weight: bold;
        font-size: 18px;
    }}
            
    .header-persons-per-application {{
        background-color: #cafaf8;
        font-style: italic;
        font-size: 14px;
    }}
            
    .header-individuals {{
        background-color: #90ee90;
        font-weight: bold;
        font-size: 18px;
    }}
            
    .header-individuals-per-10k {{
        background-color: #f0e68c;
        font-style: italic;
        font-size: 14px;
    }}
    
    .header-individuals-percentage {{
        background-color: #ffd4b3;
        font-style: italic;
        font-size: 14px;
    }}
    
    .spacer-column {{
        width: 0.1cm; 
    }}
</style>

<table class="custom-table">
    <tr>
        <td colspan="8" class="header-applications">APPLICATIONS</td>
        <td class="spacer-column"></td>
        <td colspan="12" class="header-individuals">PERSONS</td>
    </tr>
    <tr>
        <td colspan="4" class="header-cell-total"></td>
        <td class="spacer-column"></td>
        <td colspan="3" class="header-persons-per-application">Avg. persons per application</td>
        <td class="spacer-column"></td>
        <td colspan="4" class ="header-cell-total"></td>
        <td class="spacer-column"></td>
        <td colspan="3" class="header-individuals-per-10k">Per 10,000 people</td>
        <td class="spacer-column"></td>
        <td colspan="3" class="header-individuals-percentage">As percent of population</td>
        </tr>
    <tr class="header-row">
        <td class="header-cell-total">Total</td>
        <td class="header-cell-priority">Priority</td>
        <td class="header-cell-nonpriority">Non-priority</td>
        <td class="header-cell-proportion">% priority</td>
        <td class="spacer-column"></td>
        <td class="header-cell-total">Total</td>
        <td class="header-cell-priority">Priority</td>
        <td class="header-cell-nonpriority">Non-priority</td>
        <td class="spacer-column"></td>
        <td class="header-cell-total">Total</td>
        <td class="header-cell-priority">Priority</td>
        <td class="header-cell-nonpriority">Non-priority</td>
        <td class="header-cell-proportion">% priority</td>
        <td class="spacer-column"></td>
        <td class="header-cell-total">Total</td>
        <td class="header-cell-priority">Priority</td>
        <td class="header-cell-nonpriority">Non-priority</td>
        <td class="spacer-column"></td>
        <td class="header-cell-total">Total</td>
        <td class="header-cell-priority">Priority</td>
        <td class="header-cell-nonpriority">Non-priority</td>
    </tr>
    <tr class="data-row">
        <td class="data-cell-total">{TotalApplications["Value"][0]:,.0f}</td>
        <td class="data-cell-priority">{PriorityApplications["Value"][0]:,.0f}</td>
        <td class="data-cell-nonpriority">{NonpriorityApplications["Value"][0]:,.0f}</td>
        <td class="data-cell-proportion">{ProportionPriorityApplications["Value"][0]:,.1f}%</td>
        <td class="spacer-column"></td>
        <td class="data-cell-total">{AveragePersonsTotal["Value"][0]:,.1f}</td>
        <td class="data-cell-priority">{AveragePersonsPriority["Value"][0]:,.1f}</td>
        <td class="data-cell-nonpriority">{AveragePersonsNonpriority["Value"][0]:,.1f}</td>
        <td class="spacer-column"></td>
        <td class="data-cell-total">{TotalIndividuals["Value"][0]:,.0f}</td>
        <td class="data-cell-priority">{PriorityIndividuals["Value"][0]:,.0f}</td>
        <td class="data-cell-nonpriority">{NonpriorityIndividuals["Value"][0]:,.0f}</td>
        <td class="data-cell-proportion">{ProportionPriorityIndividuals["Value"][0]:,.1f}%</td>
        <td class="spacer-column"></td>
        <td class="data-cell-total">{TotalIndividuals["per 10 000"][0]:,.0f}</td>
        <td class="data-cell-priority">{PriorityIndividuals["per 10 000"][0]:,.0f}</td>
        <td class="data-cell-nonpriority">{NonpriorityIndividuals["per 10 000"][0]:,.0f}</td>
        <td class="spacer-column"></td>
        <td class="data-cell-total">{TotalIndividuals["percentage of population"][0]:,.2f}%</td>
        <td class="data-cell-priority">{PriorityIndividuals["percentage of population"][0]:,.2f}%</td>
        <td class="data-cell-nonpriority">{NonpriorityIndividuals["percentage of population"][0]:,.2f}%</td>
    </tr>
</table>
''', unsafe_allow_html=True)


