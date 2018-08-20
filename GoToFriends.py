import telebot
import emoji
from telebot import types
import time
import json
import requests
import random

token = "🔦"
telebot.apihelper.proxy = {'https': 'socks5://tvorogme:TyhoRuiGhj1874@tvorog.me:6666'}
bot = telebot.TeleBot(token=token)

news_shapito = 'shapito'
url = 'https://meduza.io/api/v3/search?chrono={}&locale=ru&page=0&per_page=24'.format(news_shapito)
response = requests.get(url)
answer = json.loads(response.text)

urr = []
documents_answer = answer.get('collection')
for i in range(len(documents_answer)):
    link = documents_answer[i]
    url = 'https://meduza.io/{}'.format(link)
    urr.append(url)
    if i == 20:
        break

queue = []
interests = {}
current_conversations = {}
nicknames={}
def interest(message):
    global queue
    user = message.chat.id
    global interests
    try:
        interests[user]=message.text
    except:
        bot.send_message(user, 'Something goes wrong...')
    bot.send_message(user, "👥 Помещаю тебя в очередь. Надо чуть подождать")
    if len(queue) == 0:
        queue.append(user)
        bot.send_message(queue[0], '🐳 Пока никого нет. Но вы в очереди.. Кип гоин!')
        return
    if user in queue:
        bot.send_message(user, '🦑 Вы уже в очереди')
        return
    else:
        ran = random.randint(1, 20)
        queue.append(user)
        current_conversations[queue[0]] = queue[1]
        current_conversations[queue[1]] = queue[0]
        nicknames[user] = message.from_user.username
        bot.send_message(current_conversations[queue[0]], "👋 Я нашел тебе собеседника")
        time.sleep(2)
        bot.send_message(current_conversations[queue[0]], "Вот, что он написал про свои интересы: " + str(interests[queue[0]]))
        time.sleep(1)
        bot.send_message(current_conversations[queue[0]], "А обсудить можете вот что: " + str(urr[ran]))

        bot.send_message(current_conversations[queue[1]], "👋 Я нашел тебе собеседника")
        time.sleep(2)
        bot.send_message(current_conversations[queue[1]], "Вот, что он написал про свои интересы: " + str(interests[queue[1]]))
        time.sleep(1)
        bot.send_message(current_conversations[queue[1]], "А обсудить можете вот что: " + str(urr[ran]))
        queue = []



@bot.message_handler(commands=['start'])
def start(message):

    global interests
    global queue
    user = message.chat.id

    if user in queue:
        bot.send_message(user, '🦑 Вы уже в очереди')
        return

    bot.send_message(user, "✋️ Привет! Я помогу тебе найти новых друзей.")

    time.sleep(1)
    bot.send_message(user, "🤖  Я соединяю тебя с рандомным пользователем, а позже (если вы подружитесь)"
                           " ты сможешь узнать как его зовут и подружиться в реале!")
    bot.send_message(user, "🙌 Чтобы узнать, кто твой собеседник напиши /deanon, если он ответит согласием, ты узнаешь кто он.")
    time.sleep(2)
    m = bot.send_message(user, "📷 🎆 🎮 Введи свои интересы через запятую")
    bot.register_next_step_handler(m, interest)
@bot.message_handler(commands=['stop'])
def stop(message):
    return

@bot.message_handler(content_types=['text'])
def talking(message):
    global nicknames
    uid=message.chat.id
    text=message.text
    print(text,message.chat.id,message.from_user.username)
    try:
        nicknames[message.chat.id] = message.from_user.username
    except:
        nicknames[message.chat.id] = 'no nickname'
    try:
        bot.send_message(current_conversations[uid],text)
    except:
        bot.send_message(uid, "Something goes wrong")
    if text == '/deanon':
        keyboard = types.InlineKeyboardMarkup()
        user = message.chat.id
        bot.send_message(user, "Жду согласия твоего собеседника 🕐")
        button1 = types.InlineKeyboardButton(text='✋️ Конечно', callback_data="button1")
        button2 = types.InlineKeyboardButton(text='🗣 Пока что нет.', callback_data="button2")
        keyboard.add(button1)
        keyboard.add(button2)
        bot.send_message(current_conversations[user], 'Твой собеседник хочет узнать кто ты. Согласен?', reply_markup=keyboard)



    @bot.callback_query_handler(func=lambda call: True)
    def photoo(call):
        global nicknames
        user=call.message.chat.id
        if call.data == 'button1':
            bot.send_message(current_conversations[user], '📢 И.. вот ссылка на вашего собеседника:')
            try:
                bot.send_message(current_conversations[user], "@"+str(nicknames[user]))
            except:
                bot.send_message(current_conversations[user],'Something goes wrong...')
            bot.send_message(user, 'Твой собеседник теперь знает твой ник. Переходите в лс и общайтесь, а лучше встретьтесь где-нибудь.')
            bot.send_message(user, 'Удачи, ребят. Вы крутые 😏')
            nicknames={}
            return
        if call.data == 'button2':
            bot.send_message(current_conversations[user], 'Жаль.. Продолжайте общаться!')
            bot.send_message(message.chat.id, 'Ваш собеседник не согласен. Жаль.')


bot.polling(none_stop=True)