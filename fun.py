
import re
from fake_useragent import UserAgent
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import wikipedia

wikipedia.set_lang("ru")


# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

    elif ms_text == "Прислать лису":
        bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе лисичка!")

    # elif ms_text == "Прислать рисунок":
    #     bot.send_photo(chat_id, photo=get_art(), caption="Вот тебе рисунок!")

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)

    elif ms_text == "Цитаты":
        bot.send_message(chat_id, text=getRandomquot())

    elif ms_text == "Википедия":
        bot.send_message(chat_id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')

    elif ms_text == "Факт":
        bot.send_message(chat_id, text=get_fact())

    elif ms_text == "Мем":
        bot.send_photo(chat_id, photo=get_meme)


#-------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url
#----------------------------------------------------
def get_meme():
    url = ""
    images = []
    page_link = 'https://knowyourmeme.com/random'.format(get_meme)
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})

    if page_link.status_code == 200:
        html = response.content
        soup = bs4.BeautifulSoup(html, 'html.parser')

        meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
        meme_links = ['http://knowyourmeme.com' + link.attrs['href'] for link in meme_links]
        for img in meme_links:
            images.append(img.get('src'))


    return url

    # infoFilm = {}
    # url = ""
    # req = 'https://dtf.ru/kek/entries/new'
    # if req.status_code == 200:
    #     response = requests.get(req, headers={'User-Agent': UserAgent().chrome})
    #     soup = bs4.BeautifulSoup(response.content, 'html.parser')
    #     result_find = soup.find('div', attrs={'class': 'content-image'})
    #     result_find2 = result_find.find('div', attrs={'class': 'andropov_image'})
    #     images = []
    #     for img in result_find2.findAll('img'):
    #         images.append(img.get('src'))
    #     infoFilm["meme"] = images[0]
    # return infoFilm


    # url = ""
    # req = requests.get('https://dtf.ru/kek/entries/new')
    # header = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36"
    # }
    # if req.status_code == 200:
    #     r = requests.get(url, headers=header).text
    #     soup = bs4.BeautifulSoup(r, 'html.parser')
    #     bs = soup.find('div', class_='content-image')
    #     bs2 = bs.find('div', class_='andropov_image')
    #     list = open("list.txt", "w+")
    #     link = (bs2['src'])  # Сам парсер мемов
    #
    #     with open("list.txt", "w") as file:
    #         file.write(link)
    #
    # return url
#------------------------------------------------------
def get_fact():
    array_anekdots = []
    req_anek = requests.get('https://randstuff.ru/fact/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('table', class_='text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""
#---------------------------------------------------------------------
# def get_art():
#     url = "https://vk.com/album-183412821_281017168"
#     art = {}
#     req_art = requests.get(url)
#     if req_art.status_code == 200:
#         soup = bs4.BeautifulSoup(req_art.text, "html.parser")
#         result_find = soup.find('div', class_="photos_row")
#         result_find2 = soup.find('div', style="background-image")
#         images = []
#         for img in result_find2.findAll('img'):
#             images.append(url + img.get('src'))
#         art["result_find2"] = images[0]
#
#     return art
#

#--------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

#----------------------------------------------------------------------------
def getRandomquot():
    array_anekdots = []
    req_anek = requests.get('https://quotes.toscrape.com/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, 'html.parser')
        quotes = soup.select('span', class_='text')

        for result in quotes:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""

# -----------------------------------------------------------------------





#-----------------------------------------------------------------------
def get_ManOrNot(bot, chat_id):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm


#------------------------------------------------------
