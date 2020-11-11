import telepot
import time
from scraper import get_data
import re
import os

urls = []
commands = ['/add', '/list', '/remove']

def hello_msg(name):
    return  '''Hello %s, 
type one of the following commands: 
/list - list the price of all your following link
/add - add a new link to follow
/remove - remove a link to follow''' %name


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(msg)
    # print(chat_id)
    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = msg['text']

        if txt == '/list':
            for index, url in enumerate(urls):
                text = get_data(url)
                bot.sendMessage(chat_id, text)

        elif '/add' in txt:
            urls.append(re.findall("(?P<url>https?://[^\s]+)", txt)[0])
            print(urls)
        elif txt == '/remove':
            bot.sendMessage(chat_id, 'bravo')
        else:
            bot.sendMessage(chat_id, 'This command does not exist')

        bot.sendMessage(chat_id, hello_msg(name))


if __name__ == "__main__":
    TOKEN = os.environ['TOKEN']

    bot = telepot.Bot(TOKEN)
    bot.message_loop(on_chat_message)

    print('Listening ...')

    while 1:
        time.sleep(10)