import pandas as pd
import re
import math
import numpy as np

# load csv
df = pd.read_csv(
    'ufo-data/ufo-sighting-db-scrubbed.csv',
    parse_dates=['datetime', 'date posted'],
    dtype={
        'duration (seconds)': str,
        'duration (hours/min)': str
    },
    low_memory=False
)

print("→ raw columns:", df.columns.tolist())

df = df.rename(columns={
    'duration (seconds)':    'duration_seconds',
    'duration (hours/min)':  'duration_hours_min'
})

# try to normalize duration into seconds
def parse_duration(row):
    # try the explicit-seconds field first
    sec = row.get('duration_seconds')
    if pd.notna(sec):
        # strip out anything but digits or dot
        s = re.sub(r'[^\d\.]', '', str(sec))
        try:
            return float(s)
        except ValueError:
            pass
    # fallback: parse the hours/minutes text
    txt = str(row.get('duration_hours_min') or '').lower()
    # strip non numeric chars
    txt = re.sub(r'\b(about|around|approx(imately)?)\b', '', txt)
    txt = txt.replace('.', '').strip()
    m = re.match(
        r'(?P<n1>\d+(\.\d+)?)(?:\s*[-–]\s*(?P<n2>\d+(\.\d+)?))?\s*'
        r'(?P<unit>sec|second|secs?|s|min|minute|mins?|hr|hour|hrs?)',
        txt
    )
    if not m:
        return pd.NA
    n1 = float(m.group('n1'))
    n2 = m.group('n2')
    val = (n1 + float(n2)) / 2 if n2 else n1
    unit = m.group('unit')
    if unit.startswith('sec'):
        return val
    if unit.startswith('min'):
        return val * 60
    if unit.startswith('hr'):
        return val * 3600
    return pd.NA

df['duration_seconds_norm'] = df.apply(parse_duration, axis=1)

# clean the all-lowercase text
df['city']    = df['city'].str.title().str.strip()
df['state']   = df['state'].str.upper().str.strip().fillna('')
df['country'] = df['country'].str.upper().str.strip().fillna('')
df['shape'] = df['shape'].str.title().str.strip()

# populate country column
us_states = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA',
    'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC', 'PR'
}
df['country'] = df['country'].replace({
    'AU': 'Australia',
    'GB': 'United Kingdom',
    'CA': 'Canada',
    'DE': 'Germany'
})
df.loc[df['state'].isin(us_states), 'country'] = 'USA'

# normalize city column
df['city'] = (
    df['city']
      .str.replace(r'\s*\(.*?\)', '', regex=True)
      .str.strip()
)

# drop any entries missing a country field, just for simplicity
df = df.dropna(subset=['country'])

# convert seconds to TIME format for SQL
def fmt_hms(total_seconds):
    try:
        s = math.ceil(total_seconds)
    except:
        return '00:00'
    # h = s // 3600
    m = (s // 60)
    sec = s % 60
    return f"{m:02d}:{sec:02d}"

    # return f"{h:02d}:{m:02d}:{sec:02d}"

df['duration(MM:SS)'] = df['duration_seconds_norm'].apply(fmt_hms)

speeds = df['comments'].str.extract(
    r'(?i)\b(?P<val>\d+(?:\.\d+)?)\s*(?P<unit>mph|kph)\b'
)

speeds['val']  = speeds['val'].astype(float)
speeds['unit'] = speeds['unit'].str.upper()


#convert to mph
df['speed_mph'] = np.where(
    speeds['unit'] == 'MPH',
    speeds['val'],
    np.where(speeds['unit'].isin(['KPH', 'KMPH']),
        speeds['val'] / 1.60934, np.nan
    )
)

# confirm final column names
final_cols = [
    'datetime','city','state','country','shape', 'speed_mph',
    'duration(MM:SS)','comments','date posted','latitude','longitude'
]
cleaned = df[final_cols]
# cleaned.columns = cleaned.columns.str.title()

cleaned.to_csv('ufo-data/kaggle_cleaned.csv', index=False)
print("Cleaned file saved to ufo-data/cleaned_sightings1.csv")
