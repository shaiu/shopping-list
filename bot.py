import json
import logging
import os

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
RAMY_TOKEN = os.environ.get('RAMY_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://www.rami-levy.co.il/api/v2/cart"

payload = json.dumps({
    "store": "412",
    "isClub": 0,
    "supplyAt": "2022-05-14T00:00:00.000Z",
    "items": {
        "35": "1.00"
    },
    "meta": None
})
headers = {
    'ecomtoken': RAMY_TOKEN,
    'Content-Type': 'application/json'
}


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    item = update.message.text
    if item == "banana":
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info("response from ramy %s", response)
        update.message.reply_text("added the item")
        return
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f'{WEBHOOK_URL}{TOKEN}')
    updater.idle()


if __name__ == '__main__':
    main()
