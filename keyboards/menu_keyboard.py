from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.STRIGNS import MENU_REF_BUTTON, MENU_GROUP_BUTTON, MENU_TERM_BUTTON

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.row(MENU_TERM_BUTTON, MENU_REF_BUTTON)
menu_keyboard.add(MENU_GROUP_BUTTON)