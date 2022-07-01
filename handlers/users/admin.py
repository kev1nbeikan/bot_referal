import logging

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from data.STRIGNS import INVITES_INFO, INPUT_TO_SHOW, LINK_USER
from filters import IsAdmin
from loader import dp, db


@dp.message_handler(IsAdmin(), text=INPUT_TO_SHOW, state='*')
async def info(message: types.Message):
    text = INVITES_INFO + '\n'
    for user, count in  db.get_top_invites_count():
        text +='\n'
        text = text + LINK_USER + str(user) + ' ---- ' + str(count)
    await message.answer(text=text)
