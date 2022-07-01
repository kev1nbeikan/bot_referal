from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType

from data.STRIGNS import MENU, INCORRECT_CAPTCHA
from .addition_funcs import show_menu, send_captcha
from loader import dp, db
from states.captcha import Dialogue
from utils.misc import uuid_url64






# @dp.message_handler(Command('cancel'))
# async def check_answer_captcha(message: types.Message, state: FSMContext):
#     await state.finish()




@dp.message_handler(content_types=ContentType.TEXT, state=Dialogue.wait_to_answering)
async def check_answer_captcha(message: types.Message, state: FSMContext):
    answer_ = message.text
    data = await state.get_data()
    if answer_ == data['answer']:

        while db.check_referral(link := uuid_url64()):
            pass

        if 'deep_link' in data:
            db.update_invites_count(data['deep_link'])
        db.add_user(message.from_user.id, link)


        await show_menu(message)
        await state.finish()
    else:
        await message.answer(text=INCORRECT_CAPTCHA)
        await send_captcha(message, state)



