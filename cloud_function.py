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

task = ['Губка Боб хочет набрать 6 литров воды из моря. У него есть 5 \
        литровый кувшин и 7 литровое ведро. Как это сделать?', 'Наливаете \
        5-литровую емкость полностью, переливаете в 7 литровую. Опять \
        наливаете 5-литровую и доливаете из нее 7-литровую полностью. Теперь \
        у вас в 5-литровой 3 литра. Выливаете 7-литровую и переливаете в нее \
        3 литра из 5-литровой. Наливаете 5-литровую полностью и доливаете из \
        нее до полной 7-литровую. Теперь у вас в 5-литровой остался один литр. \
        Выливаете 7-литровую, переливаете 1 литр из 5-литровой в 7-литровую, \
        наливаете полную 5-литровую и переливаете в 7-литровую. Теперь у вас там 6 литров.']