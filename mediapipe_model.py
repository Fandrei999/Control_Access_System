import mediapipe as mp
import cv2

p = [0 for i in range(21)]              # создаем массив из 21 ячейки для хранения высоты каждой точки
finger = [0 for i in range(5)]          # создаем массив из 5 ячеек для хранения положения каждого пальца
mpHands = mp.solutions.hands            # подключаем раздел распознавания рук
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.5)                 # создаем объект класса "руки"
mpDraw = mp.solutions.drawing_utils     # подключаем инструменты для рисования

def distance(point1, point2): #функция определения дистанции между точками на руке
    return abs(point1 - point2)

def detect_hand(image, img):
    results = hands.process(img)
    if results.multi_hand_landmarks:                            # если обнаружили точки руки
        for handLms in results.multi_hand_landmarks:            # получаем координаты каждой точки

            # при помощи инструмента рисования проводим линии между точками
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

            for id, point in enumerate(handLms.landmark):
            # получаем размеры изображения с камеры и масштабируем
                width, height, color = image.shape
                width, height = int(point.x * height), int(point.y * width)

                p[id] = height           # заполняем массив высотой каждой точки

                if id == 8:              # выбираем нужную точку
                                        # рисуем нужного цвета кружок вокруг выбранной точки
                    cv2.circle(image, (width, height), 8, (51, 255, 255), cv2.FILLED)
                if id == 12:
                    cv2.circle(image, (width, height), 8, (255, 102, 255), cv2.FILLED)
                if id == 4:
                    cv2.circle(image, (width, height), 8, (0, 51, 255), cv2.FILLED)
                if id == 16:
                    cv2.circle(image, (width, height), 8, (255, 204, 0), cv2.FILLED)
                if id == 20:
                    cv2.circle(image, (width, height), 8, (204, 255, 0), cv2.FILLED)

            distanceGood = distance(p[0], p[5]) + (distance(p[0], p[5])/2)
            # заполняем массив 1 (палец поднят) или 0 (палец сжат)
            finger[0] = 1 if distance(p[4], p[17]) > distanceGood else 0
            finger[1] = 1 if distance(p[0], p[8]) > distanceGood else 0
            finger[2] = 1 if distance(p[0], p[12]) > distanceGood else 0
            finger[3] = 1 if distance(p[0], p[16]) > distanceGood else 0
            finger[4] = 1 if distance(p[0], p[20]) > distanceGood else 0

                        # готовим сообщение для отправки
            msg = ''
            # 0 - большой палец, 1 - указательный, 2 - средний, 3 - безымянный, 4 - мизинец
            # жест "коза" - 01001
            if (finger[0]) and finger[1] and not (finger[2]) and not (finger[3]) and finger[4]:
                return 'Guest1'
            if not finger[0] and (finger[1]) and (finger[2]) and not (finger[3]) and not (finger[4]):
                return 'Guest2'
            if (finger[0]) and not finger[1] and not finger[2] and not(finger[3]) and (finger[4]):
                return 'Guest3'
            if not(finger[0]) and finger[1] and not(finger[2]) and not(finger[3]) and not(finger[4]):
                return 'Guest4'
            else:
                return ''