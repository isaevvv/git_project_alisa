def put_item(req, res):
    item = req['request']['nlu']['intents']['put_item']['slots']['what']['value']
    items = res['session_state']['items']
    if item in set(items):
        res['response']['text'] = f"{item} уже в списке"
    else:
        items.append(item)
        res['response']['text'] = f"Добавили {item}"


def check_item(req, res):
    item = req['request']['nlu']['intents']['check_item']['slots']['what']['value']
    items = res['session_state']['items']
    res['response']['text'] = f"{item} {'не' if item not in set(items) else ''}в списке"


def remove_item(req, res):
    item = req['request']['nlu']['intents']['remove_item']['slots']['what']['value']
    items = res['session_state']['items']
    if item in set(items):
        items.remove(item)
        res['response']['text'] = f"Удалили {item}"
    else:
        res['response']['text'] = f"Не нашли {item}"

def show_list(req, res):
    items = res['session_state']['items']
    if not items:
        res['response']['text'] = "Список пуст"
    else:
        res['response']['text'] = f"В списке {', '.join(items)}"

def uncloun_command(req, res):
    res['response']['text'] = 'Я навык, который умеет добавлять и удалять объекты в списке и больше ничего'

def handler(event, context):
    intents = {
        "put_item": put_item,
        "check_item": check_item,
        "remove_item": remove_item,
        "show_list": show_list
    }


    response = {
        "session": event["session"],
        "version": event["version"],
        "response": {
            "end_session": False,
        },
        "session_state": event.get('state',{}).get('session', {})
    }
    if not response['session_state']:
        response['session_state'] = {'items': []}
    try:
        intents[list(event['request']['nlu']['intents'].keys())[0]](event, response)
    except IndexError:
        uncloun_command(event, response)
    response['response']['tts'] = response['response'] ['text']
    return response


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None
        }
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я - Алиса. Какой город хочешь увидеть?'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = games.keys()
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе,
    # что хочет увидеть.
    else:
        '''
        # ищем город в сообщение от пользователя
        game = get_city(req)
        # если этот город среди известных нам,
        # то показываем его (выбираем одну из двух картинок случайно)
        if city in cities:
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю.'
            res['response']['card']['image_id'] = random.choice(cities[city])
            res['response']['text'] = 'Я угадал!'
        # если не нашел, то отвечает пользователю
        # 'Первый раз слышу об этом городе.'
        else:
            res['response']['text'] = \
                'Первый раз слышу об этом городе. Попробуй еще разок!'
        '''

def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)

task1 = ['Губка Боб хочет набрать 6 литров воды из моря. У него есть 5 \
        литровый кувшин и 7 литровое ведро. Как это сделать?', 'Наливаете \
        5-литровую емкость полностью, переливаете в 7 литровую. Опять \
        наливаете 5-литровую и доливаете из нее 7-литровую полностью. Теперь \
        у вас в 5-литровой 3 литра. Выливаете 7-литровую и переливаете в нее \
        3 литра из 5-литровой. Наливаете 5-литровую полностью и доливаете из \
        нее до полной 7-литровую. Теперь у вас в 5-литровой остался один литр. \
        Выливаете 7-литровую, переливаете 1 литр из 5-литровой в 7-литровую, \
        наливаете полную 5-литровую и переливаете в 7-литровую. Теперь у вас там 6 литров.']

task2 = []

sessionStorage = {}

games = {
    'Переливания': task1,
    'Игра Баше': task2,
    'Ним': task2
}