#!/usr/bin/env python3
# otodom_selenium_firefox_scroll.py
# Python 3.8+
# wymaga: pip install selenium pandas

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------
# Ustawienia
# ----------------------------
URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"
DELAY = 1  # krótkie pauzy po scrollu
MAX_PAGES = 5  # maksymalna liczba stron do pobrania (można zwiększyć)
OUTPUT_CSV = "otodom_warszawa.csv"

# ----------------------------
# Ścieżki
# ----------------------------
GECKODRIVER_PATH = r"C:\Users\julac\Downloads\geckodriver-v0.36.0-win32\geckodriver.exe"
FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# ----------------------------
# Konfiguracja Selenium Firefox
# ----------------------------
options = Options()
options.headless = True
options.binary_location = FIREFOX_PATH
options.add_argument("--lang=pl-PL")

service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

# ----------------------------
# Pobieranie ofert
# ----------------------------
all_offers = []

for page in range(1, MAX_PAGES + 1):
    page_url = f"{URL}?page={page}"
    print(f"[+] Pobieram stronę {page}: {page_url}")
    driver.get(page_url)

    # Czekaj maksymalnie 10 sekund na pojawienie się ogłoszeń
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-cy='listing-item']"))
        )
    except:
        print("  -> Elementy ogłoszeń nie pojawiły się na stronie")
        break

    # Scrollujemy stronę, żeby załadowały się wszystkie oferty
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(3):  # scroll 3 razy
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(DELAY)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Znajdź wszystkie ogłoszenia
    offers = driver.find_elements(By.CSS_SELECTOR, "article[data-cy='listing-item']")
    if not offers:
        print("  -> Brak ofert na stronie, koniec.")
        break

    for offer in offers:
        try:
            title_el = offer.find_element(By.CSS_SELECTOR, "a")
            title = title_el.text.strip()
            url = title_el.get_attribute("href")

            price = offer.find_element(By.CSS_SELECTOR, "p[data-cy='listing-price']").text.strip()
            price = price.replace(" ", "").replace("zł", "")
            price = int(price) if price.isdigit() else None

            area = offer.find_element(By.CSS_SELECTOR, "li[data-cy='listing-area']").text.strip()
            area = area.replace("m²", "").replace(",", ".").strip()
            area = float(area) if area.replace(".", "").isdigit() else None

            price_m2 = round(price / area, 2) if price and area else None

            address = offer.find_element(By.CSS_SELECTOR, "p[data-cy='listing-location']").text.strip()

            all_offers.append({
                "title": title,
                "url": url,
                "price": price,
                "area_m2": area,
                "price_per_m2": price_m2,
                "address": address
            })
        except Exception as e:
            print("  ! Błąd parsowania jednej oferty:", e)
            continue

driver.quit()

# ----------------------------
# Zapis do CSV
# ----------------------------
df = pd.DataFrame(all_offers)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"[OK] Zapisano {len(all_offers)} rekordów do {OUTPUT_CSV}")
