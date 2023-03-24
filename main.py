# Author: Angelo Arellano Gaona
# Description: This program uses Selenium to scrap web pages and get prices for pokemon cards based on the user search

# from webscraper import aaag_get_html_until_element_present_byclass
import webscraper as scraper

AAAG_TCGP_BASE_URL = "https://www.tcgplayer.com/search/all/product?q="
AAAG_TANDT_BASE_URL = "https://www.trollandtoad.com/category.php?selected-cat=0&search-words="


def main():
    print("main")
    aaag_card_name = "charizard"  # input("Enter the card name: ")

    aaag_tcg_search_url = AAAG_TCGP_BASE_URL + aaag_card_name

    # aaag_tcg_search_url = AAAG_TANDT_BASE_URL + aaag_card_name

    aaag_soup = scraper.aaag_get_html_until_element_present(
        aaag_tcg_search_url, "class", "search-results")

    aaag_el = scraper.aaag_get_elements_from_soup_all(
        aaag_soup, "class", "search-result")

    aaag_ch = scraper.aaag_get_element_from_soup(
        aaag_el[0], "class", "v-lazy-image")

    # aaag_text = scraper.aaag_get_text_from_element(aaag_ch)
    aaag_img = scraper.aaag_get_element_attribute(aaag_ch, "src")

    print(aaag_ch)
    print(aaag_img)


if __name__ == "__main__":
    main()
