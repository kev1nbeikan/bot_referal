import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, InputFile

from data.STRIGNS import REPEAT_WELCOME
from .addition_funcs import show_menu
from loader import dp, db
from states.captcha import Dialogue


@dp.message_handler(state='*')
async def another(message: types.Message, state: FSMContext):
    current = await state.get_state()
    logging.info(message.from_user.id)

    if current == Dialogue.wait_for_sub.state:
        text = REPEAT_WELCOME
        await message.answer(text)
    else:
        await show_menu(message)



@dp.message_handler(content_types=ContentType.ANY)
async def bot_echo(message: types.Message):
    # for filename in os.listdir('handlers/users/archive'):
    #     f =  InputFile('handlers/users/archive/' + filename, 'r')
    #     # open in readonly mode
    #     logging.info(f)
    #     msg = await message.answer_photo(photo=f)
    #     db.add_captcha(msg.photo[0].file_id, filename.split('.')[0])
    await message.answer(text=message.text)


@dp.channel_post_handler()
async def channel_echo(message: types.Message):
    await message.answer(message.chat.id)
