import re
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


OTODOM_URL = os.getenv("OTODOM_URL")
CHROME_BINARY_PATH = os.getenv("CHROME_BINARY_PATH")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

logger = logging.getLogger(__name__)


def scrap_offers(max_offer_pages):
    # Chrome config
    options = Options()
    options.binary_location = CHROME_BINARY_PATH

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pl-PL")

    # options for docker
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Open Chrome directed by python
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)


    # Get offers 
    all_offers = []
    seen_ids = set()
    for page in range(1, max_offer_pages + 1):
        page_url = f"{OTODOM_URL}?page={page}"
        logger.info(f"[+] Downloading page {page}: {page_url}")
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
            logger.info("  -> No offers found – end.")
            break


        # Find offers
        offers = driver.find_elements(By.TAG_NAME, "article")
        if not offers:
            logger.info("  -> No offers found – end.")
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
                    logger.exception("Skipping offer - url not found")
                    continue

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

                # Skipping incorrect address:
                if address is None:
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
                logger.exception("Exception in the offer:", e)

    driver.quit()
    return all_offers


def write_offers_to_json(offers, file_path):
    df = pd.DataFrame(offers)
    df.to_json(file_path, orient="records", force_ascii=False, indent=2)
    logger.info(f"[OK] Written {len(offers)} records to {file_path}")

    


