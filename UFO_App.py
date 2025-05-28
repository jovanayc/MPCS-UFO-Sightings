# UFO_App.py

import streamlit as st
from preset_query_runner import run_preset_query
from utils.sidebar import show_sidebar_queries

st.set_page_config(page_title="UFO Sightings Explorer", layout="wide")

# --- Initialize session state ---
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "last_query" not in st.session_state:
    st.session_state.last_query = None
if "confirm_delete_index" not in st.session_state:
    st.session_state.confirm_delete_index = None

# --- Title and Intro ---
st.title("🛸 UFO Sightings Explorer")
st.markdown("👽 Welcome, Earthling.")
st.markdown("""
> You’ve stumbled upon a portal into the unknown.  
> Here lie over 70,000 reported encounters, eerie lights, and glimpses from the sky.  
> Learn at your own risk. Filter sightings. Decode patterns. Add your own encounter. 
>
> 🛸 To get started, select a pre-filled query from the left side panel.
> Be-boop.
""")

# --- Show all queries via sidebar ---
show_sidebar_queries()

# --- Display results if triggered ---
if st.session_state.get("last_query") and st.session_state.get("show_results"):
    run_preset_query(st.session_state.last_query)
