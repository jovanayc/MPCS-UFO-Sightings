import streamlit as st
from mock_queries import run_mock_query, run_custom_mock_query
from side_panel.new_sighting import show_insert_form
from side_panel.build_custom_query import show_custom_query_panel


st.set_page_config(page_title="UFO Sightings Explorer", layout="wide")

st.title("🛸 UFO Sightings Explorer")

st.markdown("👽 Welcome, Earthling.")
st.markdown("""
    > You’ve stumbled upon a portal into the unknown.
    > Here lie over 70,000 reported encounters, eerie lights, and glimpses from the sky.
    > 🛸 Learn at your own risk. Filter sightings. Decode patterns. Add your own encounter. Be-boop.
""")

# --- Layout for query input ---
col1, col2 = st.columns([4, 1])
query_choice = col1.selectbox(
    label="Choose a query:",
    options=[
        "Show all sightings",
        "Sighting by top UFO location in the past 10 years",
        "Sightings from 1990 - 1999 in Phoenix Arizona"
    ],
    label_visibility="collapsed"
)

# --- Initialize session state ---
if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "last_query" not in st.session_state:
    st.session_state.last_query = None

# -- Run Query button press
run_query = col2.button("Run Query")

# -- On run query button press
if run_query:
    st.session_state.last_query = query_choice
    st.session_state.query_history.append(query_choice)
    run_mock_query(query_choice) # connects to mock_queries to run query
elif st.session_state.last_query:
    run_mock_query(st.session_state.last_query)


# --- Display query history ---
if st.session_state.query_history:
    st.markdown("Recent Queries")
    # to show recent quereies in a button to easily rerun
    for i, q in enumerate(reversed(st.session_state.query_history)):
        if st.button(f"↩️ {q}", key=f"history-btn-{i}"):
            st.write(f"🧪 _Re-running:_ **{q}**")
            run_mock_query(q)


# --- Side panel ---
st.sidebar.markdown("## UFO Lab")
run_custom, date_range, selected_states, selected_shapes, credibility_range = show_custom_query_panel()
show_insert_form()

if run_custom:
    run_custom_mock_query(date_range, selected_states, selected_shapes, credibility_range)

