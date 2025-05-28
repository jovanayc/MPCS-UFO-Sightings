# Pulls query titles from columns in Sightings, UFO, and Location tables
# Within the UFO database in mysql

import streamlit as st
from datetime import date
from constants import UFO_SHAPES, UFO_COLORS, STATE_LIST
from database.insert_sighting import insert_new_sighting

st.title("Build Your Own UFO Query")

st.markdown("Use any combination of filters to find UFO sightings. All filters are optional.")

# # for prefilled filters if called
# prefill = st.session_state.get("prefill_filters", {})

# # Filters
# date_range = st.date_input("Occurred Between", value=(date(1940, 5, 28), date.today()))
# selected_states = st.multiselect("State(s)", STATE_LIST)
# selected_shapes = st.multiselect("UFO Shape(s)", UFO_SHAPES)
# selected_colors = st.multiselect("UFO Color(s)", UFO_COLORS)
# multiple_crafts = st.selectbox("Were there multiple crafts?", ["Any", "Yes", "No"])
# summary_keywords = st.text_input("Search keyword in summary (use commas to seperate words)", placeholder="e.g. lights, triangle, military")

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
    st.success("✅ Custom query would be executed with the following filters:")
    st.json(filters)

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

# Cleanup prefilled data
st.session_state.pop("prefill_filters", None)
st.session_state.pop("editing_existing_query", None)