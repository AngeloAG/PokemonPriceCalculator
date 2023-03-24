# Author: Angelo Arellano Gaona
# Description: This program uses Selenium to scrap web pages and get prices for pokemon cards based on user search
from selenium import webdriver


def main():
    print("main")
    driver = webdriver.Chrome(executable_path='./drivers/chromedriver.exe')
    driver.get("https://google.com")


if __name__ == "__main__":
    main()
