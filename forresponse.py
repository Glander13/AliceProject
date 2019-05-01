class Response:
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
    def addAnswer(self, text):
        if not 'text' in self.res['response']:
            self.res['response']['text'] = text
        else:
            self.res['response']['text'] += ' ' + text
    # добавление кнопки или ссылки
    def addButton(self, title, url=None):
        if not 'buttons' in self.res['response']:
            self.res['response']['buttons'] = []

        button = {}
        button['title'] = title
        if url:
            button['url'] = url
            button['hide'] = False
        else:
            button['hide'] = True
        # добавляем кнопку в список
        self.res['response']['buttons'].append(button)

    # добавляем изображение по ID
    def addImage(self, title, id):
        self.res['response']['card'] = {}
        self.res['response']['card']['type'] = 'BigImage'
        self.res['response']['card']['title'] = title
        self.res['response']['card']['image_id'] = id

    # добавляем завершение сеанса
    def endSession(self):
        self.res['response']['end_session'] = True

