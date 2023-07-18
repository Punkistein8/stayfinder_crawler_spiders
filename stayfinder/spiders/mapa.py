import scrapy
import time
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from ..items import MapsItem

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(
    '../../chromedriver.exe'), options=options)


class MapaSpider(scrapy.Spider):
    name = "mapa"

    def start_requests(self):
        url = 'https://www.google.com/maps/search/hoteles+cerca+de+Latacunga/@-0.9331232,-78.6240887,12z/data=!4m6!2m5!5m3!5m2!4m1!1i1!6e3?entry=ttu'
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        driver.get(response.url)
        driver.implicitly_wait(10)

        cardsContainer = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')))

        for i in range(0, 10):
            print('Scrolling... #', i)
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", cardsContainer)
            time.sleep(1)

            # if i == 6:
            #     try:
            #         driver.find_element(By.CLASS_NAME, 'HlvSq')
            #         print('No hay mas hoteles')
            #         break
            #     except NoSuchElementException:
            #         pass

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'Nv2PK')))

        # rawCards = cardsContainer.find_elements(
        #     By.CLASS_NAME, 'Nv2PK')

        rawCards = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_elements(By.CLASS_NAME, 'Nv2PK')
        )

        wait = WebDriverWait(driver, 10)
        for card in rawCards:
            try:
                wait.until(EC.element_to_be_clickable(card)).click()
                card.click()
                card.click()

                time.sleep(1)

                contenedorFoto = wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'aoRNLd')))
                foto = contenedorFoto.find_element(
                    By.TAG_NAME, 'img').get_attribute('src')
                
                time.sleep(1)
                
                nombreHotel = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'DUwDvf'))).text

                containerEstrellas = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'F7nice')))
                estrellas = containerEstrellas.find_element(
                    By.TAG_NAME, 'span').text

                containerPrecio = wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'dkgw2')))
                precio = containerPrecio.find_element(
                    By.TAG_NAME, 'span').text


                wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'yHy1rc'))).click()

                time.sleep(1)
            except:
                pass
            driver.implicitly_wait(10)

            items = MapsItem()

            items['nombreHotel'] = nombreHotel
            items['estrellas'] = estrellas
            items['precio'] = precio
            items['foto'] = foto

            yield items
