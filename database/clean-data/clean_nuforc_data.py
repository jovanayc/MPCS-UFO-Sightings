import pandas as pd, numpy as np

df2 = pd.read_csv(
    'ufo-data/nuforc_scraped.csv',   
    dtype=str,
    low_memory=False
)

df2.columns = (
    df2.columns
       .str.strip()
       .str.lower()
       .str.replace(' ', '_')
)

# extract speed if there
speeds2 = df2['summary'].str.extract(
    r'(?i)\b(?P<val>\d+(?:\.\d+)?)\s*(?P<unit>mph|kph|kmh|kmp h?)\b'
)
speeds2['val']  = speeds2['val'].astype(float)
speeds2['unit'] = speeds2['unit'].str.upper().replace({'KMH':'KPH','KMPH':'KPH'})

# convert to mph
conditions = [
    speeds2['unit'] == 'MPH',
    speeds2['unit'] == 'KPH',
    speeds2['unit'] == 'KMPH',

]
choices = [
    speeds2['val'],
    speeds2['val'] / 1.60934,
    speeds2['val'] / 1.60934,
]
df2['speed_mph'] = np.select(conditions, choices, default=np.nan)

df2.to_csv('ufo-data/nuforc_cleaned.csv', index=False,
        #    columns=[*df2.columns, 'speed_mph']
           )
print("Saved")