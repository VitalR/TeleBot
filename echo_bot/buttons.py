from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON1_WEATHER = 'Погода'
BUTTON2_TIME = 'Время'


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_WEATHER),
            KeyboardButton(BUTTON2_TIME)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
