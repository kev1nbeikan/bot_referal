from aiogram import Bot
from typing import Union


async def check_sub(identifier: int, channel: Union[str, int]):
    bot = Bot.get_current()
    user = await bot.get_chat_member(chat_id=channel, user_id=identifier)
    return user.is_chat_member()
