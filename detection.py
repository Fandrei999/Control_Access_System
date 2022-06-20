from mediapipe_model import detect_hand
from face_model import detect_face
import cv2
from config import rtsp_stream, http_stream
from queries import open_door, random_gesture, create_connection, execute_query

# добавляем rtsp или http поток с ip камеры
# rtsp_stream = rtsp_stream
# http_stream = http_stream

# по умолчанию работаем с вебкамерой
video = cv2.VideoCapture(0)

flag = False

while True:
    _, image = video.read(0)
    img = cv2.resize(image, (0, 0), None, 0.2, 0.2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    flag, guest_name = random_gesture()
    if flag:
        guest = f'{detect_hand(image, img)}'
        if guest == guest_name:
            cv2.rectangle(image, (1100, 0), (1280, 80), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, 'OPEN', (1100, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1)
            open_door()
            print('Open door with gesture')
            connection = create_connection()
            update_post_description = f"""
            UPDATE
              users
            SET
              access = "False"
            WHERE
              name = '{guest_name}'
            """
            execute_query(connection, update_post_description)
        else:
            cv2.rectangle(image, (1100, 0), (1280, 80), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, 'CLOSE', (1100, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1)
    else:
        if detect_face(img, image):
            cv2.rectangle(image, (1100, 0), (1280, 80), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, 'OPEN', (1100, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1)
            open_door()
            print('Open door with face')
        else:
            cv2.rectangle(image, (1100, 0), (1280, 80), (0, 0, 255), cv2.FILLED)
            cv2.putText(image, 'CLOSE', (1100, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 1)

    cv2.imshow('Access control system', image)

    k = cv2.waitKey(20)
    if k == ord("q"):
        print("Q pressed, closing the app")
        # break

    cv2.destroyAllWindows()
