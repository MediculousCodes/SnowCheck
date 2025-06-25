"""
download_store_pages.py

Author: Jeremy Johnsonwall
Date: June 24th, 2025

Description:
This script uses Playwright to download HTML pages from the ServiceNow Store.
Each page corresponds to a paginated set of apps listed on the site.
The number of pages to download and the output directory are set via `settings.json`.
"""

import asyncio
import os
import json
from playwright.async_api import async_playwright

# Load settings from configuration file
with open("settings.json", "r") as config_file:
    config = json.load(config_file)

# Maximum number of pages to scrape and directory to save the HTML files
max_pages_raw = config.get("storemax_pages")
try:
    max_pages = int(max_pages_raw)
except (TypeError, ValueError):
    raise ValueError("The 'storemax_pages' setting must be a valid integer.")

output_dir = config.get("html_output_dir")

async def download_all_pages():
    """
    Downloads multiple pages from the ServiceNow Store and saves the
    fully rendered HTML content to the specified output directory.
    """
    # Create output directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    # Launch Playwright browser and page
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Loop through all configured page numbers
        for pg in range(1, max_pages):
            url = f"https://store.servicenow.com/store/apps?pg={pg}"
            filename = os.path.join(output_dir, f"pg{pg}.html")
            print(f"Loading page {pg}: {url}")

            # Navigate to page and get HTML content
            await page.goto(url)
            content = await page.content()

            # Save content to file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Saved page {pg} to {filename}")

        await browser.close()
        print("Finished downloading all pages.")

# Run the asynchronous download function
asyncio.run(download_all_pages())
