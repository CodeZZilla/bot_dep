import requests

link = 'http://192.168.0.75:8989'


def get_groups():
    req = requests.get(link + '/search/groups')
    return req.json()


def get_types():
    req = requests.get(link + '/search/types')
    return req.json()


def get_departments():
    req = requests.get(link + '/search/departmentsNumberMap')
    return req.json()


def post_search_params(users_id, groups, types_id, number_lessons):
    req = requests.post(link + '/search/params', headers={'Content-Type': 'application/json'}, json={
        'usersId': users_id,
        'groups': groups,
        'typesId': types_id,
        'numberLessons': number_lessons
    })
    return req.json()


def get_user(id_telegram):
    req = requests.get(link + '/api/telegram/user/find/' + str(id_telegram))
    return req.json()


def get_users():
    req = requests.get(link + '/api/telegram/users')
    return req.json()


def create_user(id_telegram):
    req = requests.post(link + '/api/telegram/user/create', headers={'Content-Type': 'application/json'}, json={
        'telegramId': str(id_telegram),
        'groups': [],
        'types': [],
        'departments': [],
        'numberLessons': [],
        'userStatus': False
    })
    return req.json()


def check_user(message):
    req = requests.get(link + '/api/telegram/user/find/' + str(message.from_user.id))
    if req.text == 'null':
        return False
    return True


def update_field_for_user(id_telegram, value, str_field):
    user = get_user(id_telegram)
    user[str_field] = value
    req = requests.post(link + '/api/telegram/user/edit', headers={'Content-Type': 'application/json'}, json={
        'id': str(id_telegram),
        'user': user
    })
    return req.json()

