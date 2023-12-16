import plotly.express as px
import plotly.graph_objects as go

Waitlist_trend_latest = pd.read_csv('DATA\Public_housing\Waitlist_trend_latest.csv')
Waitlist_trend = pd.read_csv('DATA\Public_housing\Waitlist_trend_long.csv')


#create class WaitlistTrend, all same attributes as WaitlistUpdate
class WaitlistTrend:
    def __init__(self, Date, ApplicantGroup, CountOf, Metric, MetricDetail, MetricAs, MetricCalc, MetricCalcAs, Estimate, Value):
        self.Date = Date
        self.ApplicantGroup = ApplicantGroup
        self.CountOf = CountOf
        self.Metric = Metric
        self.MetricDetail = MetricDetail
        self.MetricAs = MetricAs
        self.MetricCalc = MetricCalc
        self.MetricCalcAs = MetricCalcAs
        self.Estimate = Estimate
        self.Value = Value

# Create a list to hold instances of WaitlistTrend 
waitlist_trend = []
#iterate over each row in the DataFrame and create an instance of WaitlistTrend 
for index, row in Waitlist_trend.iterrows():
    trend = WaitlistTrend(
        Date = row['Date'],
        ApplicantGroup = row['Description1'],
        CountOf = row['Description2'],
        Metric = row['Description3'],
        MetricDetail = row['Description4'],
        MetricAs = row['Description5'],
        MetricCalc = row['Description6'],
        MetricCalcAs = row['Description7'],
        Estimate = row['Estimate'],
        Value = row['Value']
    )
    waitlist_trend.append(trend)

#initialize streamlit
st.title('Waitlist')
#get all objects with Group = Total, CountOf = Applications, Metric = Number, MetricCalc = Value
waitlist_total = [x for x in waitlist_trend if x.ApplicantGroup == 'Total' and x.CountOf == 'Applications' and x.Metric == 'Number' and x.MetricCalc == 'Value']
waitlist_total = pd.DataFrame.from_records([s.__dict__ for s in waitlist_total])
#plot waitlist_total trace with x=Date, y=Value using plotly
fig = px.line(waitlist_total, x='Date', y='Value', title='Total Applications')
st.plotly_chart(fig)