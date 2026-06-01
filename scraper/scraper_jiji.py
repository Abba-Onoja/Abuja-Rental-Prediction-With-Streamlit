import requests
import time
import random
import pandas as pd
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)


OUTPUT_FILE = DATA_DIR / "jiji_abuja_rentals.csv"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='scraper_activity.log'
)
base_url = "https://jiji.ng/api_web/v1/listing?slug=houses-apartments-for-rent&region_slug=abuja&page={}&webp=false"


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-listing-id": "rXNmWcRi3xid4ySD",  #gotten from jiji.ng , may change over time
     "x-page-rid": "a03876f1cd6b029e-AMS-aef272e1f93" #gotten from jiji.ng , may change over time
}

jiji_abuja_rentals = []

for page in range(1, 205): #check jiji.py for how num of pages was gotten
    print(f"scraping page {page}") 
    url = base_url.format(page)
    
    try:
        #longer timeout for jiji's api which is slow
        response = requests.get(url, headers=headers, timeout=20)
        
        
        if response.status_code == 429:
            logging.warning(f"rate limited on page {page}")
            print(f"rate limited on page {page}")
            time.sleep(60)
            continue
            
        response.raise_for_status() # Trigger error on 4xx/5xx
        
        data = response.json()
        adverts = data.get('adverts_list', {}).get('adverts', [])
        
      
        if not adverts:
            print(f"no more listings found at page {page}.")
            break
            
        for ad in adverts:
            
            price = ad.get('price_obj', {}).get('value')
            price_currency = ad.get('price_obj', {}).get('view')
            district = ad.get('region_name') 
            prop_category = ad.get('title')
            
            
            attributes = ad.get('attrs', [])
            bedrooms_val, bedrooms_cat = None, None

            for attr in attributes:
                if attr.get('name') == 'Bedrooms':
                    bedrooms_val = attr.get('value')          
                    bedrooms_cat = attr.get('semantic_value') 
            
            jiji_abuja_rentals.append({
                "Bedrooms": bedrooms_val,
                "Bedrooms(category)": bedrooms_cat,
                "Property Category": prop_category,
                "Price": price,
                "Price(with currency)": price_currency,
                "District": district,
                "Scraped_At": time.strftime("%Y-%m-%d %H:%M:%S") # 
            })
            
    except requests.exceptions.RequestException as e:
        
        logging.error(f"network error on page {page}: {e}")
        time.sleep(10) 
        continue
    except Exception as e:
        logging.error(f"error on page {page}: {e}")
        break
    
    if page % 10 == 0:
        pd.DataFrame(jiji_abuja_rentals).to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Checkpoint saved: {len(jiji_abuja_rentals)} rows at page {page}")

    time.sleep(random.uniform(3.5, 7.2)) 


if jiji_abuja_rentals:
    df = pd.DataFrame(jiji_abuja_rentals)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"saved {len(df)} listings to {OUTPUT_FILE}")
