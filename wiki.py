import wikipedia
import re

wikipedia.set_lang("ru")

def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Википедия":
        bot.send_message(chat_id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')
        input_w(bot, chat_id)

def input_w(bot, chat_id):
    ResponseHandler = lambda message: bot.send_message(chat_id,get_wiki(message.text))

    my_input(bot, chat_id,ResponseHandler)

def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)


def get_wiki(bot, chat_id):
    try:
            page = wikipedia.page()
            wikitext = page.content[:1000]
            wikimas = wikitext.split('.')
            wikimas = wikimas[:-1]
            wikitext2 = ''
            for x in wikimas:
                if not('==' in x):
                    if (len((x.strip()))>3):
                        wikitext2=wikitext2+x+''
                else:
                    break

            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)

            return wikitext2

    except Exception as e:
            return 'В энциклопедии нет информации об этом'


