from aiogram import types
from aiogram.types import ContentTypes
from data.STRIGNS import MENU_TERM, MENU_REF, MENU_GROUP, MENU_GROUP_BUTTON, MENU_TERM_BUTTON, MENU_REF_BUTTON
from loader import dp, db
from data.config import BOT_LINK

@dp.message_handler(text=MENU_TERM_BUTTON)
async def menu_terms(message: types.Message):
    user = message.from_user.id
    await message.answer(text=MENU_TERM.format(BOT_LINK + '=' + db.get_referral_user(user)))


@dp.message_handler(text=MENU_GROUP_BUTTON)
async def menu_terms(message: types.Message):
    await message.answer(text=MENU_GROUP)


@dp.message_handler(text=MENU_REF_BUTTON)
async def menu_terms(message: types.Message):
    user = message.from_user.id
    await message.answer(text=MENU_REF.format(db.get_invites_count_by_id(user), BOT_LINK + '=' + db.get_referral_user(user)))