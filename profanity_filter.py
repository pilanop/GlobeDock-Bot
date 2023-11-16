import re
from telegram import Update
from telegram.ext import CallbackContext
from better_profanity import profanity
import time

# Custom array of words to be added to the filter
custom_words = ['tebeda', 'wesha', 'jela',
                'dedeb', 'ahya', 'shermuta',
                'koletam', 'kolet', 'tnbatam',
                'gmatam', 'Enaten', 'ደደብ',
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
        time.sleep(15)
        context.bot.delete_message(chat_id=message.chat_id,
                                   message_id=message.message_id + 1)  #
        # Adjust the message_id to match the warning message

    # Check if the message contains a URL
    if contains_url(message.text):
        # Check if the user is an admin or if it's a YouTube link
        if not is_admin(context.bot,
                        message.from_user.id) and not is_youtube_link(
                message.text):
            # Delete the message with the URL
            message.delete()

            # Notify the user and tag them
            user_id = message.from_user.id
            warning_message = f"<a href='tg://user?id={user_id}'>@{message.from_user.username}</a> Your message was removed because it contains a link.\n\nPlease avoid sharing links except for YouTube videos."
            context.bot.send_message(chat_id=message.chat_id,
                                     text=warning_message, parse_mode='HTML')

            # Delete the warning message after 10 seconds
            context.job_queue.run_once(delete_warning, 10, context={
                'chat_id': message.chat_id,
                'message_id': message.message_id + 1
                # Adjusted message_id for the warning message
            })


def delete_warning(context: CallbackContext):
    chat_id = context.job.context['chat_id']
    message_id = context.job.context['message_id']

    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting warning message: {e}")


def contains_url(text):
    # Regular expression to detect URLs
    url_pattern = (r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%['
                   r'0-9a-fA-F][0-9a-fA-F]))+')
    return re.search(url_pattern, text)


def is_admin(bot, chat_id, user_id):
    try:
        # Get chat member information
        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)

        # Check if the user is an administrator
        if chat_member.status == 'administrator' or chat_member.status == 'creator':
            return True
    except Exception as e:
        print(f"Error checking admin status: {e}")

    return False


def is_youtube_link(text):
    # Check if the URL is from YouTube
    return 'youtube.com' in text or 'youtu.be' in text
