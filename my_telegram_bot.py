# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from text_date_extractor import get_date

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('apikey', 'r') as apikey_file:
    TOKEN = apikey_file.read()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Encendido')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Nadie puede oir tus gritos')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def texto(bot, update):
    msg = update.message.text.lower()
    print("message received: " + msg)
    response = ""
    (date,trace) = get_date(msg)
    print trace
    if date:
        response += "Hola, " #+ update.message.from_user.first_name
        response += "\nposible fecha detectada! : " + str(date.day) + " " + str(date.month) + " " + str(date.year) + " en :\n"
        response += msg.upper()
        update.message.reply_text(response)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, texto))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
