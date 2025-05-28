# new_sighting.py
import streamlit as st
from datetime import date, datetime
from constants import UFO_SHAPES, UFO_COLORS
from database.db_utils import get_connection

def show_insert_form():
    if "submitted_sightings" not in st.session_state:
        st.session_state.submitted_sightings = []

    with st.sidebar.expander("Insert a New Sighting", expanded=False):
        with st.form("new_sighting_form"):
            st.markdown("Enter details for a new UFO sighting:")

            # Basic info
            date_occurred = st.date_input("Date of Sighting", value=date.today())
            city = st.text_input("City")
            state = st.text_input("State (2-letter abbreviation)")
            country = st.text_input("Country", value="USA")
            shape = st.selectbox("UFO Shape", UFO_SHAPES)
            color = st.selectbox("UFO Color", UFO_COLORS)
            multiple_crafts = st.checkbox("Multiple crafts observed?")
            summary = st.text_area("Short description of what happened")
            duration = st.text_input("Duration (hh:mm:ss)", placeholder="e.g. 00:05:00")

            submitted = st.form_submit_button("Submit Sighting")

            if submitted:
                if len(state) != 2 or not state.isupper():
                    st.error("❌ State must be exactly 2 capital letters (e.g., 'AZ').")
                elif not city or not summary:
                    st.error("❌ City and description are required.")
                else:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()

                        # --- Step 1: Insert Location (minimal for now) ---
                        cursor.execute("""
                            INSERT INTO Location (City, State, Country)
                            VALUES (%s, %s, %s)
                        """, (city, state, country))
                        location_id = cursor.lastrowid

                        # --- Step 2: Insert UFO ---
                        cursor.execute("""
                            INSERT INTO UFO (Shape, Color, MultipleCrafts)
                            VALUES (%s, %s, %s)
                        """, (shape, color, int(multiple_crafts)))
                        ufo_id = cursor.lastrowid

                        # --- Step 3: Insert Sighting ---
                        cursor.execute("""
                            INSERT INTO Sightings (Summary, Duration, UFOID, LocationID, Occurred, DateReported)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (
                            summary,
                            duration if duration else None,
                            ufo_id,
                            location_id,
                            datetime.combine(date_occurred, datetime.min.time()),
                            date.today()
                        ))

                        conn.commit()
                        cursor.close()
                        conn.close()

                        st.success("✅ New sighting inserted into database!")

                    except Exception as e:
                        st.error(f"❌ Failed to insert sighting: {e}")