import telegram
import logging
from telegram.ext import CommandHandler
from telegram.ext import Updater

CONFIG_PATH = ".apiconfig"

def get_config(config_path):
    config = {}
    with open(CONFIG_PATH) as myfile:
        for line in myfile:
            name, var = line.partition(":")[::2]
            config[name.strip()] = var.strip()
    return config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

config = get_config(CONFIG_PATH)
Token = config["token"]
bot=telegram.Bot(token=Token)
print(bot.get_me())

updater = Updater(token=Token)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()