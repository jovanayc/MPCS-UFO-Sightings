import streamlit as st
from datetime import date
from constants import UFO_SHAPES, STATE_LIST

def show_custom_query_panel():
    with st.sidebar.expander("Build Your Own Query", expanded=False):
        st.markdown("Choose your filters to search past sightings:")

        date_range = st.date_input("Date Range", value=(date(2020, 1, 1), date.today()))
        selected_states = st.multiselect("State(s)", STATE_LIST)
        selected_shapes = st.multiselect("Shape(s)", UFO_SHAPES)
        credibility_range = st.slider("Credibility Score Range", 0.0, 10.0, (4.0, 9.0))

        run_custom = st.button("Run Custom Query")

    return run_custom, date_range, selected_states, selected_shapes, credibility_range