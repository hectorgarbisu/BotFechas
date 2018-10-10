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

with open('./data/apikey', 'r') as apikey_file:
    TOKEN = apikey_file.read()

# calendario object that handles calendar data (like storing and retrieving events)

calendarios = {}

# temporal storage for events pending of confirmation by the user
# Uses msg_id as key so only one date can be stored per message

temp_date_dicts = {}
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

command_list = "/start: no hace nada\n" + " /help: muestra esta lista\n" +\
"/semana: muestra los eventos de esta semana\n"+\
"/mes: muestra los eventos de este mes\n"+\
"/dias X: muestra los eventos entre hoy y dentro de X días\n"+\
"/purgar_cola: elimina los eventos pendientes de confirmación\n"+\
"/pendientes: muestra los eeventos almacenados sin confirmar\n"+\
"/borrar_pasadas: elimina los eventos anteriores al día de hoy\n"+\
"/borrar_todo: eliminna todos los eventos del calendario\n"


def clear_pending(bot, update):
    """ Clears the list of pending dates to aprove """
    chat_id = str(update.message.chat_id)
    if temp_date_dicts[chat_id]:
        temp_date_dicts[chat_id].clear()
        update.message.reply_text("Cola de entradas purgada")


def show_pending(bot, update):
    """ Shows the list of pending dates to aprove """
    chat_id = str(update.message.chat_id)
    if temp_date_dicts[chat_id]:
        response = ""
        for date_string, event in temp_date_dicts[chat_id]:
            response += "\n" + date_string + ": " + event
        update.message.reply_text(response)


def delete_old(bot, update):
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    calendarios[chat_id].delete_old()
    calendarios[chat_id].save_to_disk()
    update.message.reply_text("Eliminadas entradas anteriores a hoy")


def delete_all(bot, update):
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    calendarios[chat_id].delete_all()
    calendarios[chat_id].save_to_disk()
    update.message.reply_text("Eliminadas todas las entradas")


def days(bot, update, args):
    """ retrieves events for the following days """
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    days = 1
    if len(args): days = int(args[0])
    days_events = calendarios[chat_id].get_days(days)
    if days_events:
        update.message.reply_text("\n".join(days_events))


def week(bot, update):
    """ retrieves current week events """
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    this_weeks_events = calendarios[chat_id].get_this_week()
    if this_weeks_events:
        update.message.reply_text("\n".join(this_weeks_events))

def all(bot, update):
    """ retrieves current week events """
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    all_events = calendarios[chat_id].get_all()
    if all_events: 
        update.message.reply_text("\n".join(all_events))

def month(bot, update):
    """ retrieves current month events """
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    this_month_events = calendarios[chat_id].get_this_month()
    if this_month_events:
        update.message.reply_text("\n".join(this_month_events))


def start(bot, update):
    """Send a message when the command /start is issued."""
    chat_id = str(update.message.chat_id)
    logger.info('chat comenzado con chat_id: %s', chat_id)    
    calendarios[chat_id] = calendario(chat_id)
    temp_date_dicts[chat_id] = {}
    update.message.reply_text('Encendido')



def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Lista de comandos:\n' + command_list)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def texto(bot, update):
    """ Handles text messages by trying to find a suitable date format. The first date-like
    structure is found, it is saved temporaryly in temp_date_dict, and is added to calendario
    upon confirmation by button  """
    chat_id = str(update.message.chat_id)
    if chat_id not in calendarios:
        calendarios[chat_id] = calendario(chat_id)
        temp_date_dicts[chat_id] = {}
    msg = update.message.text.lower()
    (date, trace) = get_date(msg)
    logger.info('trace "%s" for message:  "%s"', trace, msg)
    if not date:
        return
    msg_id = update.message.message_id
    temp_date_dicts[chat_id][msg_id] = (msg, date)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Guardar en calendario", callback_data=msg_id)]])
    update.message.reply_text(response_text(
        msg, update, date), reply_markup=reply_markup)


def response_text(msg, update, date):
    response = ""
    date_string = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
    response += "posible fecha detectada para " + \
        update.message.from_user.first_name + "! : \n"
    response += date_string + " en :\n"
    response += msg
    return response


def button(bot, update):
    """ Tries to save the corresponding date and event to calendario """
    #chat_id = str(update.callback_query.chat_id)
    chat_id = str(update.callback_query.message.chat.id)
    query = update.callback_query
    emmiter_msg_id = query.data
    event, date = temp_date_dicts[chat_id].pop(int(emmiter_msg_id))
    calendarios[chat_id].add_event(event, date)
    calendarios[chat_id].save_to_disk()
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
    dp.add_handler(CommandHandler("todo", all))
    dp.add_handler(CommandHandler("dias", days, pass_args=True))
    dp.add_handler(CommandHandler("purgar_cola", clear_pending))
    dp.add_handler(CommandHandler("pendientes", show_pending))
    dp.add_handler(CommandHandler("borrar_pasadas", delete_old))
    dp.add_handler(CommandHandler("borrar_todo", delete_all))

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
