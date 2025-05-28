import streamlit as st
from datetime import date, datetime
from constants import UFO_SHAPES, UFO_COLORS, STATE_LIST
import pandas as pd
import sys, os

# Add parent directory to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.insert_sighting import insert_new_sighting
from utils.db_utils import get_connection

st.title("🛸 Add a New UFO Sighting")

st.markdown("Help us document the unknown. Submit your UFO sighting below:")

with st.form("sighting_form"):
    # Input fields
    summary = st.text_area("What did you see?", placeholder="e.g. A bright light zig-zagging across the sky...", height=100)
    shape = st.selectbox("UFO Shape", [""] + UFO_SHAPES)
    color = st.selectbox("UFO Color", [""] + UFO_COLORS)
    multiple_crafts = st.selectbox("Were there multiple crafts?", ["Yes", "No"])
    duration = st.text_input("Duration (in seconds)", placeholder="Optional")
    
    st.markdown("---")
    st.markdown("### 📍 Location Info")
    city = st.text_input("City")
    state = st.selectbox("State", [""] + STATE_LIST)
    country = st.text_input("Country", value="USA")

    date_occurred = st.date_input("Date it happened", value=date.today())

    submitted = st.form_submit_button("Submit Sighting")

if submitted:
    if not summary or not state or not city:
        st.warning("Please fill in the summary, city, and state fields.")
    else:
        # Structure the data
        data = {
            "summary": summary,
            "shape": shape if shape else None,
            "color": color if color else None,
            "multiple_crafts": 1 if multiple_crafts == "Yes" else 0,
            "duration": duration,
            "city": city,
            "state": state,
            "country": country,
            "date_occurred": date_occurred
        }
        success, msg, new_id = insert_new_sighting(data)

        if success:
            st.success(msg)
            st.markdown("###Your Entry & Recent Sightings")

            # Show last 5 entries, highlighting the one just added
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT SightingID, Summary, Occurred, DateReported
                FROM Sightings
                ORDER BY SightingID DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)

            def highlight_new_row(row):
                return ['background-color: #b0e6b0' if row['SightingID'] == new_id else '' for _ in row]

            st.dataframe(df.style.apply(highlight_new_row, axis=1), use_container_width=True)

            cursor.close()
            conn.close()
        else:
            st.error(msg)