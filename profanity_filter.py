import re
from telegram import Update
from telegram.ext import CallbackContext
from better_profanity import profanity
import time

# Custom array of words to be added to the filter
custom_words = ['tebeda', 'wesha', 'jela',
                'dedeb', 'ahya', 'shermuta',
                'koletam', 'kolet', 'tnbatam',
                'gmatam', 'Enaten', 'denez', 'ደደብ',
                '🖕🏾', '🖕', 'ተበዳ', 'ትበዳ',
                'ደነዝ', 'አህያ', 'ሸርሙጣ', 'ጀላ',
                'ቆለጥ', 'ቆለጣም', 'ግማታም',
                'ጅል', 'etc.']


# Function to update the profanity filter list
def update_profanity_list():
    profanity.load_censor_words()
    profanity.add_censor_words(custom_words)


# Function to filter out messages based on profane language
def filter_messages(update: Update, context: CallbackContext):
    message = update.message

    # Update a profanity list with custom words
    update_profanity_list()

    # Check for profane language
    if profanity.contains_profanity(message.text):
        # Delete the original offensive message
        message.delete()

        # Notify the group and tag the user
        user_id = message.from_user.id
        warning_message = f"<a href='tg://user?id={user_id}'>@{message.from_user.username}</a> Your message was removed due to the use of insulting language.\n\nPlease ensure messages are respectful and refrain from using offensive language."
        context.bot.send_message(chat_id=message.chat_id, text=warning_message,
                                 parse_mode='HTML')

        # Delete the warning message after 15 seconds
        time.sleep(10)
        context.bot.delete_message(chat_id=message.chat_id,
                                   message_id=message.message_id + 1)  #
        # Adjust the message_id to match the warning message
