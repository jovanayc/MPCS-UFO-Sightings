# preset_queries_filters.py
# for pre-filling the Build Custom Query form and editting preset queries.

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

    "Sightings by Season in USA": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Article Mentions in Famous UFO Locations": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "Roswell, Phoenix, North Bergen",
        "duration": ""
    },

    "Average UFO Speed Per Year": None,  # Not filter-based; aggregates all with Speed

    "Most Witnessed Sightings": {
        "date_range": ["1940-01-01", "2025-12-31"],
        "states": [],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Top 100 Shapes by Country": {
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

    "Illinois Sightings in Summer": {
        "date_range": ["1940-06-01", "2025-08-31"],
        "states": ["IL"],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "",
        "duration": ""
    },

    "Recent Chicago Sightings": {
        "date_range": ["2021-01-01", "2025-12-31"],
        "states": ["IL"],
        "shapes": [],
        "colors": [],
        "multiple_crafts": "Any",
        "summary_keywords": "Chicago",
        "duration": ""
    }
} 
