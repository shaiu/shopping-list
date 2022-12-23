import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.parsemode import ParseMode

from cart import cart
from catalog import catalog

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    logger.info("starting")
    context.bot_data["items"], context.bot_data["items_reverse"] = catalog.get_all_items()
    logger.info("loaded all items to context")
    update.message.reply_text("Loaded all items from catalog")


def show_cart(update, context):
    logger.info("showing cart")
    i = 1
    text = ""
    for item in cart.get_local_items():
        text += f"{i}. {context.bot_data['items_reverse'][item]}\n"
        i += 1
    if text == "":
        logger.info("no items in cart")
        update.message.reply_text("no items in cart")
        return
    logger.info(f"items in cart: {text}")
    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def load_cart(update, context):
    logger.info("loading cart to site")
    cart.add_items_cart(list(map(lambda local_item: context.bot_data["items"][local_item], cart.get_local_items())))
    update.message.reply_text("https://www.rami-levy.co.il/he")


def clear_cart(update, context):
    logger.info("clearing cart")
    cart.clear_local_items()
    update.message.reply_text("Cart is cleared")


def add_item(update, context):
    item = update.message.text
    logger.info(f"got text from user <{item}>")
    kblist = list(map(lambda cart_item: [InlineKeyboardButton(cart_item[0], callback_data=cart_item[1])],
                      cart.get_items(context.bot_data, item)))
    reply_markup = InlineKeyboardMarkup(kblist)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def button(update: Update, context) -> None:
    query = update.callback_query
    query.answer()
    item = query.data
    logger.info(f"adding item <{context.bot_data['items_reverse'][item]}> to cart")
    cart.add_local_item(item)
    query.delete_message()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cart", show_cart))
    dp.add_handler(CommandHandler("load_cart", load_cart))
    dp.add_handler(CommandHandler("clear_cart", clear_cart))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, add_item))
    dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url=f'{WEBHOOK_URL}/{TOKEN}')

    updater.idle()


if __name__ == '__main__':
    main()
