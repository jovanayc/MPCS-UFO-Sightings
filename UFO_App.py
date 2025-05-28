import streamlit as st
# from mock_queries import run_mock_query, run_custom_mock_query
from preset_query_runner import run_preset_query
from preset_queries_list import PRESET_QUERIES

# for pre-set and template query imports
dynamic_templates = [t["name"] for t in st.session_state.get("saved_templates", [])]
all_queries = PRESET_QUERIES + dynamic_templates

st.set_page_config(page_title="UFO Sightings Explorer", layout="wide")

# --- Initialize session state ---
if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "last_query" not in st.session_state:
    st.session_state.last_query = None


if "confirm_delete_index" not in st.session_state:
    st.session_state.confirm_delete_index = None

st.title("🛸 UFO Sightings Explorer")

st.markdown("👽 Welcome, Earthling.")
st.markdown("""
    > You’ve stumbled upon a portal into the unknown.
    > Here lie over 70,000 reported encounters, eerie lights, and glimpses from the sky.
    > 🛸 Learn at your own risk. Filter sightings. Decode patterns. Add your own encounter. Be-boop.
""")

# --- Layout for numeric query input ---
col1, col2 = st.columns([4, 1])
query_number = col1.number_input(
    label="Enter query number (1 - {})".format(len(all_queries)),
    min_value=1,
    max_value=len(all_queries),
    step=1,
    format="%d",
    label_visibility="collapsed"
)   

# -- Run Query button press
run_query = col2.button("Run Query", key="run_query_center")

# -- Advanced Search
st.markdown("[⚙️ Advanced Search](./Build_Custom_Query)", unsafe_allow_html=True)

# -- On run query button press
if run_query:
    selected_query = all_queries[query_number - 1]
    st.session_state.last_query = selected_query
    st.session_state.query_history.append(selected_query)
    st.session_state.show_results = True

# --- Side panel ---
st.sidebar.markdown("## Pre-Templated Queries")

# Static pre-built queries
for i, query in enumerate(PRESET_QUERIES, 1):
    if st.sidebar.button(f"# {i}) {query}", key=f"preset-{i}"):
        st.session_state.last_query = query
        st.session_state.query_history.append(query)
        st.session_state.show_results = True

# Divider between sections
st.sidebar.markdown("---")
st.sidebar.markdown("## 🧩 Custom Queries")

# For Custom Queries Section
if "saved_templates" in st.session_state and st.session_state.saved_templates:
    for j, template in enumerate(st.session_state.saved_templates):
        name = template["name"]
        index = len(PRESET_QUERIES) + j + 1
        key_suffix = f"{j}-{name.replace(' ', '_')}"

        cols = st.sidebar.columns([6, 1])

        # Query button
        if cols[0].button(f"# {index}) {name}", key=f"template-btn-{key_suffix}"):
            st.session_state.last_query = name
            st.session_state.query_history.append(name)
            st.session_state.show_results = True

        # ❌ Delete button
        if cols[1].button("❌", key=f"delete-initiate-{key_suffix}"):
            st.session_state.confirm_delete_index = j

# --- Confirm Delete Modal ---
if st.session_state.get("confirm_delete_index") is not None:
    j = st.session_state.confirm_delete_index
    name = st.session_state.saved_templates[j]["name"]

    with st.sidebar:
        st.markdown("---")
        st.warning(f"⚠️ Are you sure you want to delete: **'{name}'**?")
        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button("✅ Yes", key="confirm-delete-main"):
                st.session_state.saved_templates.pop(j)
                st.session_state.confirm_delete_index = None
                st.success(f"Deleted '{name}'")
                st.rerun()

        with cancel_col:
            if st.button("❌ No", key="cancel-delete-main"):
                st.session_state.confirm_delete_index = None


# --- Display results section ---
if st.session_state.get("last_query") and st.session_state.get("show_results"):
    run_preset_query(st.session_state.last_query)
