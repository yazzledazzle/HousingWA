import pandas as pd

full = pd.read_csv('04-DATA WIP (TO CLEAN)/Airbnb/Links/wa_tas_links.csv')
listings = full[full['type'] == 'listings']
listings.loc[:, 'date'] = listings['date'].str.replace('/', '-')
listings = listings.reset_index(drop=True)
listings.to_csv('04-DATA WIP (TO CLEAN)/Airbnb/Links/listings_links.csv', index=False)

