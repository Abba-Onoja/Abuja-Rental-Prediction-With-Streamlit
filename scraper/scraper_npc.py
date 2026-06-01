import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "npc_abuja_rentals.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='npc_scraper_activity.log'
)

base_url = "https://nigeriapropertycentre.com/for-rent/abuja?page={}"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.5",
}

npc_abuja_rentals = []

for page in range(1, 100): 
    print(f"scraping page {page}")
    url = base_url.format(page)

    try:
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code == 429:
            logging.warning(f"rate limited on page {page}")
            print(f"rate limited on page {page}")
            time.sleep(60)
            continue
            
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select(".wp-block-body")

        if not listings:
            print(f"no listings found on page {page}.")
            break

        for house in listings:
            try:
                
                prop_type = house.select(".content-title")
                prop_category = prop_type[0].text.strip() if prop_type else "N/A"

                init_price = house.select(".price")
                if len(init_price) >= 2:
                    price = init_price[0].text + init_price[1].text
                else:
                    price = "N/A"

                address = house.select(".voffset-bottom-10")
                location = address[0].text.strip()



                npc_abuja_rentals.append({
                    "Property Category": prop_category,
                    "Price (Per Annum)": price,
                    "Location": location,
                    "Scraped_At": time.strftime("%Y-%m-%d %H:%M:%S")
                })

            except AttributeError:
                continue

    except requests.exceptions.RequestException as e:
        logging.error(f"network error on page {page}: {e}")
        time.sleep(10)
        continue
    except Exception as e:
        logging.error(f"error on page {page}: {e}")
        break
     #checkpoint, saves every ten pages
    if page % 10 == 0:
        pd.DataFrame(npc_abuja_rentals).to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Checkpoint saved: {len(npc_abuja_rentals)} rows at page {page}")

    time.sleep(random.uniform(3.5, 7.2))

if npc_abuja_rentals:
    df = pd.DataFrame(npc_abuja_rentals)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"saved {len(df)} listings to {OUTPUT_FILE}")