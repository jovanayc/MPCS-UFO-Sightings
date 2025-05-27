import pandas as pd

# helper function to add keyword data to database. called from populate_database module
def insert_keyword_data(cnx):
    kw_df = pd.read_csv('../clean-data/ufo-data/keywords.csv', dtype={'keyword_id': int, 'keyword': str})

    # sighting_keyword_pairs.csv has columns sighting_id,keyword_id
    kis_df = pd.read_csv(
        '../clean-data/ufo-data/sightid_keyid.csv',
        dtype={'sighting_id': int, 'keyword_id': int}
    )

    cur = cnx.cursor()

    # insert keywords into table
    kw_rows = [(int(r.keyword_id), r.keyword) for r in kw_df.itertuples(index=False)]
    cur.executemany(
        "INSERT IGNORE INTO KeywordTag (TagID, Keyword) VALUES (%s, %s)",
        kw_rows
    )
    cnx.commit()

    # insert data into keywords in sightings table
    kis_rows = [
        (int(r.sighting_id), int(r.keyword_id))
        for r in kis_df.itertuples(index=False)
]
    cur.executemany(
        "INSERT IGNORE INTO KeywordsInSighting (SightingID, TagID) VALUES (%s, %s)",
        kis_rows
    )
    cnx.commit()
    cur.close()
    return