"""
Simple Echo Telegram Bot.
Functionality: Odessa weather, time, exchange rate of USD, EURO and BTC.
"""

import datetime
import logging

from subprocess import Popen
from subprocess import PIPE

from telegram import Bot, ParseMode
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import Filters
from echo_bot.config import TG_TOKEN
from scrap.price_usd import get_exchange_rate_usd
from scrap.price_euro import get_exchange_rate_euro
from scrap.price_btc import get_exchange_rate_btc
from scrap.weather import get_weather
from echo_bot.buttons import BUTTON1_WEATHER
from echo_bot.buttons import BUTTON2_TIME
from echo_bot.buttons import get_base_reply_keyboard
from telegram.ext import CallbackQueryHandler

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H%:%M:%S',
                    level=logging.DEBUG,
                    filemode='logs.txt')

logger = logging.getLogger('telebot')

logger.info('Telegram Bot running...')

CALLBACK_BUTTON_LEFT_PRICE_USD = 'callback_button_left_price_usd'
CALLBACK_BUTTON_RIGHT_PRICE_EURO = 'callback_button_right_price_usd'
CALLBACK_BUTTON_CENTER_PRICE_BTC = 'callback_button_right_price_btc'

TITLES = {
    CALLBACK_BUTTON_LEFT_PRICE_USD: "USD",
    CALLBACK_BUTTON_RIGHT_PRICE_EURO: "EURO",
    CALLBACK_BUTTON_CENTER_PRICE_BTC: "BTC"

}


def get_base_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_LEFT_PRICE_USD], callback_data=CALLBACK_BUTTON_LEFT_PRICE_USD),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_RIGHT_PRICE_EURO],
                                 callback_data=CALLBACK_BUTTON_RIGHT_PRICE_EURO)
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_CENTER_PRICE_BTC],
                                 callback_data=CALLBACK_BUTTON_CENTER_PRICE_BTC)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(bot: Bot, update: Update, chat_data=None, **kwargs):
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON_LEFT_PRICE_USD:

        try:
            items = get_exchange_rate_usd()
            text = f"Kurs.com.ua - USD\nКурс в банках:\n{items[0]}\n{items[1]}\nКоммерческий:\n{items[2]}\nНБУ:\n{items[3]}"
            logger.debug('Get exchange rate of USD for `{text}`.')
        except Exception:
            text = 'ERROR has happened'
            logger.debug(text)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_base_inline_keyboard()
        )

    elif data == CALLBACK_BUTTON_RIGHT_PRICE_EURO:

        try:
            items = get_exchange_rate_euro()
            text = f"Kurs.com.ua - EURO\nКурс в банках:\n{items[0]}\n{items[1]}\nКоммерческий:\n{items[2]}\nНБУ:\n{items[3]}"
            logger.debug('Get exchange rate of EURO for `{text}`.')
        except Exception:
            text = 'ERROR has happened'
            logger.debug(text)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_base_inline_keyboard()
        )

    elif data == CALLBACK_BUTTON_CENTER_PRICE_BTC:

        try:
            items = get_exchange_rate_btc()
            text = f"coinmarketcap.com - BTC:\n{items[0]}\n{items[1]}"
            logger.debug('Get exchange rate of BTC for `{text}`.')
        except Exception:
            text = 'ERROR has happened'
            logger.debug(text)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_base_inline_keyboard()
        )


def start_bot(bot: Bot, update: Update):
    logger.info('Getting weather...')

    try:
        items = get_weather()
        text = f"Привет, погода на сегодня:\n{items[0]}\n{items[1]}\n{items[2]}"
        logger.debug('Get Odessa weather for today `{text}`.')
    except Exception:
        text = 'ERROR has happened'
        logger.debug(text)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=get_base_inline_keyboard()
    )


def helper(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="This is a test Telebot-Helper.\n"
             "The list of available commands can be found in menu.\n"
             "I can help you to check today Odessa weather, current time and the exchange rate for USD, EURO and BTC.\n"
             "Please choose the command",
        reply_markup=get_base_inline_keyboard()
    )


def get_time(bot: Bot, update: Update):
    process = Popen(['date'], stdout=PIPE)
    result = process.communicate()  # Waiting the result
    text, error = result
    if error:
        text = "Error has happened."
    else:
        text = text.decode('utf-8')

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text
    )


def create_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == BUTTON1_WEATHER:
        return start_bot(bot=bot, update=update)
    elif text == BUTTON2_TIME:
        return get_time(bot=bot, update=update)
    else:
        reply_text = "Your ID = {}\nPlease choose a command.\n".format(chat_id, text)
        update.message.reply_text(
            text=reply_text,
            reply_markup=get_base_reply_keyboard()
        )


def main():
    logger.info('Starting telebot...')

    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot)

    start_handler = CommandHandler('start', start_bot)
    helper_handler = CommandHandler('help', helper)
    time_handler = CommandHandler('time', get_time)
    message_handler = MessageHandler(Filters.text, create_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(helper_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()

    logger.info('Finishing telebot...')


if __name__ == '__main__':
    main()
