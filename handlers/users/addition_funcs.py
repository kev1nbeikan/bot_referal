from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.STRIGNS import MENU, CAPTCHA_MESSAGE
from data.config import captcha_range
from loader import db
from keyboards.menu_keyboard import menu_keyboard

async def show_menu(message: types.Message):
    await message.answer(text=MENU, reply_markup=menu_keyboard)



async def send_captcha(message: types.Message, state: FSMContext):
    captcha = db.get_captcha(randint(0, captcha_range))
    await message.answer_photo(caption=CAPTCHA_MESSAGE, photo=captcha[0])
    await state.update_data(answer=captcha[1])

