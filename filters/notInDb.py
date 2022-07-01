from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class NotInDB(BoundFilter):

    async def check(self, message: types.Message):
        return not db.is_exist_user(message.from_user.id)