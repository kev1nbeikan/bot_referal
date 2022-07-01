from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.STRIGNS import ASK_TO_CHECK, CALL_BACK_ASK_CHECK

check_sub_keyboard = InlineKeyboardMarkup()

check_sub_keyboard.insert(InlineKeyboardButton(text=ASK_TO_CHECK, callback_data=CALL_BACK_ASK_CHECK))