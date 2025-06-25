"""
extract_apps.py

Author: Jeremy Johnsonwall
Date: June 24th, 2025

Description:
This script parses locally saved HTML pages from the ServiceNow Store and extracts 
application listing information. It reads the folder and output file settings from 
a configuration file (`settings.json`) and saves the extracted data as JSON.
"""

import re
import os
import json
import demjson3
from bs4 import BeautifulSoup

# Load configuration values from settings.json
with open("settings.json", "r") as config_file:
    config = json.load(config_file)

# Output JSON file and input HTML folder
apps_output_file = config.get("app_data_file")
input_dir = os.path.abspath(config.get("html_output_dir"))

def extract_apps_from_html(file_path):
    """
    Extracts the 'apps' listings JSON from a single HTML file.

    Args:
        file_path (str): Path to the HTML file.

    Returns:
        list: A list of app dictionaries extracted from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Look for <script type="module"> blocks that contain component.pageData
    script_tags = soup.find_all('script', {'type': 'module'})
    for script in script_tags:
        if 'component.pageData =' in script.text:
            match = re.search(r'component\.pageData\s*=\s*(\{.*?\});', script.text, re.DOTALL)
            if match:
                try:
                    json_text = match.group(1)
                    page_data = demjson3.decode(json_text)
                    return page_data.get("apps", {}).get("listings", [])
                except Exception as e:
                    print(f"Failed to parse JSON in {file_path}: {e}")
    return []

def extract_all_apps_from_folder(folder_path):
    """
    Extracts all apps from all HTML files in the given folder.

    Args:
        folder_path (str): Path to the folder containing HTML files.

    Returns:
        list: Combined list of all extracted apps.
    """
    all_apps = []
    folder_path = os.path.normpath(folder_path)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".html"):
            full_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}")
            apps = extract_apps_from_html(full_path)
            all_apps.extend(apps)
    return all_apps

def save_apps_to_json(apps, output_file):
    """
    Saves the extracted apps list to a JSON file.

    Args:
        apps (list): List of app dictionaries.
        output_file (str): Path to the output JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(apps)} apps and saved to '{output_file}'")

if __name__ == "__main__":
    # Validate the input directory
    if not os.path.isdir(input_dir):
        print(f"Folder not found: '{input_dir}'")
    else:
        apps = extract_all_apps_from_folder(input_dir)
        save_apps_to_json(apps, apps_output_file)
