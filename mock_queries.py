# #mock_queries.py
# import pandas as pd
# import streamlit as st
# from database.db_utils import get_connection


# mock_data = pd.DataFrame([
#     {"Date": "2023-03-21", "City": "Roswell", "State": "NM", "Shape": "Disc", "Duration": "5 min", "Credibility": 8.9},
#     {"Date": "2023-04-12", "City": "Phoenix", "State": "AZ", "Shape": "Triangle", "Duration": "10 min", "Credibility": 7.5},
#     {"Date": "2023-05-07", "City": "Groom Lake", "State": "NV", "Shape": "Light", "Duration": "2 min", "Credibility": 9.2},
#     {"Date": "2023-06-01", "City": "Phoenix", "State": "AZ", "Shape": "Fireball", "Duration": "7 min", "Credibility": 6.8},
# ])

# def run_mock_query(query_choice):
#     st.markdown("## 📊 Results")
#     # List what query was ran
#     st.markdown(
#     f"<div style='font-size: 0.85rem; color: gray;'>Results for query: <i>{st.session_state.last_query}</i></div>",
#     unsafe_allow_html=True
# )


#     if query_choice == "Sighting by top UFO location in the past 10 years":
#         # Pretend we pulled a top location (e.g., Phoenix)
#         result = (
#             mock_data[mock_data["City"] == "Phoenix"]
#             .sort_values(by="Date", ascending=False)
#         )

#     elif query_choice == "Sightings from 1990 - 1999 in Phoenix Arizona":
#         # No real 1990s data, but mock it anyway
#         result = pd.DataFrame([
#             {"Date": "1995-06-10", "City": "Phoenix", "State": "AZ", "Shape": "Disc", "Duration": "8 min", "Credibility": 7.8},
#             {"Date": "1997-03-13", "City": "Phoenix", "State": "AZ", "Shape": "Triangle", "Duration": "15 min", "Credibility": 9.1},
#         ])

#     else:
#         # Default: show all
#         result = mock_data
    
#     st.dataframe(result, use_container_width=True)


# def run_custom_mock_query(date_range, selected_states, selected_shapes, credibility_range):
#     st.markdown("## 📊 Custom Query Results")

#     # Return a single hardcoded row
#     mock_row = pd.DataFrame([{
#         "Date": "2024-10-01",
#         "City": "Los Alamos",
#         "State": "NM",
#         "Shape": "Disc",
#         "Duration": "6 min",
#         "Credibility": 8.3,
#         "Notes": "Witness reported hovering object with blue glow."
#     }])

#     st.dataframe(mock_row, use_container_width=True)

