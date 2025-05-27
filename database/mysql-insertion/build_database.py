import mysql.connector as mysc
from mysql.connector import errorcode

# remember to fill in with your own pwd!
config = {
    'user':     'root',
    'password': 'porcu555',
    'host':     'localhost',
}

try:
    cnx    = mysc.connect(**config)
    cursor = cnx.cursor()
except mysc.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("check username and pwd")
    else:
        print(err)
    exit(1)

cursor.execute("CREATE DATABASE IF NOT EXISTS UFO;")
cursor.execute("USE UFO;")

tables = {}
# Carter, I like the decision you made about where to put long and lat 
# these seem to be mostly geocoded by city, and aren't unique per sighting
# so this reduces redundancy. Made some slight changes to not null values 
# during debugging because the data is not totally uniform
tables['Location'] = (
    """
    CREATE TABLE IF NOT EXISTS Location(
        LocationID   INT NOT NULL AUTO_INCREMENT,
        City         VARCHAR(100),
        State        VARCHAR(100),
        Country      VARCHAR(100)  NOT NULL,
        Longitude    DECIMAL(8,5),
        Latitude     DECIMAL(8,5),
        PRIMARY KEY (LocationID)
    );
    """
)

# changes: speed is now a real, removed state
tables['UFO'] = (
    """
    CREATE TABLE IF NOT EXISTS UFO(
        UFOID           INT NOT NULL AUTO_INCREMENT,
        Speed           REAL(12,5),
        Shape           VARCHAR(50) NOT NULL,
        Color           VARCHAR(50),
        MultipleCrafts  BOOL        NOT NULL DEFAULT FALSE,
        PRIMARY KEY (UFOID)
    );
    """
)

# changes: added foreign key location id
tables['HistoricalEvent'] = (
    """
    CREATE TABLE IF NOT EXISTS HistoricalEvent(
        EventID           INT      NOT NULL,
        LocationID        INT,
        EventDate         DATE,
        EventTitle        VARCHAR(100) NOT NULL,
        EventDescription  VARCHAR(500) NOT NULL,
        PRIMARY KEY (EventID),
        FOREIGN KEY (LocationID)
            REFERENCES Location(LocationID)
            ON DELETE SET NULL
    );
    """
)

# changes: added foreign key eventid
tables['Article'] = (
    """
    CREATE TABLE IF NOT EXISTS Article(
        ArticleID     INT NOT NULL AUTO_INCREMENT,
        ArticleTitle  VARCHAR(200) NOT NULL,
        EventID       INT,
        URL           VARCHAR(200) NOT NULL,
        Published     DATE,
        Publisher     VARCHAR(100),
        PRIMARY KEY (ArticleID),
        FOREIGN KEY (EventID)
            REFERENCES HistoricalEvent(EventID)
            ON DELETE SET NULL
    );
    """
)
# changes: a couple of field name changes (Occurred, Date Reported, Summary)
# changed duration to a time because of how I chose to parse that data
# I think on delete should be cascade for sighting id – what do you both think?
tables['Sightings'] = (
    """
    CREATE TABLE IF NOT EXISTS Sightings(
        SightingID          INT      NOT NULL,
        Summary             VARCHAR(800),
        Duration            TIME,
        UFOID               INT      ,
        LocationID          INT      ,
        Occurred            DATETIME NOT NULL,
        DateReported        DATE NOT NULL,
        PRIMARY KEY (SightingID),
        -- ON DELETE CASCADE or RESTRICT?
        FOREIGN KEY (LocationID)
            REFERENCES Location(LocationID)
            ON DELETE CASCADE,
        FOREIGN KEY (UFOID)
            REFERENCES UFO(UFOID)
            ON DELETE CASCADE
    );
    """
)

# changes: separated this into two small tables to solve the 
# problem of how to make keywords distinct. Now there is a table
# for which keywords are used in which sighting summaries – this 
# will save on lengthy string search queries, imo, but curious what
# you both think. It follows the 3nf requirements to make this a 
# separate table, too.
tables['KeywordTag'] = (
    """
    CREATE TABLE IF NOT EXISTS KeywordTag(
        TagID     INT    NOT NULL,
        Keyword   VARCHAR(50) NOT NULL,
        PRIMARY KEY (TagID)
    );
    """
)

tables['KeywordsInSighting'] = (
    """
    CREATE TABLE IF NOT EXISTS KeywordsInSighting(
        TagID     INT    NOT NULL,
        SightingID INT   NOT NULL,
        PRIMARY KEY (SightingID, TagID),
        FOREIGN KEY (SightingID)
            REFERENCES Sightings(SightingID),
        FOREIGN KEY (TagID)
            REFERENCES KeywordTag(TagID)
    );
    """
)

# adding a separate table for event keywords – I couldn't figure out how to combine these
# easily and I think there might be reasons to keep them separate.
tables['EventKeywordTag'] = (
    """
    CREATE TABLE IF NOT EXISTS EventKeywordTag(
        TagID     INT    NOT NULL,
        Keyword   VARCHAR(50) NOT NULL,
        PRIMARY KEY (TagID)
    );
    """
)

# keyword event map
tables['KeywordsInEvent'] = (
    """
    CREATE TABLE IF NOT EXISTS KeywordsInEvent(
        TagID     INT    NOT NULL,
        EventID INT   NOT NULL,
        PRIMARY KEY (EventID, TagID),
        FOREIGN KEY (EventID)
            REFERENCES HistoricalEvent(EventID),
        FOREIGN KEY (TagID)
            REFERENCES EventKeywordTag(TagID)
    );
    """
)

for name, ddl in tables.items():
    print(f"Creating table '{name}' . . .")
    cursor.execute(ddl)

cnx.commit()
cursor.close()
cnx.close()