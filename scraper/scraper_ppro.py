import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = DATA_DIR / "raw_listings_ppro.csv"

base_url = "https://propertypro.ng/property-for-rent/in/abuja?page=1"


all_listings = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for page in range(1, 99):
    print(page)
    url = base_url + str(page)

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select(".property-listing")

    if not listings:
        break

    for house in listings:
        try:
            property_type = house.find('div', class_ = 'pl-title').find_all('a')[0].text.strip()
            price = house.find('div', class_ = 'pl-price').find('h3').text.strip()
            location = house.find('div', class_ = 'pl-title').find("p").text.strip()

            all_listings.append({
                "Property Type": property_type,
                "Price (Per Annum)": price,
                "Location": location
            })

        except Exception:
            continue

    if page % 10 == 0:
        pd.DataFrame(all_listings).to_csv(OUTPUT_FILE, index=False)

    time.sleep(random.uniform(3, 7))


pd.DataFrame(all_listings).to_csv(OUTPUT_FILE, index=False)
