# Add_New_Sighting.py
import streamlit as st
from datetime import date, datetime
from constants import UFO_SHAPES, UFO_COLORS
from database.db_utils import get_connection
from database.insert_sighting import insert_new_sighting

st.title("Report a New UFO Sighting")

st.markdown("Fill out the form below to add a new sighting to the database.")

if "submitted_sightings" not in st.session_state:
    st.session_state.submitted_sightings = []

with st.form("new_sighting_form"):
    st.subheader("Sighting Details")

    # Basic info
    date_occurred = st.date_input("Date of Sighting", value=date.today())
    city = st.text_input("City")
    state = st.text_input("State (2-letter abbreviation)")
    country = st.text_input("Country", value="USA")
    shape = st.selectbox("UFO Shape", UFO_SHAPES)
    color = st.selectbox("UFO Color", UFO_COLORS)
    multiple_crafts = st.checkbox("Multiple crafts observed?")
    summary = st.text_area("Short description of what happened")

    submitted = st.form_submit_button("Submit Sighting")

    if submitted:
        if len(state) != 2 or not state.isupper():
            st.error("❌ State must be exactly 2 capital letters (e.g., 'AZ').")
        elif not city or not summary:
            st.error("❌ City and description are required.")
        else:
            from database.insert_sighting import insert_new_sighting  # <-- add this import at the top

            success, msg = insert_new_sighting({
                "city": city,
                "state": state,
                "country": country,
                "shape": shape,
                "color": color,
                "multiple_crafts": multiple_crafts,
                "summary": summary,
                "duration": duration,
                "date_occurred": date_occurred,
            })

            st.success(msg) if success else st.error(msg)