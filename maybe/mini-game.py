# импортируем библиотеки
import json
import logging
import random

# Импортируем нужные файлы
from dialogs import *
# библиотека, которая нам понадобится для работы с JSON
from flask import Flask, request
# Импортируем нужные файлы
from images import *

# создаём приложение
# мы передаём __name__, в нём содержится информация,
# в каком модуле мы находимся.
# В данном случае там содержится '__main__',
# так как мы обращаемся к переменной из запущенного модуля.
# если бы такое обращение, например, произошло внутри модуля logging,
# то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# создаём словарь, в котором ключ — название города, а значение — массив,
# где перечислены id картинок.

ATRACTIONS = {
    'эрмитаж': HERMITAGE,
    'белый дом': WHITE_HOUSE,
    'кремль': KREMLIN,
}

# создаём словарь, где для каждого пользователя мы будем хранить его имя
sessionStorage = {}


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    logging.info('Request: %r', request.json)
    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи библиотеки json
    # преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(response, request.json)

    logging.info('Response: %r', response)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO, то пытаемся получить город(araction), если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('araction', None)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def handle_dialog(res, req):
    try:
        user_id = req['session']['user_id']
        buttons = [{
            'title': 'Помощь',
            'hide': False
        }]
        res['response']['buttons'] = buttons
        if 'помощь' in req['request']['nlu']['tokens']:
            res['response']['text'] = HELP
        else:
            if req['session']['new']:
                # Это новый пользователь.
                # Инициализируем сессию и поприветствуем его.
                res['response']['text'] = GREETING
                sessionStorage[user_id] = {
                    'first_name': None,  # здесь будет храниться имя
                    'game_started': False  # здесь информация о том, что пользователь начал игру.
                    # По умолчанию False
                }
                return
            # Сюда дойдем только, если пользователь не новый,
            # и разговор с Алисой уже был начат
            # Обрабатываем ответ пользователя.
            if sessionStorage[user_id]['first_name'] is None:
                first_name = get_first_name(req)
                if first_name is None:
                    res['response']['text'] = REPEAT_PLEASE
                else:
                    sessionStorage[user_id]['first_name'] = first_name
                    # создаём пустой массив, в который будем записывать города,
                    # которые пользователь уже отгадал
                    sessionStorage[user_id]['guessed_attractions'] = []
                    # как видно из предыдущего навыка, сюда мы попали, потому что пользователь
                    # написал своем имя.
                    # Предлагаем ему сыграть и два варианта ответа "Да" и "Нет".
                    res['response']['text'] = NICE_TO_MEET_YOU.format(first_name.title())
                    res['response']['buttons'] += [
                        {
                            'title': 'Да',
                            'hide': True
                        },
                        {
                            'title': 'Нет',
                            'hide': True
                        }
                    ]
            else:
                # У нас уже есть имя, и теперь мы ожидаем ответ на предложение сыграть.
                # В sessionStorage[user_id]['game_started'] хранится True или False в
                # зависимости от того,
                # начал пользователь игру или нет.
                if not sessionStorage[user_id]['game_started']:
                    # игра не начата, значит мы ожидаем ответ на предложение сыграть.
                    if req["request"]["command"] == SHOW_ATTRACTION:
                        pass
                    if 'да' in req['request']['nlu']['tokens']:
                        # если пользователь согласен, то проверяем не отгадал ли он уже все города.
                        # По схеме можно увидеть, что здесь окажутся и пользователи,
                        # которые уже отгадывали города
                        if len(sessionStorage[user_id]['guessed_attractions']) == 3:
                            # если все три города отгаданы, то заканчиваем игру
                            res['response']['text'] = YOU_WIN_MINIGAME
                            res['end_session'] = True
                        else:
                            # если есть неотгаданные города, то продолжаем игру
                            sessionStorage[user_id]['game_started'] = True
                            # номер попытки, чтобы показывать фото по порядку
                            sessionStorage[user_id]['attempt'] = 1
                            # функция, которая выбирает город для игры и показывает фото
                            play_game(res, req)
                    elif 'нет' in req['request']['nlu']['tokens']:
                        res['response']['text'] = 'Ну и ладно!'
                        res['end_session'] = True
                    else:
                        if req["request"]["command"] != SHOW_ATTRACTION:
                            res['response']['text'] = I_DO_NOT_UNDERSTAND
                            res['response']['buttons'] += [
                                {
                                    'title': 'Да',
                                    'hide': True
                                },
                                {
                                    'title': 'Нет',
                                    'hide': True
                                }
                            ]
                        else:
                            res['response']['text'] = PLAY_ANOTHER
                            res['response']['buttons'] = [
                                {
                                    'title': 'Да',
                                    'hide': True
                                },
                                {
                                    'title': 'Нет',
                                    'hide': True
                                }
                            ]
                else:
                    play_game(res, req)
    except Exception as e:
        res['response']['text'] = "Ошибка: {}".format(e)


def play_game(res, req):
    try:
        user_id = req['session']['user_id']
        attempt = sessionStorage[user_id]['attempt']
        if attempt == 1:
            # если попытка первая, то случайным образом выбираем город для гадания
            araction = random.choice(list(ATRACTIONS))
            # выбираем его до тех пор пока не выбираем город, которого нет в
            # sessionStorage[user_id]['guessed_attractions']
            while araction in sessionStorage[user_id]['guessed_attractions']:
                araction = random.choice(list(ATRACTIONS))
            # записываем город в информацию о пользователе
            sessionStorage[user_id]['araction'] = araction
            # добавляем в ответ картинку
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = WHAT_CITY
            res['response']['card']['image_id'] = ATRACTIONS[araction][attempt - 1]
            res['response']['text'] = LET_S_PLAY
        else:
            # сюда попадаем, если попытка отгадать не первая
            araction = sessionStorage[user_id]['araction']
            # проверяем есть ли правильный ответ в сообщение
            if get_city(req) == araction:
                # если да, то добавляем город к sessionStorage[user_id]['guessed_attractions'] и
                # отправляем пользователя на второй круг. Обратите внимание на этот шаг на схеме.
                res['response']['text'] = GOOD_PLAY_ANOTHER
                URL = "https://yandex.ru/maps/?mode=search&text={}"
                res['response']['buttons'].append({"title": SHOW_ATTRACTION,
                                                   "url": URL.format(araction),
                                                   "hide": True})
                sessionStorage[user_id]['guessed_attractions'].append(araction)
                sessionStorage[user_id]['game_started'] = False
                return
            else:
                # если нет
                if attempt == 3:
                    # если попытка третья, то значит, что все картинки мы показали.
                    # В этом случае говорим ответ пользователю,
                    # добавляем город к sessionStorage[user_id]['guessed_attractions'] и
                    # отправляем его на второй круг.
                    res['response']['text'] = YOU_TRY.format(araction.title())
                    sessionStorage[user_id]['game_started'] = False
                    sessionStorage[user_id]['guessed_attractions'].append(araction)
                    return
                else:
                    # иначе показываем следующую картинку
                    res['response']['card'] = {}
                    res['response']['card']['type'] = 'BigImage'
                    res['response']['card']['title'] = TAKE_TWO
                    res['response']['card']['image_id'] = ATRACTIONS[araction][attempt - 1]
                    res['response']['text'] = INCCORECT_ANSWER
        # увеличиваем номер попытки доля следующего шага
        sessionStorage[user_id]['attempt'] += 1
    except Exception as e:
        res['response']['text'] = "Ошибка: {}".format(e)


if __name__ == '__main__':
    app.run()
