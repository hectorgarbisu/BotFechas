# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from text_date_extractor import get_date
from bot_calendar import calendario

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('apikey', 'r') as apikey_file:
    TOKEN = apikey_file.read()

# calendario object that handles calendar data (like storing and retrieving events)
cal = calendario()
# temporal storage for events pending of confirmation by the user
# Uses msg_id as key so only one date can be stored per message
temp_date_dict = {}

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def clear_pending(bot, update):
    """ Clears the list of pending dates to aprove """
    temp_date_dict = {}
    show_pending(bot, update)

def show_pending(bot, update):
    """ Shows the list of pending dates to aprove """
    response = ""
    for date_string, event in temp_date_dict:
        response += "\n" + date_string + ": " + event
    update.message.reply_text(response)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Encendido')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Nadie puede oir tus gritos')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def days(bot, update, args=[1]):
    """ retrieves events for the following days """
    days_events = cal.get_days(int(args[0]))
    if days_events: update.message.reply_text("\n".join(days_events))

def week(bot, update):
    """ retrieves current week events """
    this_weeks_events =  cal.get_this_week()
    if this_weeks_events: update.message.reply_text("\n".join(this_weeks_events))


def month(bot, update):
    """ retrieves current month events """
    this_month_events = cal.get_this_month()
    if this_month_events: update.message.reply_text("\n".join(this_month_events))

def texto(bot, update):
    """ Handles text messages by trying to find a suitable date format. The first date-like
    structure is found, it is saved temporaryly in temp_date_dict, and is added to calendario
    upon confirmation by button  """
    msg = update.message.text.lower()
    (date,trace) = get_date(msg)
    print("message received: " + msg)
    print(trace)
    if not date: return
    msg_id = update.message.message_id
    temp_date_dict[msg_id] = (msg, date)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Guardar en calendario", callback_data = msg_id)]])
    update.message.reply_text(response_text(msg, update, date), reply_markup=reply_markup)

def response_text(msg, update, date):
    response = ""
    date_string = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
    response += "posible fecha detectada para " +  update.message.from_user.first_name + "! : \n"
    response += date_string + " en :\n"
    response += msg
    return response

def button(bot, update):
    """ Tries to save the corresponding date and event to calendario """
    query = update.callback_query
    emmiter_msg_id = query.data
    event, date = temp_date_dict.pop(int(emmiter_msg_id))
    print(temp_date_dict)
    cal.add_event(event, date)
    date_string = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
    bot.edit_message_text(text="Fecha guardada: {}".format(date_string),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

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
    dp.add_handler(CommandHandler("semana", week))
    dp.add_handler(CommandHandler("mes", month))
    dp.add_handler(CommandHandler("dias", days, pass_args=True))
    dp.add_handler(CommandHandler("limpiar", clear_pending))
    dp.add_handler(CommandHandler("pendientes", show_pending))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, texto))

    # Button handler
    dp.add_handler(CallbackQueryHandler(button))

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
