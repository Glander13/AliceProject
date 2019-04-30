from flask import request
import logging
import json
from useractions import User
from forresponse import EasyResponse
from images import Image
from dialogs import Dialogs as di

# создаём словарь, где для каждого пользователя мы будем хранить его данные
users = {}


# начало обработки запроса от Алисы
def main():
    # выводим запрос в лог
    logging.info('Request: %r', request.json)
    # создаем начальный ответ
    response = Response(request)
    # обрабатываем запрос
    handle_dialog(response, request.json)
    # логирование
    logging.info('Response: %r', response)
    return json.dumps(response.res)


# обработка запроса
def handle_dialog(res, req):
    # ID пользователя
    user_id = req['session']['user_id']

    # если пользователь новый, то просим представиться
    if req['session']['new'] or user_id not in users:
        res.addText(di.HELLO)
        # создаем класс для хранения информации о пользователе
        user = User()
        # добавляем класс в словарь
        users[user_id] = user
        return

    # находим пользователя
    user = users[user_id]

    # текст команды, которую ввел пользователь
    command = req['request']['original_utterance'].lower()

    # если пользователь еще не представился
    if user.name is None:
        first_name = get_first_name(req)

        if first_name is None:
            res.addText(di.REPEAT_PLEASE)
            return

        user.name = first_name
        res.addText(di.GREETING.format(first_name.title(), first_name.title()))
        command = None

    # обработчик 1 комнаты
    if user.room == 1:
        Greeting_room(res, req, user, command)


# обработчик 1 комнаты
def Greeting_room(res, req, user, command):
    user.room = 1
    if command == di.SHOW_ROOM:
        res.setImage(di.GREETING_ROOM, Image.GREETING_ROOM)
    if command == 'обыскать стол':
        res.addText('Что-ж, ничего.')

    elif command == 'пойти дальше':
        res.addText('скоро сделаю 2ую комнату...')
        # Room2(res, req, user, None)
        return
    else:
        if command:
            res.addText(di.I_DO_NOT_UNDERSTAND)
        res.addText("Входная комната.")
        res.addText("Ваши действия:\n")
    res.addButton(di.SHOW_ROOM)
    if not user.table1:
        res.addText('\nОбыскать стол')
        res.addButton('обыскать стол')
        user.table1 = True
    res.addButton('пойти дальше')


# поиск имени пользователя в запросе пользователя
def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)

# Может пригодится

