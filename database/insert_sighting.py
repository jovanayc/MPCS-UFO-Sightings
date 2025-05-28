from datetime import datetime
from utils.db_utils import get_connection  # Make sure this is correct

def insert_new_sighting(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Insert Location
        cursor.execute("""
            INSERT INTO Location (City, State, Country)
            VALUES (%s, %s, %s)
        """, (data["city"], data["state"], data["country"]))
        location_id = cursor.lastrowid

        # 2. Insert UFO
        cursor.execute("""
            INSERT INTO UFO (Shape, Color, MultipleCrafts)
            VALUES (%s, %s, %s)
        """, (data["shape"], data["color"], int(data["multiple_crafts"])))
        ufo_id = cursor.lastrowid

        # 3. Insert Sighting
        cursor.execute("""
            INSERT INTO Sightings (Summary, Duration, UFOID, LocationID, Occurred, DateReported)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["summary"],
            data["duration"] if data["duration"] else None,
            ufo_id,
            location_id,
            datetime.combine(data["date_occurred"], datetime.min.time()),
            datetime.today()
        ))
        sighting_id = cursor.lastrowid

        # 4. Insert Keywords using KeywordTag and KeywordsInSighting
        keywords = [kw.strip().lower() for kw in data["summary"].split(",") if kw.strip()]
        for kw in keywords:
            # Check if keyword already exists
            cursor.execute("SELECT TagID FROM KeywordTag WHERE Keyword = %s", (kw,))
            result = cursor.fetchone()
            if result:
                keyword_id = result[0]
            else:
                cursor.execute("INSERT INTO KeywordTag (Keyword) VALUES (%s)", (kw,))
                keyword_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO KeywordsInSighting (TagID, SightingID) VALUES (%s, %s)",
                (keyword_id, sighting_id)
            )

        conn.commit()
        return True, "✅ New sighting inserted into database!", sighting_id

    except Exception as e:
        return False, f"❌ Failed to insert sighting: {e}", None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
