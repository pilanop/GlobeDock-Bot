from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from message_handler import profanity_handler, image_handler, button

# imports as per the actual handlers

# Get your token from BotFather
TOKEN = "6619584072:AAFHpKqQRv5gng3ui5gCKbPnTCnX6xqj8Hg"


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(profanity_handler)
    dp.add_handler(image_handler)
    dp.add_handler(CallbackQueryHandler(button))  # Register the callback query
    # handler

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
