"""
download_app_detail_pages.py

Author: Jeremy Johnsonwall
Date: June 24th, 2025

Description:
This script uses Playwright to download HTML pages for each app on the ServiceNow Store
based on the list of app IDs in ids.json. Each page is saved as a separate HTML file
in the folder specified by app_detail_dir in settings.json.
"""

import asyncio
import os
import json
from playwright.async_api import async_playwright, Browser
from typing import List

# Load settings
with open("settings.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

output_dir = config.get("app_detail_dir", "app_detail_pages")
os.makedirs(output_dir, exist_ok=True)

# Load app IDs from ids.json
with open("ids.json", "r", encoding="utf-8") as f:
    app_ids = json.load(f)

CONCURRENCY_LIMIT = 10  # Adjust this depending on your system/network

async def fetch_app_page(sem: asyncio.Semaphore, browser: Browser, app_id: str, idx: int, total: int):
    url = f"https://store.servicenow.com/store/app/{app_id}"
    filename = os.path.join(output_dir, f"{app_id}.html")
    print(f"({idx}/{total}) Loading app: {url}")

    async with sem:
        try:
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            content = await page.content()
            await context.close()

            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"({idx}/{total}) Saved to {filename}")
        except Exception as e:
            print(f"({idx}/{total}) Failed to fetch {url}: {e}")


async def download_all_app_pages():
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [
            fetch_app_page(sem, browser, app_id, idx + 1, len(app_ids))
            for idx, app_id in enumerate(app_ids)
        ]

        await asyncio.gather(*tasks)
        await browser.close()
        print("All app pages downloaded.")

if __name__ == "__main__":
    asyncio.run(download_all_app_pages())
