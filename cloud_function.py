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