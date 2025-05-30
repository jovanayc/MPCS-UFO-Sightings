# sidebar.py
import streamlit as st
from preset_queries_filters import PRESET_FILTERS
from preset_queries_list import PRESET_QUERIES
from constants import UFO_SHAPES, UFO_COLORS, STATE_LIST
from datetime import date

def show_sidebar_queries():
    st.sidebar.markdown("## Pre-Templated Queries")

    for i, query_title in enumerate(PRESET_QUERIES, 1):
        with st.sidebar.expander(f"#{i}) {query_title}"):
            filters = PRESET_FILTERS.get(query_title) or {}

            date_range = st.date_input("Occurred Between", value=filters.get("date_range", [date(1940, 5, 28), date.today()]), key=f"date-{i}")
            # Load states and handle "All" if present
            selected_states = filters.get("states", [])
            if "All" in selected_states:
                selected_states = []
            selected_shapes = st.multiselect("UFO Shape(s)", UFO_SHAPES, default=filters.get("shapes", []), key=f"shape-{i}")
            selected_colors = st.multiselect("UFO Color(s)", UFO_COLORS, default=filters.get("colors", []), key=f"color-{i}")
            multiple_crafts = st.selectbox("Multiple Crafts?", ["Any", "Yes", "No"], index=["Any", "Yes", "No"].index(filters.get("multiple_crafts", "Any")), key=f"multi-{i}")
            summary_keywords = st.text_input("Summary Keywords", value=filters.get("summary_keywords", ""), key=f"keywords-{i}")

            if st.button(f"▶️ Run {query_title}", key=f"run-query-{i}"):
                st.session_state.prefill_filters = {
                    "date_range": [str(d) for d in date_range],
                    "states": selected_states,
                    "shapes": selected_shapes,
                    "colors": selected_colors,
                    "multiple_crafts": multiple_crafts,
                    "summary_keywords": summary_keywords,
                }
                st.session_state.last_query = query_title
                st.session_state.editing_existing_query = query_title
                st.session_state.query_history.append(query_title)
                st.session_state.show_results = True


    # Confirm Delete Modal
    if st.session_state.get("confirm_delete_index") is not None:
        j = st.session_state.confirm_delete_index
        name = st.session_state.saved_templates[j]["name"]
        with st.sidebar:
            st.markdown("---")
            st.warning(f"⚠️ Delete saved query: **'{name}'**?")
            confirm_col, cancel_col = st.columns(2)

            if confirm_col.button("✅ Yes", key="confirm-delete"):
                st.session_state.saved_templates.pop(j)
                st.session_state.confirm_delete_index = None
                st.success(f"Deleted '{name}'")
                st.rerun()

            if cancel_col.button("❌ No", key="cancel-delete"):
                st.session_state.confirm_delete_index = None
