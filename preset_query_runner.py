# preset_query_runner.py

import streamlit as st
import pandas as pd
from database.db_utils import get_connection
from preset_queries_filters import PRESET_FILTERS
from preset_queries_list import PRESET_SQL_QUERIES

# Mapping of preset query names to their actual SQL
PRESET_QUERIES = list(PRESET_SQL_QUERIES.keys())

def run_preset_query(query_title):
    st.markdown("## 📊 Results")
    st.markdown(
        f"<div style='font-size: 0.85rem; color: gray;'>Results for query: <i>{query_title}</i></div>",
        unsafe_allow_html=True
    )

    query = PRESET_SQL_QUERIES.get(query_title)

    if not query:
        st.error("Unknown query title.")
        return

    # Load associated filters for this query
    filters = PRESET_FILTERS.get(query_title)
    if filters:
        st.session_state.prefill_filters = filters

    # Run the actual query
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results)

    # Display results
    st.dataframe(df, use_container_width=True)

    # Show edit button
    st.markdown("### ✏️ Edit Query")
    if st.button("Edit Query", key="edit-query-button"):
        st.session_state.editing_existing_query = query_title
        st.switch_page("pages/Build_Custom_Query.py")

    cursor.close()
    conn.close()
