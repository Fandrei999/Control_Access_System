import face_recognition
import pickle
import os
from config import persons_path, pickle_path
from queries import create_connection, execute_query, execute_read_query
import cv2
from datetime import datetime

# обучение модкли распознавания лиц
def train_model_by_img():

    names_arr = os.listdir(persons_path) # создаём список пользователей
    data = {name: 0 for name in names_arr}

    for name in names_arr:
        known_encodings = []
        images = os.listdir(f'{persons_path}{name}')

        for (i, image) in enumerate(images):
            face_img = face_recognition.load_image_file(f'{persons_path}{name}/{image}')
            face_enc = face_recognition.face_encodings(face_img)[0]

            if len(known_encodings) == 0:
                known_encodings.append(face_enc)
            else:
                for item in range(0, len(known_encodings)):
                    result = face_recognition.compare_faces([face_enc], known_encodings[item])

                    if result[0]:
                        known_encodings.append(face_enc)
                        break
                    else:
                        break

        data[name] = known_encodings
        print(f'Пользователь {name} добавлен')

    with open(f'{pickle_path}faces_encodings.pickle', 'wb') as file:
        file.write(pickle.dumps(data))

    return 'Модель обучена'

# детектирование лица
def detect_face(img, image):
    names_arr = os.listdir(persons_path)  # список пользователей
    locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, locations)
    for face_encoding, face_location in zip(encodings, locations):  # ищем лицо на видео
        connection = create_connection()
        for name in names_arr:  # итерируемся по пользователям

            data = pickle.loads(open(pickle_path,
                                     "rb").read())  # словарь с привязкой пользователя к фото

            select_users = f"SELECT access FROM users WHERE name = '{name}'"  # запрос в БД
            user_result = execute_read_query(connection, select_users)

            result = face_recognition.compare_faces(data[name], face_encoding)  # тут сравниваем лицо на фото с нашей бд

            if False in result:  # если соответствия нет - продолжаем цикл (переходим к следующему пользователю)
                continue

            elif user_result[0][0] == 'True':  # проверяем, разрешён ли пользователю вход

                create_log = f"""
                INSERT INTO
                    `report` (`name`, `time`, `access`)
                VALUES
                    ('{name}', '{str(datetime.now().strftime("%H:%M %d.%m"))}', '');
                """
                execute_query(connection, create_log)
                left_top = (face_location[3] * 5, face_location[0] * 5)
                right_bottom = (face_location[1] * 5, face_location[2] * 5)
                color = [0, 255, 0]
                cv2.rectangle(image, left_top, right_bottom, color, 2)
                cv2.putText(image, name,
                            (face_location[3] * 5 + 30, face_location[2] * 5 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return True

            else:
                left_top = (face_location[3] * 5, face_location[0] * 5)
                right_bottom = (face_location[1] * 5, face_location[2] * 5)
                color = [0, 0, 255]
                cv2.rectangle(image, left_top, right_bottom, color, 2)
                cv2.putText(image, 'access denied',
                            (face_location[3] * 5 + 30, face_location[2] * 5 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return False
