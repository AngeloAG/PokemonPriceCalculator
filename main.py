# Author: Angelo Arellano Gaona
# Description: This program uses Selenium to scrap web pages and get prices for pokemon cards based on the user search

# from webscraper import aaag_get_html_until_element_present_byclass
import webscraper as scraper
import json
from datetime import datetime

DEBUG = True
DEBUG = False

AAAG_PAGES = [
    {
        'site': 'tcgplayer',
        'base_url': 'https://www.tcgplayer.com',
        'search_url': 'https://www.tcgplayer.com/search/all/product?q=',
        'results_limit': 1,
        'anchor_element': {
            'identifier_value': 'search-results',
            'identifier_type': 'class'
        },
        'results_container': {
            'identifier_value': 'search-results',
            'identifier_type': 'class'
        },
        'result_card': {
            'identifier_value': 'search-result',
            'identifier_type': 'class'
        },
        'result_img': {
            'identifier_value': 'v-lazy-image',
            'identifier_type': 'class',
            'attribute': 'src'
        },
        'result_name': {
            'identifier_value': 'search-result__title',
            'identifier_type': 'class'
        },
        'result_price': {
            'identifier_value': 'inventory__price-with-shipping',
            'identifier_type': 'class'
        },
        'result_expansion': {
            'identifier_value': 'search-result__subtitle',
            'identifier_type': 'class'
        },
        'result_hyperlink': {
            'element_type': 'a',
            'attribute': 'href'
        }
    },
    {
        'site': 'trollandtoad',
        'base_url': 'https://www.trollandtoad.com/',
        'search_url': 'https://www.trollandtoad.com/category.php?selected-cat=0&view=grid&search-words=',
        'results_limit': 1,
        'anchor_element': {
            'identifier_value': 'product-col',
            'identifier_type': 'class'
        },
        'results_container': {
            'identifier_value': 'result-container',
            'identifier_type': 'class'
        },
        'result_card': {
            'identifier_value': 'product-col',
            'identifier_type': 'class'
        },
        'result_img': {
            'identifier_value': 'productImage',
            'identifier_type': 'class',
            'attribute': 'src'
        },
        'result_name': {
            'identifier_value': 'card-text',
            'identifier_type': 'class'
        },
        'result_price': {
            'identifier_value': 'font-smaller font-weight-bold text-sm-center pr-2 text-success',
            'identifier_type': 'class'
        },
        'result_expansion': {
            'identifier_value': 'row mb-2',
            'identifier_type': 'class'
        },
        'result_hyperlink': {
            'element_type': 'a',
            'attribute': 'href'
        }
    },
]


def main():
    print("main")
    aaag_card_name = input("Enter the card name: ")

    aaag_results = []

    for page in AAAG_PAGES:
        aaag_result = {}
        aaag_url = page['search_url'] + aaag_card_name
        aaag_debug(aaag_url)

        # Getting main soup
        aaag_soup = scraper.aaag_get_html_until_element_present(
            aaag_url, page['anchor_element']['identifier_type'], page['anchor_element']['identifier_value'])
        aaag_results_container_soup = scraper.aaag_get_element_from_soup(
            aaag_soup, page['results_container']['identifier_type'], page['results_container']['identifier_value'])
        aaag_results_soups = scraper.aaag_get_elements_from_soup_all(
            aaag_results_container_soup, page['result_card']['identifier_type'], page['result_card']['identifier_value'])

        # In case the results are less than the normal expected results
        aaag_results_amount = len(aaag_results_soups) if (
            len(aaag_results_soups) < page['results_limit']) else page['results_limit']
        aaag_debug(f"Results amount: {aaag_results_amount}")

        for idx in range(0, aaag_results_amount):
            result_card = aaag_results_soups[idx]

            # Getting the name of the card
            aaag_result_name_soup = scraper.aaag_get_element_from_soup(
                result_card, page['result_name']['identifier_type'], page['result_name']['identifier_value'])
            aaag_result['card_name'] = scraper.aaag_get_text_from_element(
                aaag_result_name_soup)

            # Getting the card img url
            aaag_result_img_soup = scraper.aaag_get_element_from_soup(
                result_card, page['result_img']['identifier_type'], page['result_img']['identifier_value'])
            aaag_result['card_img'] = scraper.aaag_get_element_attribute(
                aaag_result_img_soup, page['result_img']['attribute'])

            # Getting the card price
            aaag_result_price_soup = scraper.aaag_get_element_from_soup(
                result_card, page['result_price']['identifier_type'], page['result_price']['identifier_value'])
            aaag_result['card_price'] = scraper.aaag_get_text_from_element(
                aaag_result_price_soup)

            # Getting card expansion
            aaag_result_expansion_soup = scraper.aaag_get_element_from_soup(
                result_card, page['result_expansion']['identifier_type'], page['result_expansion']['identifier_value'])
            aaag_result['card_expansion'] = scraper.aaag_get_text_from_element(
                aaag_result_expansion_soup)

            # Getting card hyperlink to website page
            aaag_result_hyperlink_soup = scraper.aaag_get_element_from_soup_by_element(
                result_card, page['result_hyperlink']['element_type'])

            aaag_card_hyperlink = scraper.aaag_get_element_attribute(
                aaag_result_hyperlink_soup, page['result_hyperlink']['attribute'])

            aaag_result['card_hyperlink'] = page['base_url'] + \
                aaag_card_hyperlink

            aaag_results.append(aaag_result)

    aaag_debug(aaag_results)
    aaag_save_results(aaag_results)


def aaag_save_results(aaag_results):
    """Function to save the results of a search to a json file
     Args:
         @aaag_message (list): The results to save
       Returns:
         Nothing"""
    aaag_results_json_str = json.dumps(aaag_results)
    aaag_file_name = 'search_' + datetime.now().strftime('%m%d%Y-%H%M%S') + '.json'
    with open(aaag_file_name, 'w')as save_file:
        save_file.write(aaag_results_json_str)


def aaag_debug(aaag_message):
    """Function to print debug values to console only when the program is on debug
    Args:
        @aaag_message (str): the message to print
      Returns:
        Nothing"""
    if DEBUG:
        print(aaag_message)


if __name__ == "__main__":
    main()
