import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "raw_listings_npc.csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)

base_url = "https://nigeriapropertycentre.com/for-rent/abuja?page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

all_listings = []

for page in range(1, 237):
    print(page)
    url = base_url + str(page)

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print(f"page {page} failed, status: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select(".wp-block-body")

    if not listings:
        print("No listings found")
        break

    for house in listings:
        try:
            prop_type = house.select(".content-title")
            property_type = prop_type[0].text.strip() if prop_type else "N/A"

            # the site splits currency and amount into two separate elements
            init_price = house.select(".price")
            if len(init_price) >= 2:
                price = init_price[0].text + init_price[1].text
            else:
                price = "N/A"

            address = house.select(".voffset-bottom-10")
            location = address[0].text.strip() if address else "N/A"

            all_listings.append({
                "Property Type": property_type,
                "Price (Per Annum)": price,
                "Location": location
            })

        except Exception as e:
            print(f"Skipped a listing on page {page}: {e}")

    # save every 10 pages in case the script crashes midway
    if page % 10 == 0:
        pd.DataFrame(all_listings).to_csv(OUTPUT_FILE, index=False)
        print(f"saved on page {page}")

    time.sleep(random.uniform(3, 7))


pd.DataFrame(all_listings).to_csv(OUTPUT_FILE, index=False)
print(f"{len(all_listings)} rental listings collected.")