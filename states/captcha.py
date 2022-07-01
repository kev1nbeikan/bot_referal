from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialogue(StatesGroup):
    wait_for_sub = State()
    wait_to_answering = State()
