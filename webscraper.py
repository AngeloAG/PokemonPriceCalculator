# Author: Angelo Arellano Gaona
# Description:
#   This module has all the helper functions for webscraping. It works using Selenium for browser controlling and BeautifulSoup for html elements manipulation
# Date: 3/30/2023

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

#AAAG_DRIVER_SERVICE = Service(executable_path="/drivers/chromedriver.exe")
AAAG_DRIVER_OPTIONS = Options()
AAAG_DRIVER_OPTIONS.headless = True
AAAG_DRIVER = webdriver.Chrome( options=AAAG_DRIVER_OPTIONS)


def aaag_get_html_until_element_present(aaag_url, aaag_identification_type, aaag_identification_value):
    """Gets the HTML from the specified webpage using selenium waiting until the an element with the classname defined is present on the page
    Args:
      @aaag_url (str): the website url to scrap
      @aaag_identification_type (str): the means of identifiyng the element. valid options are (class, id)
      @aaag_identification_value (str): the classname of the element
    Returns:
      page_html (BeautifulSoup): The parsed HTML of the page
    """
    try:
        AAAG_DRIVER.get(aaag_url)
        # Searches usually do delayed request after page loads, we have to wait for a certain element to appear in the DOM
        if aaag_identification_type == "class":
            WebDriverWait(AAAG_DRIVER, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, aaag_identification_value)))
        elif aaag_identification_type == "id":
            WebDriverWait(AAAG_DRIVER, 6).until(
                EC.presence_of_element_located((By.ID, aaag_identification_value)))
        else:
            raise ValueError("Bad invalid aaag_identification_type")

        aaag_soup = BeautifulSoup(
            AAAG_DRIVER.page_source, features="html.parser")

        return aaag_soup
    except TimeoutException:
        return BeautifulSoup("<html><head><title>Not found<title/></head><body>Took too long to load</body></html>", features="html.parser")
    except WebDriverException:
        return BeautifulSoup("<html><head><title>Not found<title/></head><body>Page not found</body></html>", features="html.parser")


def aaag_get_element_from_soup(aaag_soup, aaag_identification_type, aaag_identification_value):
    """Gets an element from a BeautifulSoup instance by several identification methods
      Args:
        @aaag_soup (BeautifulSoup): the soup in which to find the element
        @aaag_identification_type (str): the mean to identify the element. Valid options are (class, id)
        @aaag_identification_value (str): the value of the identification_type to search in the soup
      Returns:
        The soup element if found, if not returns None
    """
    aaag_element = aaag_soup.find(
        attrs={aaag_identification_type: aaag_identification_value})

    return aaag_element


def aaag_get_element_from_soup_by_element(aaag_soup, aaag_element):
    """Gets first appearance of an element from a BeautifulSoup instance by its type
      Args:
        @aaag_soup (BeautifulSoup): the soup in which to find the element
        @aaag_identification_type (str): the type of element (i.e. p, h1, title, img, a)
      Returns:
        The soup element if found, if not returns None
    """
    aaag_element = aaag_soup.find(aaag_element)

    return aaag_element


def aaag_get_elements_from_soup_all(aaag_soup, aaag_identification_type, aaag_identification_value):
    """Gets all the elements from a BeautifulSoup instance that match the identification method
      Args:
        @aaag_soup (BeautifulSoup): the soup in which to find the element
        @aaag_identification_type (str): the mean to identify the element. Valid options are (class, id)
        @aaag_identification_value (str): the value of the identification_type to search in the soup
      Returns:
        A list with the soup elements if found, if not returns and empty list
    """
    aaag_element = aaag_soup.find_all(
        attrs={aaag_identification_type: aaag_identification_value})

    return aaag_element


def aaag_get_text_from_element(aaag_soup):
    """Gets the text content of a BeautifulSoup element.
    Args:
      @aaag_soup (BeautifulSoup): The element from which to extract the text
    Returns:
      The text content if the element has one, if not returns an empty string
    """
    return aaag_soup.get_text(strip=True)


def aaag_get_element_attribute(aaag_soup, aaag_attribute):
    """Gets the content of the specified attribute from a BeautifulSoup element.
      Args:
        @aaag_soup (BeautifulSoup): The element from which to extract the attribute
        @aaag_attribute (str): the name of the attribute to extract
      Returns:
        The text representation of the attribute value if present, if not returns an empty string
    """
    if aaag_attribute in aaag_soup.attrs:
        return aaag_soup.attrs[aaag_attribute]
    else:
        return ""
