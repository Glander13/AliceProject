import json
import logging

from dialogs import Dialogs as di
from flask import request
from forresponse import Response
from images import Image
from useractions import User

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
        res.addAnswer(di.HELLO)
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
            res.addAnswer(di.REPEAT_PLEASE)
            return

        user.name = first_name
        res.addAnswer(di.GREETING.format(first_name.title(), first_name.title()))
        command = None

    # обработчик 1 комнаты
    if user.room == 1:
        SCENE_1(res, req, user, command)
    elif user.room == 2:
        SCENE_2(res, req, user, command)


# обработчик 1 комнаты
def SCENE_1(res, req, user, command):
    user.room = 1
    if command == di.SHOW_ROOM:
        res.addAnswer(di.SCENE_1)
        res.addImage(di.SCENE_1, Image.SCENE_1)
        res.addButton(di.CHECK_TABLE)
    elif command == di.CHECK_TABLE:
        if user.table:
            res.addAnswer(di.NOTHING_2)
        else:
            res.addAnswer(di.NOTHING)
            res.addButton(di.CHECK_TABLE)
            user.table = True
    elif command == di.GO_FURTHER:
        SCENE_2(res, req, user, di.GO_FURTHER)
        return
    else:
        if command:
            res.addAnswer(di.I_DO_NOT_UNDERSTAND)
        res.addAnswer(di.SCENE_1)
        res.addAnswer(di.YOUR_ACTIONS + "\n")
    res.addButton(di.SHOW_ROOM)
    res.addButton(di.GO_FURTHER)


def SCENE_2(res, req, user, command):
    user.room = 2
    if command == di.GO_FURTHER:
        res.addAnswer(di.GO + di.SCENE_2)
    elif command == di.SHOW_ROOM:
        res.addAnswer(di.SCENE_2)
        res.addImage(di.SCENE_2, Image.SCENE_2)
    else:
        if command:
            res.addAnswer(di.I_DO_NOT_UNDERSTAND)
            res.addAnswer(di.SCENE_1)
            res.addAnswer(di.YOUR_ACTIONS + "\n")
    res.addButton(di.SHOW_ROOM)
    # res.addButton


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
