"""This module contains functions to scrape web pages."""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec


#   MANIPULACE A PRACE S ODKAZEM
def start_session(base_url):
    """
    Start a new WebDriver session using Chrome.

    :param: base_url (str): The base URL of the web page.
    :return: WebDriver: An instance of WebDriver
           for interacting with the browser session.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(base_url)
    driver.maximize_window()
    return driver


#   FUNKCE URCENA PRO CEKANI NA PLNE NACTENI STRANKY
def wait_for_element(driver, by, value, timeout=10):
    """
    Wait for an element to become clickable on the web page.

    Args:
        driver (WebDriver): instance used to interact with the web page.
        by (str): The mechanism to locate the element.
        value (str): The value of the element locator.
        timeout (int): The maximum time in seconds to wait.
    Returns:
        WebElement or None: WebElement object if the element becomes clickable.
        None if the timeout is reached.
    Raises:
        None.
    """
    try:
        wait = WebDriverWait(driver, timeout)
        return wait.until(ec.element_to_be_clickable((by, value)))
    except TimeoutException:
        print(f"Timed out waiting for element {value} to be clickable.")
        return None


#   ZISKANI LOKALITU BYTU
def product_title(item):
    """
    Get the title of the product from the span.

    :param item: HTML element containing the product title.
    :return: title of the product as the string.
    """
    span_title = item.find("span", class_="PropertyCard_"
                                          "propertyCardAddress__hNqyR "
                                          "text-subheadline text-truncate")
    return span_title.text


#   ZISKANI CENY
def extract_price(item):
    """
    Get the price of the product from the span.

    :param item: HTML element containing the product price.
    :return: product price as text.
    """
    span_price = item.find("span", class_="PropertyPrice_property"
                                          "PriceAmount__WdEE1")
    return span_price.text


#   ZISKANI ODKAZU NA KONKRETNI BYT
def product_url(item):
    """
    Get the URL from the HTML element containing the product url.

    :param item: HTML element containing the product URL.
    :return: The URL of the product as a string.
    """
    product = item.find("article", class_="PropertyCard_propertyCard_"
                                          "_moO_5 propertyCard"
                                          " PropertyCard_propertyCard-"
                                          "-landscape__XvPmC")
    header = product.find("h2").find("a")
    url = header.get("href")
    return url

#   -------------   ZISKANI VELIKOSTI BYTU   -------------


def find_flat_size(item):
    """
    Find the size of the flat.

    :param item: HTML element containing the flat information.
    :return: size of the flat as string.
    """
    size = item.find("ul", class_="FeaturesList_featuresList"
                                  "__75Wet featuresList mt-3")
    return size.text


#   FUNKCE PRO ZISKANI VSECH UZITECNYCH DAT TYKAJICI SE BYTU
def find_items(soup):
    """
    Find all items in the HTML element.

    Args:
        soup: object containing the HTML content of the page.
    Returns:
        list: information abot the item.
              Each dictionary has the following keys:
                - 'title': The title of the item.
                - 'link': The URL link of the item.
                - 'price': The price of the item.
    """
    items_data = []
    items = soup.find_all("div", class_="box mb-last-0")
    for item in items:
        item_data = {}
        title = product_title(item)
        price = extract_price(item)
        link = product_url(item)
        flat_size = find_flat_size(item)
        item_data['title'] = title
        item_data["link"] = link
        item_data["price"] = price
        item_data["size"] = flat_size
        items_data.append(item_data)
    return items_data
