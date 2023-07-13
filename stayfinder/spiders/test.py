import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from ..items import ZzItem

options = webdriver.ChromeOptions()

options.add_argument("--no-sandbox")

# options.add_argument("--headless")

options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome(service=Service(
    'C:\chromedriver.exe'), options=options)


class TestSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        url = 'https://www.google.com/maps/search/hoteles+cerca+de+Latacunga/@-0.9331232,-78.6240887,15z/data=!4m6!2m5!5m3!5m2!4m1!1i1!6e3?entry=ttu'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        driver.get(response.url)
        # driver.implicitly_wait(10)
        rawData = driver.find_elements(By.CLASS_NAME, 'bfdHYd')
        for card in rawData:
            hotel = card.find_element(By.CLASS_NAME, 'qBF1Pd').text

            items = ZzItem()

            items['nombreHotel'] = hotel

            yield items
            print(hotel)
