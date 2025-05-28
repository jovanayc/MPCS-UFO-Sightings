import pandas as pd
import mysql.connector
import math
import re
from insert_keyword_data import insert_keyword_data
from insert_events_articles import add_events

# change this to your mysql password to run
MYPASSWORD = 'porcu555'

deduped = pd.read_csv(
    '../clean-data/ufo-data/combined_deduped.csv',
    low_memory=False,
    parse_dates=['date_reported']
)

deduped['occurred'] = pd.to_datetime(
    deduped['occurred'],
    format='%m/%d/%Y %H:%M',
    errors='coerce'
)

# # normalize column names to lowercase
# deduped.columns = [c.lower() for c in deduped.columns]

# rename 'speed_mph' column to 'speed'
if 'speed_mph' in deduped.columns:
    deduped.rename(columns={'speed_mph': 'speed'}, inplace=True)


# rename duration MM:SS to just duration
duration_cols = [c for c in deduped.columns if 'duration' in c]
if duration_cols:
    deduped.rename(columns={duration_cols[0]: 'duration'}, inplace=True)


# ensure 'shape' column exists
if 'shape' not in deduped.columns:
    deduped['shape'] = None

# initialize color column -- this will be populated later
if 'color' not in deduped.columns:
    deduped['color'] = None

# multiple crafts bool handled by finding word "multiple" in summary
deduped['summary'] = deduped['summary'].astype(str)
deduped['multiplecrafts'] = deduped['summary'].str.contains(r'\bmultiple\b', case=False)

# derive color from summary if missing... this is a pretty short list, so it may not capture everything
known_colors = [
    'red','blue','green','black','white','orange','yellow', 'beige', 'purplish'
    'purple','silver','gold','brown','grey','gray','pink', 'orangish', 'reddish', 'whitish'
]
def extract_color(text):
    # try to match variants ending in -ish (e.g., greenish, grayish)
    for color in known_colors:
        # allow optional 'ish' suffix
        pattern = r'\b' + re.escape(color) + r'(?:ish)?\b'
        if re.search(pattern, text, re.IGNORECASE):
            return color
    return 'Unknown'

# fill in colors
deduped['color'] = deduped['color'].where(deduped['color'].notnull() & (deduped['color'] != ''), None)
deduped['color'] = deduped.apply(
    lambda row: row['color'] if row['color'] else extract_color(row['summary']),
    axis=1
)

# NaN whack-a-mole chaos
def clean(val):
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

# replace all the NaNs with Nones
deduped = deduped.where(pd.notnull(deduped), None)


# put everything in mysql
cnx = mysql.connector.connect(
    host='localhost', user='root', password= MYPASSWORD, database='UFO'
)
cur = cnx.cursor()

# insert into locations:
loc_deduped = deduped[['city','state','country','longitude','latitude']].drop_duplicates()
loc_rows = [
    (
        clean(city), clean(state), clean(country),
        clean(lon), clean(lat)
    ) for city, state, country, lon, lat in loc_deduped.to_records(index=False)
]

deduped['has_coords'] = (
    deduped['longitude'].notna() &
    deduped['latitude'].notna()
)

# sort so ones with coord come first
deduped = deduped.sort_values(
    by='has_coords',
    ascending=False
)

# drop duplicates (ones with no coords)
loc_deduped = deduped.drop_duplicates(
    subset=['city','state','country'],
    keep='first'
)[['city','state','country','longitude','latitude']]

# drop helper column
deduped.drop(columns='has_coords', inplace=True)

loc_rows = [
    (
        clean(city), clean(state), clean(country),
        clean(lon), clean(lat)
    )
    for city, state, country, lon, lat
    in loc_deduped.to_records(index=False)
]


# insert ignore is similar to insert distinct except that it will just continue if 
# it encounters an error with a particular line
cur.executemany(
    """
    INSERT IGNORE INTO Location
      (City, State, Country, Longitude, Latitude)
    VALUES (%s, %s, %s, %s, %s)
    """, loc_rows
)
cnx.commit()

# build location map to match location ids to sightings further on
cur.execute(
    "SELECT LocationID, City, State, Country FROM Location"
)
loc_map = {}
for lid, city, state, country in cur.fetchall():
    loc_map[(
        city, state, country,
    )] = lid
# seed default Location for missing keys
cur.execute(
    "INSERT IGNORE INTO Location (City, State, Country, Longitude, Latitude) VALUES (%s,%s,%s,%s,%s)",
    ('Unknown','Unknown','Unknown', None, None)
)
cnx.commit()
# get default_loc_id
default_loc_id = loc_map.get(('Unknown','Unknown','Unknown', None, None))
# refresh loc_map including default 
if default_loc_id is None:
    cur.execute(
        "SELECT LocationID FROM Location WHERE City='Unknown' AND State='Unknown' AND Country='Unknown' LIMIT 1"
    )
    default_loc_id = cur.fetchone()[0]
    loc_map[('Unknown','Unknown','Unknown', None, None)] = default_loc_id

# insert into ufos
ufo_deduped = deduped[['speed','shape','color','multiplecrafts']].drop_duplicates()
ufo_rows = [
    (
        clean(speed), shape, color,
        bool(multi) if multi is not None else False
    )
    for speed, shape, color, multi in ufo_deduped.to_records(index=False)
]
cur.executemany(
    """
    INSERT IGNORE INTO UFO
      (Speed, Shape, Color, MultipleCrafts)
    VALUES (%s, %s, %s, %s)
    """, ufo_rows
)
cnx.commit()

cur.execute(
    """
    INSERT IGNORE INTO UFO
      (Speed, Shape, Color, MultipleCrafts)
    VALUES (NULL, 'Unknown', 'Unknown', FALSE)
    """
)
cnx.commit()

# again, build a map so that ufo id can be tied to a given sighting
cur.execute(
    "SELECT UFOID, Speed, Shape, Color, MultipleCrafts FROM UFO"
)
ufo_map = {}
for uid, speed, shape, color, multi in cur.fetchall():
    ufo_map[(
        float(speed) if speed is not None else None,
        shape, color,
        bool(multi)
    )] = uid


# insert sightings
sight_rows = []
for row in deduped.itertuples(index=False):
    loc_key = (
        row.city, row.state, row.country
    )
    ufo_key = (
        clean(row.speed), row.shape, row.color, bool(row.multiplecrafts)
    )
    sight_rows.append(
        (
            int(row.sighting_id),
            clean(row.summary),
            clean(row.duration),
            ufo_map.get(ufo_key), # here is where the maps are used
            loc_map.get(loc_key, default_loc_id),
            row.occurred,
            row.date_reported
        )
    )

cur.executemany(
    """
    INSERT IGNORE INTO Sightings
      (SightingID, Summary, Duration, UFOID, LocationID, Occurred, DateReported)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """,
    sight_rows
)
cnx.commit()

# call helper functions to insert additional since it must be done after the
# locations are in the table.
insert_keyword_data(cnx)
add_events(cnx)

cur.close()
cnx.close()