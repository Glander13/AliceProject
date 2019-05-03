# Файл, хранящий тексты для диалога
# Примечание: фразы, содержащие только буквы нижнего регистра являются текстами для команд (кнопок)
class Dialogs:
    # Приветствие
    HELLO = "Привет! Назови свое имя!"
    GREETING = "Приятно познакомиться, {}! Давай поиграем! Вы являетесь двойным агентом России и" \
               " США и вам удалось обмануть Америку. Но Вы не знаете английский язык, Вам " \
               "помогает Алиса. Вам поручили важную миссию по спасению мира. Итак, Вы попали " \
               "в Белый дом. По нашим достоверным источникам пришла информация, что в доме " \
               "президента произошел взрыв ядовитых газов. Президент был быстро эвакуирован с" \
               " места происшествия, но нейтрализовать газ пока не невозможно. Однако, " \
               "там остались важные документы. Доставить эти документы можете только вы, наш " \
               "главный и секретный агент. Итак, ваша задача, агент {} - вам нужно доставить " \
               "эти документы. Как вы помните, ваш уникальный костюм способен выдержать любые " \
               "нагрузки, даже взрыв ядерной бомбы. Однако, костюм не сможет закрыть ваше лицо, " \
               "поэтому вы должны найти противогаз в Белом доме. Удачи солдат!"

    REPEAT_PLEASE = "Не расслышала имя. Повтори, пожалуйста!"

    # Общее для сцен
    I_DO_NOT_UNDERSTAND = "Не поняла ответа! Пожалуйста, повторите еще раз."
    SHOW_SCENE = 'покажи комнату'
    YOUR_ACTIONS = "\nВаши действия:"
    GO_FURTHER = "пойти дальше"
    GO = "Вы перешли "
    YOU_RETURNED = "Вы успешно вернулись назад."
    RETURN = "вернуться назад"

    # Сцена 1
    SCENE_1 = "Входная комната."
    # NOTHING = "Что-ж, ничего кроме ненужных бумаг вы там не нашли"
    # NOTHING_2 = "Вы уже смотрели эту комнату, и ничего не нашли"
    CHECK_TABLE = "обыскать стол"
    SOMETHING_INTERESTING = "Хмм... Что-то интересное: вы нашли записку и шкатулку"
    READ_PAPER = "прочесть записку"
    TEXT_FOR_BOX = "Чтобы открыть шкатулку нужен ключик."
    GET_BOX = "взять шкатулку"
    YOU_GET_BOX = "вы взяли шкатулку"

    # Сцена 2
    SCENE_2 = "Лестничный подъем."
    GO_TO_THE_STAND_WITH_PICTS = "подойти к стенду с картинами"

    # Сцена 3
    SCENE_3 = "Картинный стенд."
    CONSIDER_PICTERS = "расмотреть фотогорафии"
    ANALISE_PICTERS = "Вы рассмотрели фотографии и обнаружили на самой старой из них непонятные " \
                      "записи, состоящие из точек и дефисов, нечто очень похожее на код Морзе."
    TRY_UNDERSTAND_IT_YOURSELF = "попытаться понять это самостоятельно"
    TRYING = "Самостоятельно расшифровать это не получилось."
    USE_ALICE = "использовать алису"

    # "Первое" число для кода от сейфа

    USING_ALICE = "Вы сказали Алисе, чтобы она перевела этот код и получили разгаданное " \
                  "послание: 'Просто так ты ничего не получишь, вспомни хотя бы один эпизод из " \
                  "стиха о заливе морском, именно о том, о котором все говорят. Если вспомнил " \
                  "данное место назови ты и число героев в защите, которые там находились. И " \
                  "отними от этого числа три десятка, прибавив четверку. Сделав все эти " \
                  "манипуляции получишь число ты зашифрованное.'"

    # Сцена 4
    SCENE_4 = "Комната с портретом и проходом дальше."
    RETURN_TO_SCENE_2 = "вернуться к лестничному подъему"
    RETURN_TO_SCENE_3 = "вернуться к стенду с картинами"
    ANALISE_PORTRAIT = "расмотреть портрет"
    ASK_ALICE_ABOUT_PORTRAIT = "спросить у алисы кто это"
    WHO_IS = "Хмм... Что-то всплывает в вашей голове. Будто бы вы видели этого человека раннее " \
             "Помойму его звали на 'Ч' или как-то так. Больше вы ничего не вспомнили"
    ALAN_CHESTER = "Это Алан Честер. Согласно русской википедии, 21-й президент Соединённых " \
                   "Штатов Америки с 1881 по 1885, республиканец. Сменил на посту Джеймса Гарфилда " \
                   "после убийства последнего."
    HOW_SAID_ALICE = "как сказала Алиса, это Алан Честер 21-й президент Америки"

    # Сцена 5
    SCENE_5 = "Комната с двумя дверями и сейфом."
    TRY_OPEN_SAFE = "попробовать открыть сейф"
    INPUT_THE_CODE = "введите четырёхзначный код"
    NOTHING = "К сожаленью, у вас ничего не получилось"
    YOU_FIND_GAS_MASK = "вы нашли противогаз и записку"
    GO_TO_THE_LEFT = "пойти налево"
    GO_TO_THE_RIGHT = "пойти направо"
    CODE_FOR_SAFE = "3217"
    YOU_OPENED_SAFE = "Вы успешно открыли сейф. Там лежат: ключ с биркой (на бирке написано: ключ от маленького " \
                      "столика) и деньги."
    TRY_OPEN_TABELS = "попробовать открыть столики ключом из сейфа"
    READ_WARNING = "прочитать предупреждение"
    TEXT_WARNING_ON_ENGLISH = "Attention! There was an accident in the White house with the " \
                              "emission of toxic gases. " \
                              "Turn on the local radio, TV, and listen to the emergency message." \
                              " Give the " \
                              "information to your relatives and neighbors. In this regard, " \
                              "the population living " \
                              "and working in this area must act in accordance with the " \
                              "instructions of the heads of " \
                              "rescue services. Leaving the apartment, working space, you " \
                              "must immediately take " \
                              "identification documents, food (at the rate of two days) put " \
                              "in a sealed container. " \
                              "Turn off gas, electricity, water. In the process of leaving " \
                              "the infected zone to " \
                              "transmit information to other residents. If it is impossible " \
                              "to evacuate, close all " \
                              "Windows and doors, carry out additional sealing of the premises, " \
                              "report by phone 911. " \
                              "Feeling the smell of contaminated air, use to protect the " \
                              "respiratory system tight " \
                              "clothing items, clean material, moistened with water."
    TRANSLATE_INTO_RUSSIAN = "перевести на русский с помощью алисы"
    GO_TO_NOT_SAFE_ZONE = "пойти дальше в незащищенную зону"
    I_AM_SURE = "да, я уверен"
    NO = "нет, не пойду"
    ARE_YOU_SURE = "Вы уверены что хотите пойти? Ваше чутье подсказывает вам что это небезопасно..."
    YOU_RIGHT = "вот и правильно"
    DEATH_SCENE = "Чутье вас предупреждало и не зря. К сожаленью, вы попали в зараженную зону " \
                  "и ... проиграли."
    OMG_YOU_FIND_ALL_PAPERS = "Вдруг, вы обнаружили еще одно послание."
    TAKE_PAPER = "взять и прочитать послание"
    TEXT_OF_PAPER = "Соединив воедино все знания накопленные за пребывание здесь, тебе лишь " \
                    "осталось расставить их " \
                    "в нужном порядке. Помни: первым летят утки, дальше идет нумерованный " \
                    "человек и наконец, число, " \
                    "из стихотворения. Собрав все это вместе, получишь ты код заветный от сейфа."
    USE_GAS_MASK = "надеть и использовать газовую маску"

    # Сцена 6 (налево)
    SCENE_6 = "Комната со многими вещами."
    LOOK_WARDROBE = "посмотреть шкаф"
    LOOKING_WARDROBE = "Вы осмотрели шкаф и нашли там ключи, очень похожие по своей стилю на " \
                       "шкатулку"

    # возможно это могло войти в квест, но все-таки пусть это будет здесь
    # CHECKING_TABLE = "Осмотрев стол вы обнаружили там записку (подписанную как третию)
    # с номерами и точками"
    # YOU_GET_CORDS = "вы получили координаты"
    # URL_FOR_ALICE = "https://yandex.ru/maps/?l=map&ll=-77.035761%2C38.898901&mode=routes
    # &rtext=38.897684%" \
    #                 "2C-77.036540~38.899625%2C-77.036471~38.899698%2C-77.035350~38.898952
    #                 %2C-77.036407~38.898767%" \
    #                 "2C-77.036391~38.898818%2C-77.035377~38.897663%2C-77.036532&rtt=pd
    #                 &source6=wizgeo&" \
    #                 "utm_medium=maps-desktop&utm_source=serp&z=18"

    TRY_OPEN_BOX = "попробовать открыть шкатулку"
    MESSAGE_FROM_BOX = "[прошло какое-то время]... вы перепробовали почти все ключи. " \
                       "Остался только один... И он " \
                       "подошел. Шкатулка изрекает следующее послание: лишь умный человек " \
                       "способен эту загадку разг" \
                       "адать. Летели утки: одна впереди и две позади, одна позади и две " \
                       "впереди, " \
                       "одна между двумя. Сколько их было всего? Не спеши с ответом, подумай!"

    # Сцена 7 (направо)
    SCENE_7 = "Комната со многими вещами."
    YOU_FIND_NEW_PAPER = "вы нашли новую записку"
    USE_IT_WISELY = "Используй это с умом"

    # Финал
    FINAL = "Что-ж вот и подходит к концу наш квест. И я хочу задать вам последний и" \
            " единственный вопрос. " \
            "Вы за кого Россия или США?"
    RUSSIA = "конечно, россия"
    USA = "сша"
    RUSSIAN = "Итак, вы решили выбрать Россию. Вы вернулись на базу своей родины и отдали " \
              "документы своему " \
              "главнокомандующему. Получив эти документы, Россия смогла стать самой великой " \
              "сверхдержавой," \
              "которой еще никогда не была раньше. Вам вручили пожизненную награду за помощь " \
              "Родине. Поздравляем," \
              "солдат. Вы достигли мирового успеха."
    AMERICAN = "Итак, вы решили выбрать США. Вы вернулись на базу Америки. Вас начали " \
               "распрашивать про так вам это удалось и тут вы попались (вы же не знаете " \
               "аншлийского языка). Вас посадили в терьму на пожизненный срок, а также " \
               "объявили самым ужасным предателем за всю историю России."
    # THE END

    # GAME OVER
    GAME_OVER = "К сожаленью, вы проиграли."

    # WIN GAME
    WIN_GAME = "УРА! УРА! Вы прошли этот квест."

    # NEW_GAME
    NEW_GAME = "начать снова"
