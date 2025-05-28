# preset_queries_filters.py
# for pre-filling the Build Custom Query form and editing preset queries.

PRESET_FILTERS = {
    "Total Sightings Per Year": None,  # Not filter-based; aggregate query

    "UFO Sightings by Country": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Seasonal Sightings in the USA": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": ["ALL"],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Articles Related to Famous Locations": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "Roswell, Phoenix, North Bergen",
        "duration": ""
    },

    "Average Speed by Year": None,  # Not filter-based; aggregates all with Speed

    "Most Witnessed Sightings": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Top 100 UFO Shapes by Country": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Military Base Mentions in Sightings": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "military, base",
        "duration": ""
    },

    "Illinois Summer Sightings": {
        "date_range": ["1940-06-01", "2025-08-31"],
        "states": ["IL"],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Chicago Sightings (Past 5 Years)": {
        "date_range": ["2020-01-01", "2025-12-31"],
        "states": ["IL"],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "Chicago",
        "duration": ""
    }
}