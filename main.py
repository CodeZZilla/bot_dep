import telebot
import api
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import async_dec

TELEGRAM_TOKEN = ''
bot = telebot.TeleBot(TELEGRAM_TOKEN)
token_access = '12345'


@bot.message_handler(commands=['start'])
def start_message(message):
    telegram_id = message.chat.id
    if api.check_user(message):
        bot.send_message(telegram_id, 'Вітаю, ви вже зареєстровані у системі')
    else:
        api.create_user(telegram_id)
        bot.send_message(telegram_id, 'Вітаю у інформаційному боті e-розкладу Військового інституту'
                                      ' телекомунікацій та інформатизацій імені Героїв Крут')
        bot.send_message(telegram_id, 'Токен доступу: ')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        chat_id = call.message.chat.id
        split_array = str(call.data).split(':')
        key = split_array[0]
        value = split_array[1]

        if key == "group":
            reply_markup = call.message.reply_markup
            inline_keyboard = reply_markup.keyboard
            if value == 'save' or value == 'continue':
                selected_groups = filter_multi_select_return_array(inline_keyboard)
                if value == 'continue':
                    selected_groups = api.get_groups()
                api.update_field_for_user(chat_id, selected_groups, 'groups')
                filter_departments(chat_id, call.message.id, True)
            else:
                bot.edit_message_reply_markup(chat_id, call.message.id,
                                              reply_markup=filter_multi_select(reply_markup, value))
        elif key == "dep":
            reply_markup = call.message.reply_markup
            inline_keyboard = reply_markup.keyboard
            if value == 'save' or value == 'continue':
                selected_dep = filter_multi_select_return_array(inline_keyboard)
                if value == 'continue':
                    selected_dep = []
                    for k, v in api.get_departments().items():
                        selected_dep.append(v)
                api.update_field_for_user(chat_id, selected_dep, 'departments')
                filter_numbers_lessons(chat_id, call.message.id, True)
            else:
                bot.edit_message_reply_markup(chat_id, call.message.id,
                                              reply_markup=filter_multi_select(reply_markup, value))
        elif key == "number":
            reply_markup = call.message.reply_markup
            inline_keyboard = reply_markup.keyboard
            if value == 'save' or value == 'continue':
                selected_num = filter_multi_select_return_array(inline_keyboard)
                if value == 'continue':
                    selected_num = ["1", "2", "3", "4"]
                api.update_field_for_user(chat_id, selected_num, 'numberLessons')
                filter_types(chat_id, call.message.id, True)
            else:
                bot.edit_message_reply_markup(chat_id, call.message.id,
                                              reply_markup=filter_multi_select(reply_markup, value))
        elif key == "type":
            reply_markup = call.message.reply_markup
            inline_keyboard = reply_markup.keyboard
            if value == 'save' or value == 'continue':
                selected_types = filter_multi_select_return_array(inline_keyboard)
                if value == 'continue':
                    selected_types = []
                    for item in api.get_types():
                        selected_types.append(item['_id'])
                api.update_field_for_user(chat_id, selected_types, 'types')
                search(chat_id, call.message.id)
            else:
                bot.edit_message_reply_markup(chat_id, call.message.id,
                                              reply_markup=filter_multi_select(reply_markup, value))


@async_dec()
def filter_group(id_telegram, message_id, edit_flag=False):
    inline_keyboard = InlineKeyboardMarkup()
    group_array = api.get_groups()
    for i in range(0, len(group_array), 2):
        if i + 1 > len(group_array) - 1:
            inline_keyboard.row(
                InlineKeyboardButton(text=group_array[i], callback_data='group:' + group_array[i]))
        else:
            inline_keyboard.row(
                InlineKeyboardButton(text=group_array[i], callback_data='group:' + group_array[i]),
                InlineKeyboardButton(text=group_array[i + 1],
                                     callback_data='group:' + group_array[i + 1]))
    inline_keyboard.row(
        InlineKeyboardButton(text='Продовжити', callback_data='group:continue'),
        InlineKeyboardButton(text='Зберегти', callback_data='group:save'))
    if not edit_flag:
        bot.send_message(id_telegram, 'Виберіть групи (є можливість вибирати декілька)', reply_markup=inline_keyboard)
    else:
        bot.edit_message_text('Виберіть групи (є можливість вибирати декілька)', id_telegram, message_id)
        bot.edit_message_reply_markup(id_telegram, message_id, reply_markup=inline_keyboard)


@async_dec()
def filter_departments(id_telegram, message_id, edit_flag=False):
    inline_keyboard = InlineKeyboardMarkup()
    departments_map = api.get_departments()
    departments_array = []
    for k, v in departments_map.items():
        departments_array.append({
            'title': k,
            'id': v
        })
    for i in range(0, len(departments_array), 2):
        if i + 1 > len(departments_array) - 1:
            inline_keyboard.row(
                InlineKeyboardButton(
                    text=departments_array[i]['title'],
                    callback_data='dep:' + departments_array[i]['id']))
        else:
            inline_keyboard.row(
                InlineKeyboardButton(
                    text=departments_array[i]['title'],
                    callback_data='dep:' + departments_array[i]['id']),
                InlineKeyboardButton(
                    text=departments_array[i + 1]['title'],
                    callback_data='dep:' + departments_array[i + 1]['id']))
    inline_keyboard.row(
        InlineKeyboardButton(text='Продовжити', callback_data='dep:continue'),
        InlineKeyboardButton(text='Зберегти', callback_data='dep:save'))
    if not edit_flag:
        bot.send_message(id_telegram, 'Виберіть кафедри', reply_markup=inline_keyboard)
    else:
        bot.edit_message_text('Виберіть кафедри', id_telegram, message_id)
        bot.edit_message_reply_markup(id_telegram, message_id, reply_markup=inline_keyboard)


@async_dec()
def filter_numbers_lessons(id_telegram, message_id, edit_flag=False):
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.row(
        InlineKeyboardButton(text='1 пара', callback_data='number:1'),
        InlineKeyboardButton(text='2 пара', callback_data='number:2'))
    inline_keyboard.row(
        InlineKeyboardButton(text='3 пара', callback_data='number:3'),
        InlineKeyboardButton(text='4 пара', callback_data='number:4'))
    inline_keyboard.row(
        InlineKeyboardButton(text='Продовжити', callback_data='number:continue'),
        InlineKeyboardButton(text='Зберегти', callback_data='number:save'))
    if not edit_flag:
        bot.send_message(id_telegram, 'Виберіть пари', reply_markup=inline_keyboard)
    else:
        bot.edit_message_text('Виберіть пари', id_telegram, message_id)
        bot.edit_message_reply_markup(id_telegram, message_id, reply_markup=inline_keyboard)


@async_dec()
def filter_types(id_telegram, message_id, edit_flag=False):
    inline_keyboard = InlineKeyboardMarkup()
    types = api.get_types()
    for i in range(0, len(types), 2):
        if i + 1 > len(types) - 1:
            inline_keyboard.row(
                InlineKeyboardButton(text=types[i]['typeTitle'],
                                     callback_data='type:' + types[i]['_id']))
        else:
            inline_keyboard.row(
                InlineKeyboardButton(text=types[i]['typeTitle'],
                                     callback_data='type:' + types[i]['_id']),
                InlineKeyboardButton(text=types[i + 1]['typeTitle'],
                                     callback_data='type:' + types[i + 1]['_id']))
    inline_keyboard.row(
        InlineKeyboardButton(text='Продовжити', callback_data='type:continue'),
        InlineKeyboardButton(text='Зберегти', callback_data='type:save'))
    if not edit_flag:
        bot.send_message(id_telegram, 'Виберіть вид заняття (є можливість вибирати декілька)',
                         reply_markup=inline_keyboard)
    else:
        bot.edit_message_text('Виберіть вид заняття (є можливість вибирати декілька)', id_telegram, message_id)
        bot.edit_message_reply_markup(id_telegram, message_id, reply_markup=inline_keyboard)


def search(id_telegram, message_id):
    bot.delete_message(id_telegram, message_id)
    user = api.get_user(id_telegram)
    array_req = api.post_search_params(user['departments'], user['groups'], user['types'], user['numberLessons'])
    text = ''
    if len(array_req) == 0:
        text = 'Не знайдено❗️\n'
    else:
        text = 'Знайдено❗️\n'
        for item in array_req:
            text = text + f'{item["numberLesson"]} пара - {item["group"]} нг - {item["type"]} - {item["audience"]}' \
                          f' ({item["departmentNumber"]}) - {item["teacher"]} ({item["title"]})\n'
    bot.send_message(id_telegram, str(text))


def filter_multi_select_return_array(inline_keyboard):
    len_inline_keyboard = len(inline_keyboard)
    selected = []
    for i in range(len_inline_keyboard - 1):
        len_row = len(inline_keyboard[i])
        for j_row in range(len_row):
            if str(inline_keyboard[i][j_row].text).startswith('✅ '):
                selected.append(inline_keyboard[i][j_row].callback_data.split(':')[1])
    return selected


def filter_multi_select(reply_markup, value):
    keyboard = reply_markup.keyboard
    len_keyboard = len(keyboard)
    if not value == 'save' and not value == 'continue':
        for i in range(len_keyboard - 1):
            len_row = len(keyboard[i])
            for j_row in range(len_row):
                if str(keyboard[i][j_row].callback_data).split(':')[1] == value:
                    if not str(keyboard[i][j_row].text).startswith('✅ '):
                        keyboard[i][j_row].text = '✅ ' + keyboard[i][j_row].text
                    else:
                        keyboard[i][j_row].text = keyboard[i][j_row].text[2:]
        reply_markup.keyboard = keyboard
        return reply_markup


@bot.message_handler(content_types=['text'], func=lambda message: True)
def send_text(message):
    telegram_id = message.chat.id
    message_text = message.text
    user = api.get_user(telegram_id)
    if not user['userStatus']:
        if message_text == token_access:
            api.update_field_for_user(telegram_id, True, 'userStatus')
            bot.send_message(telegram_id,
                             'Токен доступу прийнятий, тепер ви можете використовувати повний функціонал боту')
            filter_group(telegram_id, True)


print('Listening....')
count_restarts = 0
while True:
    try:
        bot.polling(none_stop=True)
    except:
        count_restarts = count_restarts + 1
        print(f'count_restarts = {count_restarts}')
        # logging.error(sys.exc_info()[0])
        # time.sleep(TIME_SLEEP)
