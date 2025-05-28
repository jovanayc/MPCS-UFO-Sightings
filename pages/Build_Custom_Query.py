import streamlit as st
from datetime import date
from constants import UFO_SHAPES, STATE_LIST

st.set_page_config(page_title="Build Custom Query", layout="centered")
st.title("Build Your Own UFO Query")

st.markdown("Use filters below to create a custom search across UFO sightings.")

# --- Filter Inputs ---
date_range = st.date_input("Date Range", value=(date(2020, 1, 1), date.today()))
selected_states = st.multiselect("State(s)", STATE_LIST)
selected_shapes = st.multiselect("Shape(s)", UFO_SHAPES)
credibility_range = st.slider("Credibility Score Range", 0.0, 10.0, (4.0, 9.0))

# --- Run Query Button ---
if st.button("Run Custom Query"):
    st.success("✅ Custom query would be executed here with selected filters (mock for now).")
    st.write("Filters applied:")
    st.json({
        "date_range": [str(d) for d in date_range],
        "states": selected_states,
        "shapes": selected_shapes,
        "credibility": credibility_range,
    })

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
                "credibility": credibility_range
            }
        }
        if "saved_templates" not in st.session_state:
            st.session_state.saved_templates = []
        st.session_state.saved_templates.append(new_template)
        st.success(f"Saved '{query_name}' as a new template!")
    else:
        st.warning("Please enter a name before saving.")