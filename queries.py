import mysql.connector
from mysql.connector import Error
from config import host_name, user_name, user_password, db_name, guest_arr, com_port
import time
import serial

my_serial = serial.Serial(com_port, 9600)

# создаём подключение к БД
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print('Подключение к базе успешно')
    except Error as e:
        print(f'Ошибка подключения: {e}')
    return connection

# читаем данные из БД
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'Ошибка подключения: {e}')

# изменяем, добавляем запись в БД
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f'Ошибка подключения: {e}')

# генерация отчёта
def get_report():
    connection = create_connection()
    result = ''
    select_users = "SELECT name, time from report LIMIT 500 OFFSET 1"
    users = execute_read_query(connection, select_users)
    for i in range(len(users)):
        if f'{users[i][0]} - {users[i][1]}' in result:
            continue
        else:
            result += f'{users[i][0]} - {users[i][1]} '
    return result

# команда на открытие двери
def open_door():
    my_serial.write(b'True')
    time.sleep(2)
    pass

# Если активирован случайный жест, меняем его уровень доступа на запрещён
def random_gesture():
    for name in guest_arr:
        connection = create_connection()
        select_users = f'SELECT access FROM users WHERE name = {name}'
        user_result = execute_read_query(connection, select_users)
        if user_result[0][0] == 'True':
            return True, name
    return False, _