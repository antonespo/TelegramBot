import logging
from scraper import get_data, print_data_ordered
import os

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_LINK, TYPING_LINK_TO_DELETE = range(3)

reply_keyboard = [
    ['Add link', 'Delete link'],
    ['Show links', 'Show products'],
    ['Done']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! My name is TrovaPrezzi Bot. I will hold the link of the products you want to monitor. "
        "And if you click on 'Show products' button, I will scrape the website to give you interesting info about price",
        reply_markup=markup,
    )
    return CHOOSING


def add_link(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Can you please add a link of TrovaPrezzi.it with the product you are interested in?'
    )
    return TYPING_LINK


def received_link(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if context.user_data.get('links') is None:
        context.user_data['links'] = []
    context.user_data['links'].append(text)

    update.message.reply_text(
        "Wonderful! I have saved %s links!" %len(context.user_data.get('links')),
        reply_markup=markup
    )
    return CHOOSING


def delete_link(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('links') is None:
        update.message.reply_text(
            'You have not inserted links yet',
            reply_markup=markup
        )
    else:
        update.message.reply_text(
            'Can you please type the number of the link you want to delete?'
        )
        text = ''
        for index, link in enumerate(context.user_data.get('links')):
            text = text + f"\n {index+1} - {link} "
        update.message.reply_text(text)
    return TYPING_LINK_TO_DELETE


def received_link_to_delete(update: Update, context: CallbackContext) -> int:
    num = int(update.message.text)
    context.user_data['links'].pop(num-1)

    update.message.reply_text(
        "Wonderful! I have deleted the link and now the list is %s long" %len(context.user_data.get('links')),
        reply_markup=markup
    )
    return CHOOSING


def show_links(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('links') is None:
        update.message.reply_text(
            'You have not inserted links yet',
            reply_markup=markup
        )
    else:
        text = "These are the links saved: "
        for index, link in enumerate(context.user_data.get('links')):
            text = text + f"\n {index+1} - {link} "
        update.message.reply_text(
            text,
            reply_markup=markup
        )
    return CHOOSING


def show_products(update: Update, context: CallbackContext) -> int:
    if context.user_data.get('links') is None:
        update.message.reply_text(
            'You have not inserted links yet',
            reply_markup=markup
        )
    else:
        for link in context.user_data.get('links'):
            df = get_data(link)
            text = print_data_ordered(df, link)
            update.message.reply_text(text)
        make_choise(update, context)
    return CHOOSING


def make_choise(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('How do you want to continue?',
                              reply_markup=markup)
    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        "Bye, bye. Digit /start to start again"
    )
    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ['TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Add link)$'), add_link
                ),
                MessageHandler(
                    Filters.regex('^(Show links)$'), show_links
                ),
                MessageHandler(
                    Filters.regex('^(Show products)$'), show_products
                ),
                MessageHandler(
                    Filters.regex('^(Delete link)$'), delete_link
                ),
                MessageHandler(
                    ~(Filters.command | Filters.regex('^Done$')), make_choise
                )
            ],
            TYPING_LINK: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_link
                )
            ],
            TYPING_LINK_TO_DELETE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_link_to_delete
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()