# Author: Angelo Arellano Gaona
# Description:
#   These are a series of tests performed on the webscraper module to ensure the proper functionality of them

import pytest
from webscraper import *
from bs4 import BeautifulSoup


def ntest_aaag_get_html_until_element_present():
    """Tests the functionality of the function to get the html from a webpage
    Args: None
    Returns: Nothing
    """
    # Ensuring it opens web pages correctly ------------------------
    aaag_google_url = "https://google.com"
    aaag_soup = aaag_get_html_until_element_present(
        aaag_google_url, "id", "hplogo")

    # ensure the soup has an html tag
    assert aaag_soup.find("html"), "The returned element contains no HTML"
    # ensure the opened page was google
    assert aaag_soup.title.get_text() == "Google", "Wrong webpage"

    aaag_bing_url = "https://bing.com"
    aaag_soup = aaag_get_html_until_element_present(
        aaag_bing_url, "class", "logo_cont")

    # ensure the soup has an html tag
    assert aaag_soup.find("html"), "The returned element contains no HTML"
    # ensure the opened page was bing
    assert aaag_soup.title.get_text() == "Bing", "Wrong webpage"
    # -------------------------------------------------------------------

    # Ensuring it handles when a element non present in the page is passed ----
    aaag_google_url = "https://google.com"
    aaag_soup = aaag_get_html_until_element_present(
        aaag_google_url, "id", "09876544")

    # ensure the soup has an html tag
    assert aaag_soup.find("html"), "The returned element contains no HTML"
    # ensure the returned soup has Not found as title
    assert aaag_soup.title.get_text() == "Not found", "Wrong webpage"
    # Asserting the right exception was raised
    assert aaag_soup.body.get_text(
    ) == "Took too long to load", "Wrong exception, expected (Took too long to load)"
    # -------------------------------------------------------------------

    # ensuring it handles non existent web pages------------------------
    aaag_invalid_url = "https://12345678764534.com"
    aaag_soup = aaag_get_html_until_element_present(
        aaag_invalid_url, "id", "09876544")

    # ensure the soup has an html tag
    assert aaag_soup.find("html"), "The returned element contains no HTML"
    # ensure the returned soup has Not found as title
    assert aaag_soup.title.get_text() == "Not found", "Wrong webpage"
    # Asserting the right exception was raised
    assert aaag_soup.body.get_text(
    ) == "Page not found", "Wrong exception, expected (Page not found)"


def test_aaag_get_element_from_soup():
    """Tests if the function aaag_get_element_from_soup returns the element searched
    Args: None
    Returns: Nothing"""

    # Custom soup for the test
    aaag_soup = BeautifulSoup(
        """<html><head><title>Test page</title></head><body><h1 class="header">Test header</h1><p id="paragraph">Test paragraph</p></body></html>""", features="html.parser")

    # ensureing it can search for the header element by its class
    aaag_element = aaag_get_element_from_soup(aaag_soup, "class", "header")
    assert aaag_element is not None, "Expected a beautifulsoup object"
    assert aaag_element.get_text() == "Test header"

    # ensuring it can search for the paragraph element by id
    aaag_element = aaag_get_element_from_soup(aaag_soup, "id", "paragraph")
    assert aaag_element is not None, "Expected a beautifulsoup object"
    assert aaag_element.get_text() == "Test paragraph"

    # ensuring that when searching for a non existent element None is returned
    aaag_element = aaag_get_element_from_soup(aaag_soup, "id", "nonexistent")
    assert aaag_element is None, "Expected a beautifulsoup object"


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])
