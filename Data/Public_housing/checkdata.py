import pandas as pd


Waitlist_latest = pd.read_csv("DATA\Public_housing\Waitlist_trend_long.csv")

check = Waitlist_latest.copy()
#keep only Description3, Description4, Description5, Description6, Description7
check = check[['Description3', 'Description4', 'Description5', 'Description6', 'Description7']]
#drop duplicates
check = check.drop_duplicates()
#save to csv
check.to_csv('DATA\Public_housing\check.csv', index=False)