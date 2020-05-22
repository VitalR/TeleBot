import logging
import requests
from bs4 import BeautifulSoup as BS
from echo_bot.config import URL_BTC

logger = logging.getLogger('telebot.scraping_btc')


def get_exchange_rate_btc():
    logger.debug('Scraping exchange rate of BTC with BeautifulSoup HTML parser.')
    page = requests.get(URL_BTC)
    soup = BS(page.content, 'html.parser')

    price = soup.find(class_='cmc-details-panel-price__price').text
    # print(price)
    price_change = soup.find(class_='cmc--change-negative cmc-details-panel-price__price-change').text
    # print(price_change)

    btc_rate = [price, price_change]
    return btc_rate


get_exchange_rate_btc()
