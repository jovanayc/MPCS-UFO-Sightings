# Pulls query titles from columns in Sightings, UFO, and Location tables
# Within the UFO database in mysql

import sys, os
import streamlit as st
from datetime import date
from constants import UFO_SHAPES, UFO_COLORS, STATE_LIST
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.insert_sighting import insert_new_sighting
from utils.db_utils import get_connection

st.title("Build Your Own UFO Query")

st.markdown("Use any combination of filters to find UFO sightings. All filters are optional.")

# for prefilled filters if called
prefill = st.session_state.get("prefill_filters", {})

# Filters with prefill logic
date_range = st.date_input(
    "Occurred Between",
    value=prefill.get("date_range", (date(1940, 5, 28), date.today()))
)

selected_states = st.multiselect(
    "State(s)",
    STATE_LIST,
    default=prefill.get("states", [])
)

selected_shapes = st.multiselect(
    "UFO Shape(s)",
    UFO_SHAPES,
    default=prefill.get("shapes", [])
)

selected_colors = st.multiselect(
    "UFO Color(s)",
    UFO_COLORS,
    default=prefill.get("colors", [])
)

multiple_crafts = st.selectbox(
    "Were there multiple crafts?",
    ["Any", "Yes", "No"],
    index=["Any", "Yes", "No"].index(prefill.get("multiple_crafts", "Any"))
)

summary_keywords = st.text_input(
    "Search keyword in summary (use commas to separate words)",
    value=prefill.get("summary_keywords", ""),
    placeholder="e.g. lights, triangle, military"
)

# Run Custom Query Button
if st.button("Run Custom Query"):
    filters = {
        "date_range": [str(d) for d in date_range],
        "states": selected_states,
        "shapes": selected_shapes,
        "colors": selected_colors,
        "multiple_crafts": multiple_crafts,
        "summary_keywords": summary_keywords,
    }
    st.success("✅ Custom query executed")

    # To trigger results from custom query run
    st.session_state.prefill_filters = filters
    st.session_state.last_query = "Custom Query"
    st.session_state.show_results = True

    st.success("✅ Custom query executed")

# --- Save as Template ---
st.markdown("---")
st.subheader("Save This Query as a New Template")
query_name = st.text_input("Give this query a name:")

if st.button("Save Query"):
    if query_name:
        new_template = {
            "name": query_name,
            "filters": {
                "date_range": [str(d) for d in date_range],
                "states": selected_states,
                "shapes": selected_shapes,
                "colors": selected_colors,
                "multiple_crafts": multiple_crafts,
                "summary_keywords": summary_keywords,
            }
        }
        if "saved_templates" not in st.session_state:
            st.session_state.saved_templates = []
        st.session_state.saved_templates.append(new_template)
        st.success(f"Saved '{query_name}' as a new template!")
    else:
        st.warning("Please enter a name before saving.")

# # Cleanup prefilled data
# st.session_state.pop("prefill_filters", None)
# st.session_state.pop("editing_existing_query", None)

# Run results after query form is submitted
if st.session_state.get("last_query") == "Custom Query" and st.session_state.get("show_results"):
    from preset_query_runner import run_custom_query
    st.markdown("## 📊 Results for Custom Query")
    run_custom_query(st.session_state.get("prefill_filters"))