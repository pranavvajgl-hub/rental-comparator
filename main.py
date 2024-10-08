"""This module contains the main program for the program."""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from web_scraper import start_session, wait_for_element, find_items
import pandas as pd

#   STARTING THE WEB-SCRAPING SESSION 'BEZREALITKY.CZ'
driver = start_session(base_url=("https://www.bezrealitky.cz/"
                                 "vyhledat?offerType=PRONAJEM&e"
                                 "stateType=BYT&osm_value="
                                 "Praha%2C+%C4%8Cesko&regionOsmIds="
                                 "R435541&currency=CZK&location=exact"))
url = driver.current_url

#   ACCEPT COOKIES :)
try:
    driver.find_element(By.XPATH, "//button[@id='"
                                  "CybotCookiebotDialog"
                                  "BodyLevelButtonLevel"
                                  "OptinAllowAll']").click()
except Exception as e:
    print(e)
    pass

#   ZJISTENI POCET STRAN
soup = BeautifulSoup(driver.page_source, "html.parser")
last_page_number = None
pages = soup.find_all("a", class_="page-link")
for link in pages:
    # Extrahovani jednotlivych page-link, kde na konci je page=[cislo]
    href = link.get("href")
    #  Zjisteni cisla posledni stranky
    if href and "page=" in href:
        number = href.split("=")[-1]
        if last_page_number is None or int(number) > int(last_page_number):
            last_page_number = number

#   PROHCZENI JEDNOTLIVYCH STRANEK WEBU PRO ZISKAVANI DAT
#   Vytvoreni array pro vycitane data
all_items_data = []
for page in range(1, int(last_page_number) + 1):
    #   Inkrementace stranek
    driver.get(url + "&page=" + str(page))
    try:
        #   Pro uplne nacteni stranky
        wait_for_element(driver, By.CLASS_NAME, "Header_headerLogo__4edC_")
        #   Updatnuti html
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = find_items(soup)
        all_items_data.extend(data)
    except Exception as e:
        #   Ziskani chyby
        print(f"An error occurred on page {page}: {e}")
        pass
#   -------------   ACCEPT COOKIES POKUD STALE EXISTUJE     -------------
    try:
        driver.find_element(By.XPATH, "//button[@id="
                                      "'CybotCookiebotDialogBody"
                                      "LevelButtonLevelOptinAllow"
                                      "All']").click()
    except Exception as e:
        print(e)
        pass

#   -------------   ZFORMATOVANI DAT PRO EXCEL  -------------
    df = pd.DataFrame(all_items_data)
    df.to_excel("./output-scrape.xlsx", index=False)

#   -------------   UKONCENI PROHLIZECE    -------------
driver.quit()
