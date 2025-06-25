"""
extract_ids.py

Author: Jeremy Johnsonwall
Date: June 24th, 2025

Description:
Reads app listing data from a JSON file specified in settings.json,
extracts the "id" field from each app, and writes all IDs to ids.json.
"""

import json

# Load settings
with open("settings.json", "r") as config_file:
    config = json.load(config_file)

# Get app data file path
app_data_file = config.get("app_data_file")
print(f"Reading from: {app_data_file}")

# Load app data (expected to be a list of dictionaries)
with open(app_data_file, "r", encoding="utf-8") as f:
    apps = json.load(f)

# Extract IDs
app_ids = [app["id"] for app in apps if "id" in app]

# Save to ids.json
with open("ids.json", "w", encoding="utf-8") as f:
    json.dump(app_ids, f, indent=2)

print(f"Extracted {len(app_ids)} IDs and saved to 'ids.json'")
