import telebot
from telebot import types
import botGames
import menuBot
from menuBot import Menu
import DZ
import fun



bot = telebot.TeleBot('5220552349:AAGUwS1OQLApB0Lovm7AWNDK75GKCXNZf3Q')


# -----------------------------------------------------------------------
@bot.message_handler(commands="start")
def command(message):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)



# -----------------------------------------------------------------------
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    # bot.send_message(message.chat.id, voice)



# -----------------------------------------------------------------------
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)




# -----------------------------------------------------------------------
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])

    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)
    if subMenu is not None:

        if subMenu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))
            text_game = game21.get_cards(2)
            bot.send_media_group(chat_id, media=game21.mediaCards)
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = botGames.newGame(chat_id, botGames.GameRPS())
            bot.send_photo(chat_id, photo=gameRPS.url_picRules, caption=gameRPS.text_rules, parse_mode='HTML')

        return


    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:
        module = cur_menu.module

        if module != "":
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Помощь":
            send_help(bot, chat_id)

    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":
        botGames.callback_worker(bot, cur_user, cmd, par, call)


# -----------------------------------------------------------------------
def send_help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Швец Андрей")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/user59387")
    markup.add(btn1)
    img = open('Швец Андрей.png', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

# ---------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)
