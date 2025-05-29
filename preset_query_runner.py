# preset_query_runner.py

import streamlit as st
import pandas as pd
from utils.db_utils import get_connection
from preset_queries_filters import PRESET_FILTERS
from preset_queries_list import PRESET_SQL_QUERIES

# Mapping of preset query names to their actual SQL
PRESET_QUERIES = list(PRESET_SQL_QUERIES.keys())

# run query in main page
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

    # Load associated filters for this query, if available
    filters = PRESET_FILTERS.get(query_title)
    if filters:
        st.session_state.prefill_filters = filters

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results)

        # Display results
        st.dataframe(df, use_container_width=True)

        # Edit option
        st.markdown("### ✏️ Edit Query")
        if st.button("Edit Query", key="edit-query-button"):
            st.session_state.editing_existing_query = query_title
            st.switch_page("pages/Build_Custom_Query.py")

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Query failed: {e}")

# run query in custom page
def run_custom_query(filters):
    import streamlit as st
    import pandas as pd
    from utils.db_utils import get_connection

    st.markdown("## 📊 Results for Custom Query")
    
    query = """
        SELECT Sightings.*, Location.City, Location.State, Location.Country
        FROM Sightings
        JOIN Location ON Sightings.LocationID = Location.LocationID
        WHERE 1=1
    """
    params = []

    # Add date range
    if filters.get("date_range"):
        query += " AND Occurred BETWEEN %s AND %s"
        params.extend(filters["date_range"])

    # Add states
    if filters.get("states") and "All" not in filters["states"]:
        placeholders = ", ".join(["%s"] * len(filters["states"]))
        query += f" AND Location.State IN ({placeholders})"
        params.extend(filters["states"])

    # Add keyword search
    if filters.get("summary_keywords"):
        keywords = [kw.strip() for kw in filters["summary_keywords"].split(",")]
        if keywords:
            keyword_conditions = " OR ".join(["Summary LIKE %s" for _ in keywords])
            query += f" AND ({keyword_conditions})"
            params.extend([f"%{kw}%" for kw in keywords])

    # Connect and run
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No results found for this query.")

