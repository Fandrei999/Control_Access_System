from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN, persons_path, bot_password
import keyboards as kb
import queries as sql
from random import randrange
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from user_states import UserData as ud
from face_model import train_model_by_img
import os

connection = sql.create_connection()
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# Старт бота
@dp.message_handler(commands=['start'])
async def shop(message: types.Message):
    await message.answer("Введите пароль Администратора:")


# Функции бота

# Отчет из SQL
@dp.callback_query_handler(lambda c: c.data == 'A')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, sql.get_report())


# Выбор пользователя из второстепенного меню
@dp.callback_query_handler(lambda c: c.data == 'B')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите пользователя!', reply_markup=kb.secondary_menu)


# Создание нового пользователя
@dp.callback_query_handler(lambda c: c.data == 'new', state='*')
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await state.update_data(user_id=user_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, 'Пришлите имя пользователя!')
    await ud.user_name.set()


# Добавляем пользователя
@dp.callback_query_handler(lambda c: c.data == 'add_user', state=ud.add_sql)
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        user_name = data['user_name']
        os.mkdir(f'{persons_path}/{user_name}')
        print(user_name)
        add_user = f"""
               INSERT INTO
                 `users` (`name`, `access`)
               VALUES
                  ('{user_name}', 'True');
                """
        sql.execute_query(connection, add_user)
        train_model_by_img()
        await state.finish()
        await bot.send_message(callback_query.from_user.id, "Пользователь добавлен в базу✅:", reply_markup=kb.main_menu)


# Кнопка назад
@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Главное меню:', reply_markup=kb.main_menu)


# Блок для пользователя user_1
@dp.callback_query_handler(lambda c: c.data == 'user_1')
async def process_callback_button(callback_query: types.CallbackQuery):
    photo = open(f'{persons_path}/user_1/user_1.jpg', 'rb')
    await bot.send_photo(callback_query.from_user.id, photo)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете доступ', reply_markup=kb.access_user_1)


# меняем уровень доступа на разрешён
@dp.callback_query_handler(lambda c: c.data == 'user_on_1')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
    UPDATE
        users
    SET
        access = "True"
    WHERE
        name = 'user_1'
    """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ предоставлен!✅', reply_markup=kb.main_menu)


# меняем уровень доступа на запрещён
@dp.callback_query_handler(lambda c: c.data == 'user_off_1')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
        UPDATE
            users
        SET
            access = "False"
        WHERE
            name = 'user_1'
        """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ закрыт!❌', reply_markup=kb.main_menu)


# Блок для пользователя user_2
@dp.callback_query_handler(lambda c: c.data == 'user_2')
async def process_callback_button(callback_query: types.CallbackQuery):
    photo = open(f'{persons_path}/user_2/user_2.jpg', 'rb')
    await bot.send_photo(callback_query.from_user.id, photo)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете доступ', reply_markup=kb.access_user_2)


# меняем уровень доступа на разрешён
@dp.callback_query_handler(lambda c: c.data == 'user_on_2')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
        UPDATE
            users
        SET
            access = "True"
        WHERE
            name = 'user_2'
        """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ предоставлен!✅', reply_markup=kb.main_menu)


# меняем уровень доступа на запрещён
@dp.callback_query_handler(lambda c: c.data == 'user_off_2')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
        UPDATE
            users
        SET
            access = "False"
        WHERE
            name = 'user_2'
        """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ закрыт!❌', reply_markup=kb.main_menu)


# Блок для пользователя user_3
@dp.callback_query_handler(lambda c: c.data == 'user_3')
async def process_callback_button(callback_query: types.CallbackQuery):
    photo = open(f'{persons_path}/user_3/user_3.jpg', 'rb')
    await bot.send_photo(callback_query.from_user.id, photo)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете доступ', reply_markup=kb.access_user_3)


@dp.callback_query_handler(lambda c: c.data == 'user_on_3')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
            UPDATE
                users
            SET
                access = "True"
            WHERE
                name = 'user_3'
            """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ предоставлен!✅', reply_markup=kb.main_menu)


# меняем уровень доступа на запрещён
@dp.callback_query_handler(lambda c: c.data == 'user_off_3')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
            UPDATE
                users
            SET
                access = "False"
            WHERE
                name = 'user_3'
            """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ закрыт!❌', reply_markup=kb.main_menu)


# Блок для пользователя user_4
@dp.callback_query_handler(lambda c: c.data == 'user_4')
async def process_callback_button(callback_query: types.CallbackQuery):
    photo = open(f'{persons_path}/user_4/user_4.jpg', 'rb')
    await bot.send_photo(callback_query.from_user.id, photo)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете доступ', reply_markup=kb.access_user_4)


# меняем уровень доступа на разрешён
@dp.callback_query_handler(lambda c: c.data == 'user_on_4')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
      UPDATE
          users
      SET
          access = "True"
      WHERE
          name = 'User_4'
      """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ предоставлен!✅', reply_markup=kb.main_menu)


# меняем уровень доступа на запрещён
@dp.callback_query_handler(lambda c: c.data == 'user_off_4')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    update_post_description = """
        UPDATE
            users
        SET
            access = "False"
        WHERE
            name = 'user_4'
        """
    sql.execute_query(connection, update_post_description)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Доступ закрыт!❌', reply_markup=kb.main_menu)


# Генерация случайных одноразовых гостевых жестов
@dp.callback_query_handler(lambda c: c.data == 'Guest')
async def process_callback_button(callback_query: types.CallbackQuery):
    guest_gesture = (randrange(1, 5))
    if guest_gesture == 1:
        await bot.send_message(callback_query.from_user.id, 'Используйте этот жест для входа️')
        await bot.send_message(callback_query.from_user.id, '🤟')
        update_post_description = """
            UPDATE
                users
            SET
                access = "True"
            WHERE
                name = 'Guest1'
            """
        sql.execute_query(connection, update_post_description)

    if guest_gesture == 2:
        await bot.send_message(callback_query.from_user.id, 'Используйте этот жест для входа️')
        await bot.send_message(callback_query.from_user.id, '✌️')
        update_post_description = """
            UPDATE
                users
            SET
                access = "True"
            WHERE
                name = 'Guest2'
            """
        sql.execute_query(connection, update_post_description)
    if guest_gesture == 3:
        await bot.send_message(callback_query.from_user.id, 'Используйте этот жест для входа️')
        await bot.send_message(callback_query.from_user.id, '🤙')
        update_post_description = """
            UPDATE
                users
            SET
                access = "True"
            WHERE
                name = 'Guest3'
            """
        sql.execute_query(connection, update_post_description)
    if guest_gesture == 4:
        await bot.send_message(callback_query.from_user.id, 'Используйте этот жест для входа️')
        await bot.send_message(callback_query.from_user.id, '☝️')
        update_post_description = """
            UPDATE
                users
            SET
                access = "True"
            WHERE
                name = 'Guest4'
            """
        sql.execute_query(connection, update_post_description)


# Ловим текст от пользователя: Запрашиваем пароль для Админстратора
@dp.message_handler()
async def echo_message(msg: types.Message):
    text = msg.text
    if text == bot_password:
        await bot.send_message(msg.from_user.id, 'Добро пожаловать', reply_markup=kb.main_menu)
    else:
        await bot.send_message(msg.from_user.id, 'Неверный пароль, попробуйте еще раз!')

# Машина состояний, улавливает имя и фамилию от пользователя и записывает  в storage
@dp.message_handler(state = ud.user_name)
async def load_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await ud.next()
    await msg.reply('Пришлите фото')

# Машина состояний, улавливает фото от пользователя и создает папку с именем пользователя.
@dp.message_handler(content_types = ['photo'], state = ud.user_photo_path)
async def load_photo(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name']
        os.mkdir(f'{persons_path}/{name}')
        await msg.photo[-1].download(f'{persons_path}/{name}/{name}.jpg')
        await msg.reply('Подтвердите добавление пользователя',reply_markup = kb.add_user_button)

if __name__ == '__main__':
    executor.start_polling(dp)