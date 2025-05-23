import streamlit as st
from datetime import date
from constants import UFO_SHAPES

def show_insert_form():
    # Initialize session state storage
    if "submitted_sightings" not in st.session_state:
        st.session_state.submitted_sightings = []

    with st.sidebar.expander("Insert a New Sighting", expanded=False):
        with st.form("new_sighting_form"):
            st.markdown("Enter details for a new UFO sighting:")

            date_input = st.date_input("Date", value=date.today())
            city = st.text_input("City")
            state = st.text_input("State (2-letter abbreviation)")
            shape = st.selectbox("Shape", UFO_SHAPES)
            duration = st.text_input("Duration (e.g., '5 min')")
            credibility = st.slider("Credibility Score", 0.0, 10.0, 5.0)
            notes = st.text_area("Notes (Optional)", height=100)

            submitted = st.form_submit_button("Submit Sighting")

            if submitted:
                # Validate required fields
                if len(state) != 2 or not state.isupper():
                    st.error("❌ State must be exactly 2 capital letters (e.g., 'AZ').")
                elif not city:
                    st.error("❌ City is required.")
                else:
                    st.session_state.submitted_sightings.append({
                        "Date": date_input,
                        "City": city,
                        "State": state,
                        "Shape": shape,
                        "Duration": duration,
                        "Credibility": credibility,
                        "Notes": notes
                    })
                    st.success(f"✅ New sighting logged")

