import logging
import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import ContentType, ReplyKeyboardRemove

from data.STRIGNS import WELCOME_TEXT, CALL_BACK_ASK_CHECK, MENU, CAPTCHA_MESSAGE, REPEAT_WELCOME, INCORRECT_CAPTCHA
from .addition_funcs import send_captcha, show_menu
from loader import dp
from keyboards import check_sub_keyboard
# from keyboards import menu_keyboard
from utils.misc import check_sub, uuid_url64
from data.config import channels, captcha_range
from random import randint
from loader import db
from states.captcha import Dialogue
from aiogram.utils.deep_linking import get_start_link
from filters import IsDeeplink, NotInDB


@dp.message_handler(IsDeeplink(), NotInDB())
async def bot_start_ref(message: types.Message, state: FSMContext):
    if db.is_exist_user(message.from_user.id):
        await show_menu(message)
        return
    deep_link = message.text.split()[1]
    if db.check_referral(deep_link):
        await state.update_data(deep_link=deep_link)

    text = WELCOME_TEXT.format(message.from_user.full_name)
    await Dialogue.first()
    msg = await message.answer(text, reply_markup=check_sub_keyboard)
    await state.update_data(msg_id=msg.message_id)


@dp.message_handler(NotInDB())
async def bot_start(message: types.Message, state: FSMContext):
    if db.is_exist_user(message.from_user.id):
        await show_menu(message)
        return
    text = WELCOME_TEXT.format(message.from_user.full_name)
    await Dialogue.first()
    msg = await message.answer(text, reply_markup=check_sub_keyboard)
    await state.update_data(msg_id=msg.message_id)


@dp.callback_query_handler(text=CALL_BACK_ASK_CHECK, state=Dialogue.wait_for_sub)
async def check_sub_query(callback_query: types.CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    if await check_sub(user, channels[0]):
        await send_captcha(callback_query.message, state)
        data = await state.get_data()
        await dp.bot.edit_message_reply_markup(message_id=data['msg_id'], chat_id=callback_query.message.chat.id,
                                               reply_markup=None)
        await Dialogue.next()
    else:
        text = REPEAT_WELCOME.format(callback_query.message.from_user.full_name)
        await callback_query.message.answer(text)

    await callback_query.answer()

