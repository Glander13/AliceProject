# класс упрощающий написание JSON ответа
class Response:
    # инициализация
    def __init__(self, request):
        # заголовок ответа
        self.res = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False
            }
        }

    # добавление текста
    def addText(self, text):
        # если текста еще нет, то задает, иначе добавляем
        if not 'text' in self.res['response']:
            self.res['response']['text'] = text
        else:
            self.res['response']['text'] += ' ' + text

    # задание текста
    def setText(self, text):
        self.res['response']['text'] = text

    # добавление кнопки или ссылки
    def addButton(self, title, url=None):
        # если списка кнопок еще нет, то создаем
        if not 'buttons' in self.res['response']:
            self.res['response']['buttons'] = []

        button = {}
        button['title'] = title
        if url:
            button['url'] = url
            # если есть ссылка, то показываем ее, как ссылка, и чтобы не удалялась при нажатии
            button['hide'] = False
        else:
            # если ссылки нет, то показываем, как кнопка, и чтобы удалялась при нажатии
            button['hide'] = True

        # добавляем кнопку в список
        self.res['response']['buttons'].append(button)

    # добавляем изображение по ID
    def setImage(self, title, id):
        self.res['response']['card'] = {}
        self.res['response']['card']['type'] = 'BigImage'
        self.res['response']['card']['title'] = title
        self.res['response']['card']['image_id'] = id

    # добавляем завершение сеанса
    def endSession(self):
        self.res['response']['end_session'] = True
