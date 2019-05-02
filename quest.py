import json
import logging

from dialogs import Dialogs as di
from flask import request
from forresponse import Response
from images import Image
from useractions import User

# создаём словарь, хранящий данные пользователя
users = {}


def main():
    logging.info('Request: %r', request.json)
    response = Response(request)
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response.res)


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


# новая игра (игра занова)
def new_game(user):
    user.name = None
    user.scene = 1
    user.scene_4_from_scene = None
    user.table = False
    user.images = False
    user.morse = False
    user.chester = False
    user.ready_to_die = False
    user.game_over = False
    user.end = False


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
    if not user.end:
        if user.scene == 1:
            SCENE_1(res, req, user, command)
        elif user.scene == 2:
            SCENE_2(res, req, user, command)
        elif user.scene == 3:
            SCENE_3(res, req, user, command)
        elif user.scene == 4:
            SCENE_4(res, req, user, command, user.scene_4_from_scene)
        elif user.scene == 5:
            SCENE_5(res, req, user, command)
        elif user.scene == 6:
            SCENE_6(res, req, user, command)
        elif user.scene == 7:
            SCENE_7(res, req, user, command)
    elif user.game_over:
        if command == di.NEW_GAME:
            res.addAnswer(di.HELLO)
            new_game(user)
            return


# несуществующая команда
def error_command(res, command, scene_command):
    if command:
        res.addAnswer(di.I_DO_NOT_UNDERSTAND)
    res.addAnswer(scene_command)
    res.addAnswer(di.YOUR_ACTIONS + "\n")


# обработчик 1 сцены
def SCENE_1(res, req, user, command):
    user.scene = 1
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_1)
        res.addImage(di.SCENE_1, Image.SCENE_1)
        res.addButton(di.CHECK_TABLE)
    elif command == di.RETURN:
        res.addAnswer(di.YOU_RETURNED)

    elif command == di.CHECK_TABLE:
        if user.table:
            res.addAnswer(di.NOTHING_2)
        else:
            res.addAnswer(di.NOTHING)
            res.addButton(di.CHECK_TABLE)
            user.table = True
    elif command == di.GO_FURTHER:
        SCENE_2(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_1)
    res.addButton(di.GO_FURTHER)
    res.addButton(di.SHOW_SCENE)


def SCENE_2(res, req, user, command):
    user.scene = 2
    if command == di.GO_FURTHER:
        SCENE_4(res, req, user, None, 2)
        user.scene_4_from_scene = 2
        return
    elif command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_2)
        res.addImage(di.SCENE_2, Image.SCENE_2)
    elif command == di.RETURN:
        SCENE_1(res, req, user, None)
        return
    elif command == di.GO_TO_THE_STAND_WITH_PICTS:
        SCENE_3(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_2)
    res.addButton(di.GO_FURTHER)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)
    res.addButton(di.GO_TO_THE_STAND_WITH_PICTS)


def SCENE_3(res, req, user, command):
    user.scene = 3
    if command == di.GO_FURTHER:
        SCENE_4(res, req, user, None, 3)
        user.scene_4_from_scene = 3
        return
    elif command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_3)
        res.addImage(di.SCENE_3, Image.SCENE_3)
        if not user.images:
            res.addButton(di.CONSIDER_PICTERS)
    elif command == di.TRY_UNDERSTAND_IT_YOURSELF:
        res.addAnswer(di.TRYING)
    elif command == di.USE_ALICE:
        res.addAnswer(di.USING_ALICE)
        user.morse = True
    elif command == di.CONSIDER_PICTERS:
        res.addAnswer(di.ANALISE_PICTERS)
        user.images = True
    elif command == di.RETURN:
        SCENE_2(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_3)
    if not user.morse and user.images:
        res.addButton(di.TRY_UNDERSTAND_IT_YOURSELF)
        res.addButton(di.USE_ALICE)
    res.addButton(di.GO_FURTHER)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)


def SCENE_4(res, req, user, command, from_scene):
    user.scene = 4
    if command == di.GO_FURTHER:
        SCENE_5(res, req, user, None)
        return
    elif command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_4)
        res.addImage(di.SCENE_4, Image.SCENE_4)
        res.addButton(di.ANALISE_PORTRAIT)
    elif command == di.RETURN:
        if from_scene == 3:
            SCENE_3(res, req, user, None)
            return
        elif from_scene == 2:
            SCENE_2(res, req, user, None)
            return
    elif command == di.RETURN_TO_SCENE_2:
        SCENE_2(res, req, user, None)
        return
    elif command == di.RETURN_TO_SCENE_3:
        SCENE_3(res, req, user, None)
        return
    elif command == di.ASK_ALICE_ABOUT_PORTRAIT:
        res.addAnswer(di.ALAN_CHESTER)
        user.chester = True
    elif command == di.ANALISE_PORTRAIT:
        if not user.chester:
            res.addAnswer(di.WHO_IS)
            res.addButton(di.ASK_ALICE_ABOUT_PORTRAIT)
        else:
            res.addAnswer(di.HOW_SAID_ALICE)
    else:
        error_command(res, command, di.SCENE_4)
    res.addButton(di.GO_FURTHER)
    if from_scene == 3:
        res.addButton(di.RETURN_TO_SCENE_2)
    else:
        res.addButton(di.RETURN_TO_SCENE_3)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)


def SCENE_5(res, req, user, command):
    user.scene = 5
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_5)
        res.addImage(di.SCENE_5, Image.SCENE_5)
    elif command == di.RETURN:
        SCENE_4(res, req, user, None)
        return
    elif command == di.I_AM_SURE:
        res.addAnswer(di.DEATH_SCENE)
        user.game_over = True
        user.end = True
        res.addButton(di.NEW_GAME)
    elif command == di.NO:
        res.addAnswer(di.YOU_RIGHT)
    elif command == di.GO_TO_NOT_SAFE_ZONE:
        res.addAnswer(di.ARE_YOU_SURE)
        res.addButton(di.I_AM_SURE)
        res.addButton(di.NO)
    elif command == di.GO_TO_THE_LEFT:
        SCENE_6(res, req, user, None)
        return
    elif command == di.GO_TO_THE_RIGHT:
        SCENE_7(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_5)
    if not user.end:
        res.addButton(di.GO_TO_THE_LEFT)
        res.addButton(di.GO_TO_NOT_SAFE_ZONE)
        res.addButton(di.GO_TO_THE_RIGHT)
        res.addButton(di.SHOW_SCENE)
        res.addButton(di.RETURN)


def SCENE_6(res, req, user, command):
    user.scene = 6
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_6)
        res.addImage(di.SCENE_6, Image.SCENE_6)
    elif command == di.LOOK_WARDROBE:
        user.keys = True
        res.addAnswer(di.LOOKING_WARDROBE)
    elif command == di.CHECK_TABLE:
        res.addAnswer(di.CHECKING_TABLE)
        res.addButton(di.USE_ALICE, di.URL_FOR_ALICE)
        res.addButton(di.TRY_UNDERSTAND_IT_YOURSELF)
    elif command == di.USE_ALICE:
        user.paper_with_cords = True
        res.addAnswer(di.YOU_GET_CORDS)
    elif command == di.TRY_UNDERSTAND_IT_YOURSELF:
        res.addAnswer(di.TRYING)
    elif command == di.RETURN:
        SCENE_5(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_6)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)
    if not user.paper_with_cords:
        res.addButton(di.CHECK_TABLE)
    if not user.keys:
        res.addButton(di.LOOK_WARDROBE)


def SCENE_7(res, req, user, command):
    user.scene = 7
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_7)
        res.addImage(di.SCENE_7, Image.SCENE_7)
    elif command == di.RETURN:
        SCENE_5(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_7)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)
