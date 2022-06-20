from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


#Кнопки Главного меню
report = InlineKeyboardButton('Отчёт ', callback_data='A')
users_access = InlineKeyboardButton('Управление персоналом', callback_data='B')
guest_access = InlineKeyboardButton('Разовый доступ', callback_data='Guest')
main_menu = InlineKeyboardMarkup(row_width=1).add(report,users_access,guest_access)


#Кнопки второстепенного меню
sec_menu_user_1 = InlineKeyboardButton('user_1', callback_data='user_2')
sec_menu_user_2 = InlineKeyboardButton('user_2', callback_data='user_1')
sec_menu_user_3 = InlineKeyboardButton('user_3', callback_data='user_3')
sec_menu_user_4 = InlineKeyboardButton('user_4', callback_data='user_4')
add_new_user = InlineKeyboardButton('Добавить нового пользователя', callback_data='newp')
return_button = InlineKeyboardButton('Назад ↩️',callback_data='back')
secondary_menu = InlineKeyboardMarkup(row_width=1).add(sec_menu_user_1,sec_menu_user_2,sec_menu_user_3,sec_menu_user_4,add_new_user,return_button)

#Добавление пользователя в модель
add_user = InlineKeyboardButton('Добавить', callback_data='add_user')
add_user_button = InlineKeyboardMarkup(row_width=1).add(add_user)


#Кнопки управления уровнем доступа пользователей
access_accept_1 = InlineKeyboardButton('Открыть доступ✅', callback_data='user_on_1')
access_denied_1 = InlineKeyboardButton('Закрыть доступ❌', callback_data='user_off_1')
access_user_1 = InlineKeyboardMarkup(row_width=1).add(access_accept_1,access_denied_1)

access_accept_2 = InlineKeyboardButton('Открыть доступ✅', callback_data='user_on_2')
access_denied_2 = InlineKeyboardButton('Закрыть доступ❌', callback_data='user_off_2')
access_user_2 = InlineKeyboardMarkup(row_width=1).add(access_accept_2,access_denied_2)

access_accept_3 = InlineKeyboardButton('Открыть доступ✅', callback_data='user_on_3')
access_denied_3 = InlineKeyboardButton('Закрыть доступ❌', callback_data='user_off_3')
access_user_3 = InlineKeyboardMarkup(row_width=1).add(access_accept_3,access_denied_3)

access_accept_4 = InlineKeyboardButton('Открыть доступ✅', callback_data='user_on_4')
access_denied_4 = InlineKeyboardButton('Закрыть доступ❌', callback_data='user_off_4')
access_user_4 = InlineKeyboardMarkup(row_width=1).add(access_accept_4,access_denied_4)



