# Информация о пользователе
class User:
    def __init__(self):

        # имя пользователя
        self.name = None
        # сцена, в которой находится пользователь
        self.scene = 0
        #
        self.greeting_2 = False
        self.greeting_3 = False

        self.ready = False
        # из какой сцены игрок попал в 4 сцену (либо из 2, либо из 3)
        self.scene_4_from_scene = None

        """
        шкатулка
        """
        self.read_thirst_paper = False
        # прочел ли игрок записку о шкатулке?
        self.read_boxpaper = False
        # взял ли игрок шкатулку?
        self.take_box = False
        # есть ли у игрока ключи для шкатулки
        self.keys_for_box = False
        # открытая ли шкатулка?
        self.opened_box = False

        # посмотрели ли игрок фотографии со стенда с картинками?
        self.seen_images = False
        # разгадал ли игрок морзе?
        self.morse = False

        # знает ли игрок кто изображен на портрете?
        self.chester = False

        # прочёл ли игрок предупреждение?
        self.read_warning = False

        self.thirst_paper = False
        self.second_paper = False
        self.third_paper = False
        self.had_readen_paper = False
        self.some_paper = False
        # окрыт ли сейф?
        self.safe_opened = False

        # нашел ли игрок газовую маску?
        self.find_gas_mask = False

        # готов ли игрок умереть?
        self.ready_to_die = False

        # игра проиграна
        self.game_over = False

        # квест пройден упешно
        self.win = False

        # конец
        self.end = False