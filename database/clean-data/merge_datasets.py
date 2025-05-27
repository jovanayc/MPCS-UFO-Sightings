import pandas as pd

# load cleaned data
df1 = pd.read_csv(
    'ufo-data/kaggle_cleaned.csv',
    parse_dates=['datetime','date posted'],
    low_memory=False
)
df2 = pd.read_csv(
    'ufo-data/nuforc_cleaned.csv',
    parse_dates=['occurred','date_reported'],
    low_memory=False
)

# rename columns so they match
df1 = df1.rename(columns={
    'datetime':     'occurred',
    'date posted':  'date_reported',
    'comments':     'summary'
})

# fully concat tables without merging them yet
combined = pd.concat([df1, df2], ignore_index=True, sort=False)

# collapse duplicate sightings (matching on occurred, city, and state)
dedup = combined.groupby(
    ['occurred','city','state'], 
    as_index=False
).first()

dedup = dedup.reset_index(drop=True)
# just starting at a higher index so these are easier to differentiate
dedup.insert(0, 'sighting_id', dedup.index + 1000000)

dedup.to_csv(
    'ufo-data/combined_deduped.csv',
    index=False
)

print("Saved")