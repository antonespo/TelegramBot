import telepot
import time
import os


def on_new_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = msg['text']
        bot.sendMessage(chat_id, 'Hello %s, this is your new bot!'%name)
        bot.sendMessage(chat_id, 'You have just typed: %s'%txt)

TOKEN = os.environ['TOKEN']

bot = telepot.Bot(TOKEN)
bot.message_loop(on_new_message)

print('Listening ...')

while 1:
    time.sleep(10)
