from aiogram.dispatcher.filters.state import State, StatesGroup

class UserData(StatesGroup):
    user_id = State()
    user_name = State()
    user_photo_path = State()
    add_sql = State()