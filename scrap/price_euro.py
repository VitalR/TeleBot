import logging
import requests
from bs4 import BeautifulSoup as BS
from echo_bot.config import URL_EURO

logger = logging.getLogger('telebot.scraping_euro')


def get_exchange_rate_euro():
    logger.debug('Scraping exchange rate of EURO with BeautifulSoup HTML parser.')
    page = requests.get(URL_EURO)
    soup = BS(page.content, 'html.parser')

    k0 = soup.find_all(class_='course')[0].text
    k1 = soup.find_all(class_='course')[1].text
    k2 = soup.find_all(class_='course')[2].text
    k3 = soup.find_all(class_='course')[3].text

    rate = [k0, k1, k2, k3]

    return rate


get_exchange_rate_euro()
