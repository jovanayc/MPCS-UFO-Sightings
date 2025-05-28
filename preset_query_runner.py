# preset_query_runner.py

import streamlit as st
import pandas as pd
from database.db_utils import get_connection

# Mapping of preset query names to their actual SQL
PRESET_SQL_QUERIES = {
    "Total Sightings Per Year": """
        SELECT YEAR(Occurred) as VisitedYear, COUNT(*) as TotalSightings
        FROM Sightings
        GROUP BY YEAR(Occurred)
        ORDER BY VisitedYear;
    """,

    "UFO Sightings by Country": """
        SELECT Country, COUNT(*) as SightingsPerCountry
        FROM Location
        WHERE Country IS NOT NULL
        GROUP BY Country
        ORDER BY Country ASC;
    """,

    "Sightings by Season in USA": """
        SELECT Location.Country,
               CASE
                   WHEN MONTH(Sightings.Occurred) IN (12, 1, 2) THEN 'Winter'
                   WHEN MONTH(Sightings.Occurred) IN (3, 4, 5) THEN 'Spring'
                   WHEN MONTH(Sightings.Occurred) IN (6, 7, 8) THEN 'Summer'
                   WHEN MONTH(Sightings.Occurred) IN (9, 10, 11) THEN 'Fall'
               END AS SightingSeason,
               COUNT(*) AS SeasonalSighting
        FROM Sightings
        JOIN Location ON Sightings.LocationID = Location.LocationID
        WHERE Location.Country = 'USA'
        GROUP BY Location.Country, SightingSeason
        ORDER BY SeasonalSighting DESC;
    """,

    "Article Mentions in Famous UFO Locations": """
        SELECT Article.ArticleTitle, COUNT(*) AS ReferenceCount
        FROM Sightings
        JOIN Location ON Sightings.LocationID = Location.LocationID
        JOIN HistoricalEvent ON Location.LocationID = HistoricalEvent.LocationID
        JOIN Article ON HistoricalEvent.EventID = Article.EventID
        WHERE Location.City IN ('Roswell', 'Phoenix', 'North Bergen')
              AND Article.ArticleTitle IS NOT NULL
              AND Article.ArticleTitle <> ''
        GROUP BY Article.ArticleTitle
        ORDER BY ReferenceCount DESC;
    """,

    "Average UFO Speed Per Year": """
        SELECT YEAR(Sightings.Occurred) AS SightedYear,
               ROUND(AVG(UFO.Speed)) AS AverageSpeed,
               COUNT(*) AS Sightings
        FROM UFO
        JOIN Sightings ON Sightings.UFOID = UFO.UFOID
        WHERE UFO.Speed IS NOT NULL
        GROUP BY SightedYear
        ORDER BY SightedYear;
    """,

    "Most Witnessed Sightings": """
        SELECT Location.City, Location.State, COUNT(*) AS Witnesses, UFO.Shape,
               DATE(Sightings.Occurred) AS VisitedDay
        FROM UFO
        JOIN Sightings ON Sightings.UFOID = UFO.UFOID
        JOIN Location ON Sightings.LocationID = Location.LocationID
        WHERE Location.City IS NOT NULL
        GROUP BY Location.City, Location.State, UFO.Shape, VisitedDay
        HAVING Witnesses > 3
        ORDER BY Witnesses DESC;
    """,

    "Top 100 Shapes by Country": """
        SELECT Location.Country, UFO.Shape, COUNT(*) AS CountryCount
        FROM UFO
        JOIN Sightings ON UFO.UFOID = Sightings.UFOID
        JOIN Location ON Sightings.LocationID = Location.LocationID
        WHERE Location.Country <> 'unknown'
        GROUP BY Location.Country, UFO.Shape
        ORDER BY CountryCount DESC
        LIMIT 100;
    """,

    "Military Base Mentions in Sightings": """
        SELECT UFO.Shape, Sightings.Duration, Location.City, Location.State, Sightings.Occurred
        FROM UFO
        JOIN Sightings ON UFO.UFOID = Sightings.UFOID
        JOIN Location ON Location.LocationID = Sightings.LocationID
        WHERE Sightings.Summary LIKE '%BASE%' OR Sightings.Summary LIKE '%Military%'
        ORDER BY Sightings.Duration DESC;
    """,

    "Illinois Sightings in Summer": """
        SELECT UFO.Shape, COUNT(*) AS ShapeSightings
        FROM UFO
        JOIN Sightings ON UFO.UFOID = Sightings.UFOID
        JOIN Location ON Sightings.LocationID = Location.LocationID
        WHERE Location.State = 'IL' AND MONTH(Sightings.Occurred) IN (6, 7, 8)
        GROUP BY UFO.Shape
        ORDER BY UFO.Shape;
    """,

    "Recent Chicago Sightings": """
        SELECT Sightings.Occurred, Location.City, Location.State, UFO.Shape, Sightings.Summary
        FROM Sightings
        JOIN Location ON Sightings.LocationID = Location.LocationID
        JOIN UFO ON Sightings.UFOID = UFO.UFOID
        WHERE Location.City = 'Chicago' AND Sightings.Occurred > '2020-12-31';
    """
}

def run_preset_query(query_title):
    st.markdown("## 📊 Results")
    st.markdown(
        f"<div style='font-size: 0.85rem; color: gray;'>Results for query: <i>{query_title}</i></div>",
        unsafe_allow_html=True
    )

    query = PRESET_SQL_QUERIES.get(query_title)

    if not query:
        st.error("Unknown query title.")
        return

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results)

    st.dataframe(df, use_container_width=True)

    cursor.close()
    conn.close()
