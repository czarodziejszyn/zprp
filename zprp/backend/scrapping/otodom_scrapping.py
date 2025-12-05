import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"

MAX_PAGES = 1
OUTPUT_JSON = "otodom_warszawa.json"


# CHROME PATHS 
CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"
CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


# Chrome config
options = Options()
options.binary_location = CHROME_BINARY_PATH
# options.add_argument("--headless=new")    # TODO: add headless + antidetection
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--lang=pl-PL")


# Open Chrome directed by python
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


# Get offers 
all_offers = []
seen_ids = set()
for page in range(1, MAX_PAGES + 1):
    page_url = f"{URL}?page={page}"
    print(f"[+] Downloading page {page}: {page_url}")
    driver.get(page_url)

    # Accept cookies
    try:
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Akceptuj')]"))
        ).click()
    except:
        pass


    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except:
        print("  -> No offers found – end.")
        break


    # Find offers
    offers = driver.find_elements(By.TAG_NAME, "article")
    if not offers:
        print("  -> No offers found – end.")
        break


    for offer in offers:
        try:
            full_text = offer.text

            # Get url 
            try:
                link = offer.find_element(By.XPATH, ".//a[contains(@href,'/oferta/')]")
                url = link.get_attribute("href")
                offer_id = url.split("-")[-1]
            except Exception as e:
                print("Exception in the offer - url not found:", e)

            # Skip duplicates
            if offer_id in seen_ids:
                continue
            seen_ids.add(offer_id)

            # Get title
            try:
                title = url.split("/")[-1].replace("-", " ")
            except:
                title = ""


            # Get price
            try:
                price_text = offer.find_element(
                    By.XPATH, ".//span[@data-sentry-element='MainPrice']"
                ).text

                price = int(
                    price_text
                    .replace("zł", "")
                    .replace("\xa0", "")
                    .replace(" ", "")
                )

            except:
                price = None


            # Get area
            try:
                area_match = re.search(r"(\d+[,\.]?\d*)\s*m²", full_text)
                if area_match:
                    area = float(area_match.group(1).replace(",", "."))
                else:
                    area = None
            except:
                area = None


            # Get address
            try:
                address = offer.find_element(
                    By.XPATH, ".//p[@data-sentry-component='Address']"
                ).text
            except:
                address = ""


            # Skipping ads / investemnts offers
            if price is None or area is None:
                continue

            # Get price / m2
            price_m2 = round(price / area, 2) if price and area else None

            all_offers.append({
                "title": title,
                "url": url,
                "price": price,
                "area_m2": area,
                "price_per_m2": price_m2,
                "address": address
            })

        except Exception as e:
            print("Exception in the offer:", e)

driver.quit()



# Write to .json file
df = pd.DataFrame(all_offers)
df.to_json(OUTPUT_JSON, orient="records", force_ascii=False, indent=2)
print(f"[OK] Written {len(all_offers)} records to {OUTPUT_JSON}")

