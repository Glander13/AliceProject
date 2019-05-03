import json
import logging

import requests
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


# перевод текста
def translate(lang, text):
    # url переводчика
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    # мой API-ключ от api яндекс.переводчика
    key = 'trnsl.1.1.20190503T052928Z.26c6d99725b2e11f.2452f176b372b7feef2586e78e1cc3bdeac67e85'
    translation = requests.get(url, data={'key': key, 'text': text, 'lang': lang}).json()['text'][0]
    return translation


# новая игра (игра занова)
def new_game(user):
    user.name = None
    user.scene = 1
    user.scene_4_from_scene = None
    user.read_thirst_paper = False
    user.read_boxpaper = False
    user.take_box = False
    user.keys_for_box = False
    user.opened_box = False
    user.seen_images = False
    user.morse = False
    user.chester = False
    user.read_warning = False
    user.thirst_paper = False
    user.second_paper = False
    user.third_paper = False
    user.had_readen_paper = False
    user.some_paper = False
    user.safe_opened = False
    user.find_gas_mask = False
    user.ready_to_die = False
    user.game_over = False
    user.win = False
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
    res.addButton(di.HELP)
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
        elif user.scene == 8:
            FINAL_SCENE(res, req, user, command)
    elif user.game_over:
        if command == di.NEW_GAME:
            res.addAnswer(di.HELLO)
            new_game(user)
            return
    elif user.win:
        if command == di.NEW_GAME:
            res.addAnswer(di.HELLO)
            new_game(user)
            return


# несуществующая команда
def error_command(res, command, scene_command):
    if command == di.HELP:
        res.addAnswer(di.HELP_TEXT)
    if command and command != di.HELP:
        res.addAnswer(di.I_DO_NOT_UNDERSTAND)
    res.addAnswer(scene_command)
    res.addAnswer(di.YOUR_ACTIONS + "\n")


# обработчик 1 сцены
def SCENE_1(res, req, user, command):
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_1)
        res.addImage(di.SCENE_1, Image.SCENE_1)
        # если у игрока ещё нет записки со шкатулкой
        if not user.read_boxpaper:
            # пусть он проверит стол и найдет эти вещи
            res.addButton(di.CHECK_TABLE)
        # если игрок прочитал записку и не взял шкатулку
        if not user.opened_box and user.read_boxpaper:
            # предлагаем взять её
            res.addButton(di.GET_BOX)
    elif command == di.RETURN:
        res.addAnswer(di.YOU_RETURNED)
    elif command == di.CHECK_TABLE and not user.read_boxpaper:
        # нашел записку и шкатулку
        res.addAnswer(di.SOMETHING_INTERESTING)
        # прочитать записку?
        res.addButton(di.READ_PAPER)
    elif command == di.READ_PAPER and not user.read_boxpaper:
        # показать текст записки
        res.addAnswer(di.TEXT_FOR_BOX)
        # игрок прочел записку
        user.read_boxpaper = True
        # если игрок прочел записку и не нашел ключи от шкатулки,
        if not user.opened_box and user.read_boxpaper and not user.keys_for_box:
            # предлагаем взять шкатулку
            res.addButton(di.GET_BOX)
    elif command == di.GET_BOX and not user.opened_box and user.read_boxpaper:
        # вы взяли шкатулку
        res.addAnswer(di.YOU_GET_BOX)
        user.take_box = True
        # если игрок нашел ключи
        if user.keys_for_box:
            # предлагаем открыть шкатулку
            res.addButton(di.TRY_OPEN_BOX)
    # игрок решил открыть шкатулку
    elif command == di.TRY_OPEN_BOX and not user.third_paper and not user.opened_box:
        # и получил послание
        res.addAnswer(di.MESSAGE_FROM_BOX)
        user.third_paper = True
        user.opened_box = True
    elif command == di.GO_FURTHER:
        SCENE_2(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_1)
    user.scene = 1
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
        # если игрок еще не рассматривал фотографии
        if not user.seen_images:
            # предлагаем это сделать
            res.addButton(di.CONSIDER_PICTERS)
    elif command == di.CONSIDER_PICTERS and not user.seen_images:
        # говорим, то чтобы он проанализировал то, что было сказано раньше
        res.addAnswer(di.ANALISE_PICTERS)
        user.seen_images = True
    # если игрок пытается разгадать морзе
    elif command == di.TRY_UNDERSTAND_IT_YOURSELF and not user.morse:
        # то, к сожаленью у него не получается
        res.addAnswer(di.TRYING)
    # если же воспользуется Алисой
    elif command == di.USE_ALICE and not user.morse:
        # то получит расшифровку
        res.addAnswer(di.USING_ALICE)
        user.thirst_paper = True
        user.morse = True
    elif command == di.RETURN:
        SCENE_2(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_3)
    # если код морзе ещё не разгадан, но игрок уже посмотрел фотографии
    if not user.morse and user.seen_images:
        # предлагаем ему попытаться понять это самостоятельно
        res.addButton(di.TRY_UNDERSTAND_IT_YOURSELF)
        # или воспользоваться Алисой
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
    elif command == di.ASK_ALICE_ABOUT_PORTRAIT and not user.chester:
        res.addAnswer(di.ALAN_CHESTER)
        user.second_paper = True
        user.chester = True
    elif command == di.ANALISE_PORTRAIT:
        # если игрок не знает кьо изображен на портрете
        if not user.chester:
            # говорим ему это
            res.addAnswer(di.WHO_IS)
            # и предлагаем ему спросить у Алисы
            res.addButton(di.ASK_ALICE_ABOUT_PORTRAIT)
        # иначе
        else:
            # говорим кто это
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
        # если игрок не прочел предупреждение
        if not user.read_warning:
            # предлагаем сделать это
            res.addButton(di.READ_WARNING)
        # открыть сейф?
        # res.addButton(di.TRY_OPEN_SAFE)
    elif command == di.TRY_OPEN_SAFE:
        # введите код
        res.addAnswer(di.INPUT_THE_CODE)
    # если код верный
    elif command == di.CODE_FOR_SAFE and user.thirst_paper and user.second_paper \
            and user.third_paper and not user.safe_opened:
        res.addAnswer(di.YOU_OPENED_SAFE)
        user.safe_opened = True
    elif command == di.RETURN:
        SCENE_4(res, req, user, None, user.scene_4_from_scene)
        return
    elif command == di.READ_WARNING and not user.read_warning:
        res.addAnswer(di.TEXT_WARNING_ON_ENGLISH)
        # перевести предупреждение на русский?
        res.addButton(di.TRANSLATE_INTO_RUSSIAN)
    # если игрок перевел
    elif command == di.TRANSLATE_INTO_RUSSIAN and not user.read_warning:
        res.addAnswer(translate("en-ru", di.TEXT_WARNING_ON_ENGLISH))
        user.read_warning = True
    # если игрок решился пойти в опасную зону без противогаза
    elif command == di.GO_TO_NOT_SAFE_ZONE:
        res.addAnswer(di.ARE_YOU_SURE)
        # предлагаем ему последний выбор
        res.addButton(di.I_AM_SURE)
        res.addButton(di.NO)
    # игрок проиграл
    elif command == di.I_AM_SURE and not user.game_over:
        res.addAnswer(di.DEATH_SCENE)
        user.game_over = True
        user.end = True
        # предлагаем начать занова
        res.addButton(di.NEW_GAME)
    elif command == di.NO:
        res.addAnswer(di.YOU_RIGHT)
    elif command == di.GO_TO_THE_LEFT:
        SCENE_6(res, req, user, None)
        return
    elif command == di.GO_TO_THE_RIGHT:
        SCENE_7(res, req, user, None)
        return
    elif command == di.USE_GAS_MASK:
        FINAL_SCENE(res, req, user, None)
        res.addAnswer(di.FINAL)
        return
    elif command == di.TAKE_PAPER:
        res.addAnswer(di.TEXT_OF_PAPER)
        user.had_readen_paper = True
    elif command == di.HELP:
        res.addAnswer(di.HELP_TEXT)
    else:
        if command:
            res.addAnswer(di.INCORRECT_CODE_OR_CMD)
        res.addAnswer(di.SCENE_5)
        res.addAnswer(di.YOUR_ACTIONS + "\n")
    if not user.end:
        if user.thirst_paper and user.second_paper and user.third_paper \
                and not user.had_readen_paper:
            res.addAnswer(di.OMG_YOU_FIND_ALL_PAPERS)
            res.addButton(di.TAKE_PAPER)
        res.addButton(di.TRY_OPEN_SAFE)
        res.addButton(di.GO_TO_THE_LEFT)
        res.addButton(di.GO_TO_NOT_SAFE_ZONE)
        res.addButton(di.GO_TO_THE_RIGHT)
        res.addButton(di.SHOW_SCENE)
        res.addButton(di.RETURN)
        if user.find_gas_mask:
            res.addButton(di.USE_GAS_MASK)


def SCENE_6(res, req, user, command):
    user.scene = 6
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_6)
        res.addImage(di.SCENE_6, Image.SCENE_6)
        # если у игрока нет ключей для шкатулки
        if not user.keys_for_box:
            # пусть посмотрит в шкафу
            res.addButton(di.LOOK_WARDROBE)
        if user.keys_for_box and user.take_box and not user.opened_box:
            res.addButton(di.TRY_OPEN_BOX)
    elif command == di.LOOK_WARDROBE and not user.keys_for_box:
        # вы нашли ключи от шкатулки
        res.addAnswer(di.LOOKING_WARDROBE)
        user.keys_for_box = True
        # если игрок ещё не открыл шкатулку и она у него есть
        if not user.opened_box and user.take_box:
            res.addButton(di.TRY_OPEN_BOX)
    elif command == di.TRY_OPEN_BOX and user.keys_for_box and user.take_box and not user.opened_box:
        res.addAnswer(di.MESSAGE_FROM_BOX)
        user.third_paper = True
        user.opened_box = True
    elif command == di.RETURN:
        SCENE_5(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_6)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)


def SCENE_7(res, req, user, command):
    user.scene = 7
    if command == di.SHOW_SCENE:
        res.addAnswer(di.SCENE_7)
        res.addImage(di.SCENE_7, Image.SCENE_7)
        # если игрок не нашел газовую маску и сейф открыт
        if not user.find_gas_mask and user.safe_opened:
            # пусть поищет в столах
            res.addButton(di.TRY_OPEN_TABELS)
    elif command == di.LOOK_WARDROBE:
        res.addAnswer(di.YOU_FIND_NEW_PAPER)
        res.addButton(di.READ_PAPER)
    # записка, объединяющая остальные
    elif command == di.READ_PAPER and not user.some_paper:
        res.addAnswer(di.USE_IT_WISELY)
        user.some_paper = True
    elif command == di.TRY_OPEN_TABELS and not user.find_gas_mask and user.safe_opened:
        res.addAnswer(di.YOU_FIND_GAS_MASK)
        res.addButton(di.READ_PAPER)
        user.find_gas_mask = True
    elif command == di.RETURN:
        SCENE_5(res, req, user, None)
        return
    else:
        error_command(res, command, di.SCENE_7)
    res.addButton(di.SHOW_SCENE)
    res.addButton(di.RETURN)


def FINAL_SCENE(res, req, user, command):
    user.scene = 8
    if command == di.RUSSIA and not user.end:
        res.addAnswer(di.RUSSIAN)
        user.end = True
        user.win = True
        # предлагаем начать занова
        res.addButton(di.NEW_GAME)
    elif command == di.USA and not user.game_over:
        res.addAnswer(di.AMERICAN)
        user.game_over = True
        user.end = True
        # предлагаем начать занова
        res.addButton(di.NEW_GAME)
    else:
        error_command(res, command, di.SCENE_7)
    if not user.end:
        res.addButton(di.RUSSIA)
        res.addButton(di.USA)
