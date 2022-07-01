from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsDeeplink(BoundFilter):

    async def check(self, message: types.Message):
        return len(message.text.split()) == 2