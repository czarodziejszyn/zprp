#!/usr/bin/env python3
# otodom_selenium_chrome.py
# Python 3.8+
# wymaga: pip install selenium pandas

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------
# Ustawienia
# ----------------------------
URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"
DELAY = 1       # seconds
MAX_PAGES = 1
OUTPUT_CSV = "otodom_warszawa.csv"
OUTPUT_JSON = "otodom_warszawa.json"

# ----------------------------
# ŚCIEŻKA DO CHROMEDRIVER
# ----------------------------
CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"
CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ----------------------------
# Konfiguracja Chrome
# ----------------------------
# CONFIG
options = Options()
options.binary_location = CHROME_BINARY_PATH
# options.add_argument("--headless=new") # na produkcji bedzie potrzbene to + anti detection. 
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--lang=pl-PL")

# opens chrome directed by python
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# ----------------------------
# Pobieranie ofert
# ----------------------------
all_offers = []

# for pages
for page in range(1, MAX_PAGES + 1):
    page_url = f"{URL}?page={page}"     # link do kolejnych pages
    print(f"[+] Pobieram stronę {page}: {page_url}")
    driver.get(page_url)


    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Akceptuj')]"))
        ).click()
    except:
        pass




    try:
        # wait 15 seconds for frist <article>
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except:
        print("  -> Brak ogłoszeń – koniec.")
        break

    # Scroll
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 1200);")  # js needs to load the offers
        time.sleep(DELAY)

    offers = driver.find_elements(By.TAG_NAME, "article")   # gets all offers from the page

    if not offers:
        print("  -> Brak ofert na stronie, koniec.")
        break

    # DEBUG: zapisz HTML pierwszego ogłoszenia do pliku
    debug_html = offers[0].get_attribute("outerHTML")

    with open("offer_debug.html", "w", encoding="utf-8") as f:
        f.write(debug_html)

    print("[OK] Zapisano HTML do pliku offer_debug.html")




    for offer in offers:
        try:
            full_text = offer.text

            # ----------------------------
            # URL + TITLE
            # ----------------------------
            try:
                link = offer.find_element(By.XPATH, ".//a[contains(@href,'/oferta/')]")
                url = link.get_attribute("href")
                title = url.split("/")[-1].replace("-", " ")
            except:
                url = None
                title = ""

            # ----------------------------
            # PRICE – wyciągamy z tekstu
            # ----------------------------

            try:
                price = offer.find_element(By.XPATH, ".//span[contains(text(),'zł')]").text
                price = price.replace(" ", "").replace("zł", "")
                price = int(price)
            except:
                price = None



            # ----------------------------
            # AREA – też z tekstu
            # ----------------------------
            try:
                area_match = re.search(r"(\d+[,\.]?\d*)\s*m²", full_text)
                if area_match:
                    area = float(area_match.group(1).replace(",", "."))
                else:
                    area = None
            except:
                area = None

            # ----------------------------
            # ADDRESS – pierwsza sensowna linia
            # ----------------------------
            try:
                lines = full_text.split("\n")
                address = lines[-1]
                if "m²" in address or "zł" in address:
                    address = ""
            except:
                address = ""

            # ----------------------------
            # PRICE / M2
            # ----------------------------
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
            print("  ! Błąd jednej oferty:", e)

driver.quit()

# ----------------------------
# Zapis do CSV
# ----------------------------
df = pd.DataFrame(all_offers)
# df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
# print(f"[OK] Zapisano {len(all_offers)} rekordów do {OUTPUT_CSV}")

df.to_json(OUTPUT_JSON, orient="records", force_ascii=False, indent=2)
print(f"[OK] Zapisano {len(all_offers)} rekordów do {OUTPUT_JSON}")

