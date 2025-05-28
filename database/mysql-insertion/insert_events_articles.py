import os
import re
import pandas as pd
from urllib.parse import urlparse

# helper function to add events / articles and related tables
def add_events(cnx):
    csv_dir = "../clean-data/ufo-data"  # shared dir

    loc_lookup_sql = """
    SELECT LocationID
        FROM Location
    WHERE City   = %s
        AND State  = %s
        AND Country= %s
    LIMIT 1
    """

    loc_insert_sql = """
    INSERT INTO Location (City, State, Country)
    VALUES (%s, %s, %s)
    """

    sightings_df = pd.read_csv(
        os.path.join(csv_dir, "cleaned_wiki_sightings.csv"),
        dtype={"EventID": int},
        ).fillna("")
    event_keys_df = pd.read_csv(
        os.path.join(csv_dir, "event_keywords.csv"),
        dtype={"KeywordID": int, "Keyword": str}
    )
    event_key_map_df = pd.read_csv(
        os.path.join(csv_dir, "event_keyword_mapping.csv"),
        dtype={"EventID": int,   "KeywordID": int}
    )

    # explode citation columns
    citation_cols = ["Citation_1","Citation_2","Citation_3","Citation_4"]
    df_long = (
        sightings_df
        .melt(id_vars=["EventID"], value_vars=citation_cols, value_name="url")
        .loc[lambda d: d["url"].str.strip() != ""]
        .assign(url=lambda d: d["url"].str.split(";"))
        .explode("url")
        .assign(
            url=lambda d: d["url"].str.strip(),
            title=lambda d: d["url"].map(slug_to_title),
            publisher=lambda d: d["url"].map(url_to_publisher),
            date_str=lambda d: d["url"].map(extract_date_from_url)
        )
    )

    cursor = cnx.cursor()

    # historical event with location id
    hist_rows = []
    for row in sightings_df.itertuples(index=False):
        eid = int(row.EventID)

        # parse date
        raw = pd.to_datetime(row.Date, errors="coerce")
        dt  = raw.date() if not pd.isna(raw) else None

        title = row.Name.strip() or f"Event {eid}"
        desc  = row.Description.strip()[:500]

        # get normalized location fields (use unknown instead of None for blank fields)
        city    = row.City.strip()    or "Unknown"
        state   = row.State.strip()   or "Unknown"
        country = row.Country.strip() or "Unknown"

        # does location exist?
        cursor.execute(loc_lookup_sql, (city, state, country))
        loc_hit = cursor.fetchone()
        if loc_hit:
            loc_id = loc_hit[0]
        else:
            # not found
            cursor.execute(loc_insert_sql, (city, state, country))
            cnx.commit()                # commit so lastrowid is valid
            loc_id = cursor.lastrowid

        # get historical event parameters
        hist_rows.append((eid, dt, title, desc, loc_id))

    # insert historical events (now with location id attached)
    cursor.executemany(
        """
        INSERT IGNORE INTO HistoricalEvent
        (EventID, EventDate, EventTitle, EventDescription, LocationID)
        VALUES (%s,      %s,        %s,           %s,                 %s)
        """,
        hist_rows
    )
    cnx.commit()
    print(f"Inserted {len(hist_rows)} HistoricalEvent rows...")

    # insert keyword tags and event keyword mapping
    cursor.executemany(
        "INSERT IGNORE INTO EventKeywordTag (TagID, Keyword) VALUES (%s, %s)",
        list(event_keys_df.itertuples(index=False, name=None))
    )
    cursor.executemany(
        "INSERT IGNORE INTO KeywordsInEvent (TagID, EventID) VALUES (%s, %s)",
        [(tag, evt) for evt, tag in event_key_map_df.itertuples(index=False, name=None)]
    )
    cnx.commit()
    print(f"Inserted {len(event_keys_df)} keywords and {len(event_key_map_df)} mappings.")

    # insert deduped articles
    insert_sql = """
    INSERT IGNORE INTO Article
        (EventID, ArticleTitle, URL, Publisher, Published)
    VALUES (%s,      %s,           %s,  %s,        %s)
    """
    seen = set()
    count = 0
    for eid, title, url, pub, date_str in df_long[["EventID","title","url","publisher","date_str"]].itertuples(index=False):
        key = (eid, url)
        if key in seen:
            continue
        seen.add(key)
        date_val = date_str or None
        cursor.execute(insert_sql, (int(eid), title, url, pub, date_val))
        count += 1

    cnx.commit()
    print(f"Inserted {count} Article rows...")

    # don't close connection because it will be closed externally, by whoever called this func
    cursor.close()
    print("Done loading events, keywords, articles...")


def slug_to_title(url):
    path = re.sub(r"[?#].*$", "", url)
    seg  = path.rstrip("/").split("/")[-1]
    seg  = re.sub(r"\.", "", seg)
    seg  = seg.replace("-", " ").replace("_", " ").strip()
    title = seg.title()
    # if no letters or only a single word, treat as missing
    if (not re.search(r"[A-Za-z]", title)) or (len(title.split()) < 2):
        return None
    return title

def url_to_publisher(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    for prefix in ("www.", "en.", "m."):
        if netloc.startswith(prefix):
            netloc = netloc[len(prefix):]
    return netloc or "none"

def extract_date_from_url(url: str) -> str:
    # first try contiguous YYYYMMDD between slashes
    m = re.search(r"/([12]\d{3})(\d{2})(\d{2})/", url)
    if m:
        y, mth, d = m.groups()
        return f"{y}-{mth}-{d}"
    # then try dashed or slashed
    m = re.search(r"([12]\d{3})[-/](\d{1,2})[-/](\d{1,2})", url)
    if m:
        y, mth, d = m.groups()
        return f"{y}-{int(mth):02d}-{int(d):02d}"
    return ""
