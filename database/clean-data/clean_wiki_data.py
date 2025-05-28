import pandas as pd
import re
from datetime import datetime

# regex for dates: https://uibakery.io/regex-library/date

df = pd.read_csv('ufo-data/wiki_sightings.csv', dtype=str, low_memory=False)

# assign event ids really quickly if not done
if 'EventID' not in df.columns:
    df.insert(0, 'EventID', range(100, 100 + len(df)))

def to_mysql_date(val):
    s = str(val).strip()

    # if there are two full dates, grab the first
    dates = re.findall(r'(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})', s)
    if dates:
        y, mo, da = dates[0]
        return f"{int(y):04d}-{int(mo):02d}-{int(da):02d}"

    m = re.match(r'^(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})$', s)
    if m:
        y, mo, da = m.groups()
        return f"{int(y):04d}-{int(mo):02d}-{int(da):02d}"

    # match different styles
    m = re.match(r'^(\d{1,2})\s*[/-]\s*(\d{1,2})\s*[/-]\s*(\d{4})$', s)
    if m:
        mo, da, y = m.groups()
        return f"{int(y):04d}-{int(mo):02d}-{int(da):02d}"

    # match c. (aka circa)
    m = re.match(r'^[cC]\.?\s*(\d{3,4})$', s)
    if m:
        y = int(m.group(1))
        return f"{y:04d}-01-01"

    # match AD
    m = re.search(r'(?:^AD\s*(\d{1,4})|(\d{1,4})\s*AD$)', s, re.IGNORECASE)
    if m:
        y = int(m.group(1) or m.group(2))
        return f"{y:04d}-01-01"

    # can't match BC
    if re.search(r'\bBC\b', s, re.IGNORECASE):
        return None

    # find just a year
    m = re.search(r'(?<!\d)(\d{4})(?!\d)', s)
    if m:
        y = int(m.group(1))
        return f"{y:04d}-01-01"

    return None


df['Date'] = df['Date'].apply(to_mysql_date)
df.to_csv('ufo-data/cleaned_wiki_sightings.csv', index=False)