import logging
import requests
from bs4 import BeautifulSoup as BS
from echo_bot.config import URL_WEATHER

logger = logging.getLogger('telebot.scraping_weather')


def get_weather():
    logger.debug('Scraping today`s Odessa weather with BeautifulSoup HTML parser.')
    page = requests.get(URL_WEATHER)
    soup = BS(page.content, 'html.parser')
    day = soup.find(id='bd1').text.strip()
    today_water = soup.find(class_='today-water').text.strip()
    description = soup.select('.wDescription .description')[0].text.strip()
    weather = [day, today_water, description]
    # print(weather)

    return weather


get_weather()
