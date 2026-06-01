import math
import requests
import time


base_url = "https://jiji.ng/api_web/v1/listing?slug=houses-apartments-for-rent&region_slug=abuja&page={}&webp=false"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-listing-id": "rXNmWcRi3xid4ySD",  #gotten from jiji.ng , may change over time
     "x-page-rid": "a03876f1cd6b029e-AMS-aef272e1f93" #gotten from jiji.ng , may change over time
}
first_page_url = base_url.format(1)
response = requests.get(first_page_url, headers=headers)
data = response.json()

total_listings = data.get('adverts_list', {}).get('count', 0)
listings_per_page = len(data.get('adverts_list', {}).get('adverts', []))

if total_listings > 0 and listings_per_page > 0:
    max_pages = math.ceil(total_listings / listings_per_page)
    print(f"Total Listings: {total_listings}")
    print(f"Items per Page: {listings_per_page}")
    print(f"Total Pages to scrape: {max_pages}")
else:
    max_pages = 1
    print("Could not determine page range, defaulting to 1.")
