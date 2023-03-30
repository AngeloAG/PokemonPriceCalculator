# Author: Angelo Arellano Gaona
# Description: This program uses Selenium to scrap web pages and get prices for pokemon cards based on the user search, all is displayed in a GUI made in tkinter
# Date: 3/30/2023

# IMPORTANT! Run " pip install -r requirements.txt " before running this program
# This program uses Selenium, BeautifulSoup and other packages that need to be installed for it to work properly
# After that, you can run the program via VSCODE or by " python main.py " in the terminal
# A window will appear, use the search bar and type a pokemon you want to search cards for and click on "search", if you want to save the results click on "search and save".

import webscraper as scraper
import json
from datetime import datetime
import tkinter as tk
from tkinter import Frame, Label, Button, Text, END, W, Scrollbar, Canvas
import webbrowser

DEBUG = True
# DEBUG = False


def main():
    # Create the Tk root object.
    aaag_root = tk.Tk()
    aaag_root.geometry('700x350')

    # Create the main window.
    aaag_frm_main = Frame(aaag_root)
    aaag_frm_main.master.title("Pokemon Price Calculator")
    aaag_frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=0)

    aaag_results_frame = Frame(aaag_root, height="250")
    aaag_results_frame.pack(
        padx=4, pady=3, fill=tk.BOTH, expand=0)

    aaag_populate_main_window(aaag_frm_main, aaag_results_frame)

    # Start the tkinter loop that processes user events
    # such as key presses and mouse button clicks.
    aaag_root.mainloop()


def aaag_populate_main_window(aaag_frame, aaag_results_frame):
    """Puts all the GUI elements for the window and binds the buttons to the actions that will populate the results of the search
      Parameter
          aaag_frame: the frame for the search elements
          aaag_results_frame: the frame that will hold the results of a search
      Return: nothing
      """
    # Search bar elements
    aaag_header_lbl = Label(
        aaag_frame, text='Card name (i.e. Charizard):', justify="left", anchor="w")
    aaag_searchbar_ent = Text(aaag_frame, height=1, width=30)
    aaag_search_btn = Button(aaag_frame, text='Search',
                             width=10)
    aaag_save_btn = Button(aaag_frame, text='Search and Save Results')
    # This label is used to display informational messages to the user
    aaag_action_lbl = Label(
        aaag_frame, text="", justify="left", anchor="w")

    # Adding the elements to the frame on a grid
    aaag_header_lbl.grid(row=0, column=0, padx=3, pady=3)
    aaag_searchbar_ent.grid(row=0, column=1, padx=1, pady=3)
    aaag_search_btn.grid(row=0, column=3, padx=10, pady=3)
    aaag_save_btn.grid(row=0, column=4, padx=5, pady=3)

    aaag_debug("Basic elements populated successfully")

    def aaag_save():
        """Function to search and save the search results to file. It shows the name of the savefile to the user on the GUI"""
        aaag_search_term = aaag_searchbar_ent.get("1.0", END)
        aaag_search_term = aaag_search_term.strip()
        aaag_action_lbl.grid_forget()

        if aaag_search_term != "":
            # Displaying a message to let the user know it is working
            aaag_action_lbl.configure(text="Searching...")
            aaag_action_lbl.grid(row=1, column=0, padx=3, pady=3)
            aaag_frame.update()

            aaag_results = aaag_get_cards_information(aaag_search_term)
            aaag_debug(f"Amount of results {str(len(aaag_results))}")

            # Letting know it is saving
            aaag_action_lbl.configure(text="Saving...")
            aaag_frame.update()

            aaag_save_filename = aaag_save_results(aaag_results)

            aaag_debug(f"File Saved {aaag_save_filename}")

            # Letting know the name of the savefile
            aaag_action_lbl.configure(text=aaag_save_filename)
            aaag_frame.update()

    def aaag_search():
        """Performs the search of the value in the searchbar and calls the function to put them on the GUI"""
        aaag_search_term = aaag_searchbar_ent.get("1.0", END)
        aaag_search_term = aaag_search_term.strip()
        aaag_action_lbl.grid_forget()

        if aaag_search_term != "":
            # Displaying a message to let the user know it is working
            aaag_action_lbl.configure(text="Searching...")
            aaag_action_lbl.grid(row=1, column=0, padx=3, pady=3)
            aaag_frame.update()

            aaag_results = aaag_get_cards_information(aaag_search_term)
            aaag_debug(f"Amount of results {str(len(aaag_results))}")

            # Removing the waiting message
            aaag_action_lbl.grid_forget()

            aaag_populate_results(aaag_results)

    def aaag_populate_results(aaag_results):
        """Populates the results of a search on the results frame. Usually called by the aaag_search function"""

        # Removing any result from previous searches
        for aaag_element in aaag_results_frame.winfo_children():
            aaag_element.destroy()

        # Creating a canvas and scrollbar for the results
        aaag_canvas = Canvas(aaag_results_frame)
        aaag_scrollbar = Scrollbar(
            aaag_results_frame, orient="vertical", command=aaag_canvas.yview)

        # The scrollable_frame goes inside the canvas that allows the scroll
        aaag_scrollable_frame = Frame(aaag_canvas)

        # Binding the configuration of the canvas to the frame so it recalculates the area to scroll
        aaag_scrollable_frame.bind(
            "<Configure>",
            lambda e: aaag_canvas.configure(
                scrollregion=aaag_canvas.bbox("all")
            )
        )

        # Creating the space in which the scrollable frame will be displayed
        aaag_canvas.create_window(
            (0, 0), window=aaag_scrollable_frame, anchor="nw")

        # Setting the scrollbar behavior to the scroll on y axis command of the canvas
        aaag_canvas.configure(yscrollcommand=aaag_scrollbar.set)

        # Iterating through the results and building the GUI elements to be added to the frame
        aaag_row_idx = 0
        for result in aaag_results:
            aaag_card_name_lbl = Label(
                aaag_scrollable_frame, text="Name: " + result['card_name'], anchor="w", justify="left")

            aaag_card_expansion = Label(
                aaag_scrollable_frame, text="Expansion: " + result['card_expansion'], anchor="w", justify="left")

            aaag_card_price = Label(
                aaag_scrollable_frame, text="Price: " + result['card_price'], anchor="w", justify="left")

            aaag_card_hyperlink = Label(
                aaag_scrollable_frame, text=result['card_hyperlink'], anchor="w", justify="left", fg="blue", cursor="hand2", wraplength=500)

            aaag_separator = Label(
                aaag_scrollable_frame, text="----------------------------------", anchor="w", justify="left")

            def aaag_open_url(aaag_event):
                """Function to open the link to the card"""
                webbrowser.open_new_tab(aaag_event.widget.cget("text"))

            # To allow the user to click on the label and open the url
            aaag_card_hyperlink.bind(
                "<Button-1>", aaag_open_url)

            aaag_card_name_lbl.grid(
                row=aaag_row_idx, column=1, padx=3, pady=3, sticky=W)
            aaag_card_expansion.grid(
                row=aaag_row_idx+1, column=1, padx=3, pady=3, sticky=W)
            aaag_card_price.grid(row=aaag_row_idx+2, column=1,
                                 padx=3, pady=3, sticky=W)
            aaag_card_hyperlink.grid(
                row=aaag_row_idx+3, column=1, padx=3, pady=3, sticky=W)
            aaag_separator.grid(
                row=aaag_row_idx+4, column=1, padx=3, pady=3, sticky=W)

            # The amount of rows to skip to accomodate the next result
            aaag_row_idx += 5

        aaag_debug("Results populated successfully")
        # Rendering the canvas and the scrollbar
        aaag_canvas.pack(side="left", fill="both", expand=True)
        aaag_scrollbar.pack(side="right", fill="y")

    aaag_search_btn.config(command=aaag_search)
    aaag_save_btn.config(command=aaag_save)


def aaag_save_results(aaag_results):
    """Function to save the results of a search to a json file, it saves it in the same folder the code is being executed
     Args:
         @aaag_message (list): The results to save
       Returns:
         Name of the file (str)"""
    aaag_results_json_str = json.dumps(aaag_results)
    aaag_file_name = 'search_' + datetime.now().strftime('%m%d%Y-%H%M%S') + '.json'
    with open(aaag_file_name, 'w')as save_file:
        save_file.write(aaag_results_json_str)

    return aaag_file_name


def aaag_debug(aaag_message):
    """Function to print debug values to console only when the program is on debug
    Args:
        @aaag_message (str): the message to print
      Returns:
        Nothing"""
    if DEBUG:
        print(aaag_message)


def aaag_get_cards_information(aaag_card_name):
    """Function to scrap web pages to find prices for a pokemon tcg card.
    Args:
      @aaag_card_name (str): the search term to scrap webpages for
    Returns: a list of dictionaries, each dictionary contains a result for the search"""
    # Pages that will be use to conduct the search. If is desired to search on more pages, add them to the list.
    AAAG_PAGES = [
        {
            'site': 'tcgplayer',
            'base_url': 'https://www.tcgplayer.com',
            'search_url': 'https://www.tcgplayer.com/search/all/product?q=',
            'results_limit': 5,
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
            'base_url': 'https://www.trollandtoad.com',
            'search_url': 'https://www.trollandtoad.com/category.php?selected-cat=0&view=grid&search-words=',
            'results_limit': 5,
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

    aaag_results = []
    for page in AAAG_PAGES:
        aaag_url = page['search_url'] + aaag_card_name + "%20pokemon"
        aaag_debug(aaag_url)

        # Getting main soup
        aaag_soup = scraper.aaag_get_html_until_element_present(
            aaag_url, page['anchor_element']['identifier_type'], page['anchor_element']['identifier_value'])
        aaag_soup_title_element = scraper.aaag_get_element_from_soup_by_element(
            aaag_soup, "title")
        aaag_soup_title = scraper.aaag_get_text_from_element(
            aaag_soup_title_element)

        aaag_debug(f"Soup title: {aaag_soup_title}")

        if aaag_soup_title != "Not found":
            aaag_results_container_soup = scraper.aaag_get_element_from_soup(
                aaag_soup, page['results_container']['identifier_type'], page['results_container']['identifier_value'])
            aaag_results_soups = scraper.aaag_get_elements_from_soup_all(
                aaag_results_container_soup, page['result_card']['identifier_type'], page['result_card']['identifier_value'])

            # In case the results are less than the normal expected results
            aaag_results_amount = len(aaag_results_soups) if (
                len(aaag_results_soups) < page['results_limit']) else page['results_limit']
            aaag_debug(f"Results amount: {aaag_results_amount}")

            for idx in range(0, aaag_results_amount):
                aaag_result = {}
                result_card = aaag_results_soups[idx]

                # Getting the name of the card
                aaag_result_name_soup = scraper.aaag_get_element_from_soup(
                    result_card, page['result_name']['identifier_type'], page['result_name']['identifier_value'])
                aaag_result['card_name'] = scraper.aaag_get_text_from_element(
                    aaag_result_name_soup)

                aaag_debug(f"Card Name: {aaag_result['card_name']}")

                # Getting the card img url
                aaag_result_img_soup = scraper.aaag_get_element_from_soup(
                    result_card, page['result_img']['identifier_type'], page['result_img']['identifier_value'])
                aaag_result['card_img'] = scraper.aaag_get_element_attribute(
                    aaag_result_img_soup, page['result_img']['attribute'])

                aaag_debug(f"Card Img: {aaag_result['card_img']}")

                # Getting the card price
                aaag_result_price_soup = scraper.aaag_get_element_from_soup(
                    result_card, page['result_price']['identifier_type'], page['result_price']['identifier_value'])
                if aaag_result_price_soup is None:
                    aaag_result['card_price'] = 'Not provided'
                else:
                    aaag_result['card_price'] = scraper.aaag_get_text_from_element(
                        aaag_result_price_soup)

                aaag_debug(f"Card Price: {aaag_result['card_price']}")

                # Getting card expansion
                aaag_result_expansion_soup = scraper.aaag_get_element_from_soup(
                    result_card, page['result_expansion']['identifier_type'], page['result_expansion']['identifier_value'])
                aaag_result['card_expansion'] = scraper.aaag_get_text_from_element(
                    aaag_result_expansion_soup)

                aaag_debug(f"Card Expansion: {aaag_result['card_expansion']}")

                # Getting card hyperlink to website page
                aaag_result_hyperlink_soup = scraper.aaag_get_element_from_soup_by_element(
                    result_card, page['result_hyperlink']['element_type'])

                aaag_card_hyperlink = scraper.aaag_get_element_attribute(
                    aaag_result_hyperlink_soup, page['result_hyperlink']['attribute'])

                # This converts the subaddress of the link into a real url
                aaag_result['card_hyperlink'] = page['base_url'] + \
                    aaag_card_hyperlink

                aaag_debug(f"Card Hyperlink: {aaag_result['card_hyperlink']}")

                aaag_results.append(aaag_result)
    return aaag_results


if __name__ == "__main__":
    main()
