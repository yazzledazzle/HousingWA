import pandas as pd

full = pd.read_csv('wa_tas_links.csv')
wa = full[full['region'] == 'Western Australia']
wa = wa[wa['type'] == 'listingssummary']
wa['type'] = wa['type'].replace('listingssummary', 'summary')
wa = wa.drop(columns=['region', 'bytes', 'publish status'])
wa = wa.reset_index(drop=True)
wa.to_csv('wa_links.csv', index=False)

