import pandas as pd

full = pd.read_csv('04-DATA WIP (TO CLEAN)/Airbnb/Links/wa_tas_links.csv')
batch = full[full['region'] == 'Tasmania']
batch = batch[batch['type'] == 'calendar']
batch['type'] = batch['type'].replace('listingssummary', 'summary')
batch = batch.drop(columns=['region', 'bytes', 'publish status'])
#in datecolumn, replace / with -
batch['date'] = batch['date'].str.replace('/', '-')
batch = batch.reset_index(drop=True)
batch.to_csv('04-DATA WIP (TO CLEAN)/Airbnb/Links/batch_links.csv', index=False)

