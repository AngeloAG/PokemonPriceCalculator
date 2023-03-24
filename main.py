# Author: Angelo Arellano Gaona
# Description: This program uses Selenium to scrap web pages and get prices for pokemon cards based on user search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def main():
    print("main")
    driver_service = Service(executable_path="/drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    driver.get("https://google.com")


if __name__ == "__main__":
    main()
