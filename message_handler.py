from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters
from profanity_filter import filter_messages as profanity_filter_messages
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext


def filter_messages(update, context):
    profanity_filter_messages(update, context)


# Function to forward image to admin with approval buttons

def forward_to_admin(update, context):
    admin_id = 942560773  # Replace with the actual admin's user ID

    message = update.effective_message

    image = message.photo[-1] if message.photo else message.document

    if image:
        try:
            # Get the uploader username
            uploader_username = f"@{message.from_user.username}" if message.from_user.username else "the uploader"
            # Get the user's caption, if any
            user_caption = message.caption if message.caption else ""
            # Create the caption with the uploader username tagged and
            # approval buttons
            caption = f"{user_caption}\n\nPosted by {uploader_username}"

            # Create an inline keyboard with approval and denial buttons
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Approve",
                                         callback_data=f"approve_{message.message_id}"),
                    InlineKeyboardButton("Deny",
                                         callback_data=f"deny_{message.message_id}")
                ]
            ])

            # Send a notification to the user
            notification = f"Hi {uploader_username}, your image is in the approval process and will be posted soon."
            sent_message = context.bot.send_message(chat_id=message.chat_id,
                                                    text=notification)

            # Forward the image to the admin with buttons in the caption
            sent_image = context.bot.send_photo(chat_id=admin_id,
                                                photo=image.file_id,
                                                caption=caption,
                                                reply_markup=keyboard)

            # Delete the uploaded image from the group
            message.delete()

            # Schedule the deletion of the notification message after 30 seconds
            context.job_queue.run_once(delete_notification, 10, context={
                'message_id': sent_message.message_id,
                'chat_id': sent_message.chat_id})

        except Exception as e:
            print("Error occurred:", e)
    else:
        print("No image found in the message")


def delete_notification(context):
    try:
        message_id = context.job.context['message_id']
        chat_id = context.job.context['chat_id']
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except BadRequest as e:
        print("Error deleting message:", e)


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data.split("_")
    action = data[0]  # 'approve' or 'deny'
    message_id = int(data[1])

    if action == "approve":
        group_chat_id = -1002136969189  # Replace with your group's chat ID
        repost_image(context.bot, group_chat_id, query.message)

    # Add logic for denying the image if needed

    # Delete the admin's approval/denial message
    context.bot.delete_message(chat_id=query.message.chat_id,
                               message_id=query.message.message_id)


def repost_image(bot, chat_id, message):
    if message.photo or message.document:
        try:
            # Repost the approved message (image/document) in the group
            forwarded_message = bot.forward_message(chat_id=chat_id,
                                                    from_chat_id=message.chat_id,
                                                    message_id=message.message_id)
        except Exception as e:
            print("Error occurred while reposting:", e)
    else:
        print("No image or document found in the forwarded message")


# Handler for detecting image uploads
image_handler = MessageHandler(
    Filters.photo | Filters.document.category("image"), forward_to_admin)

# Register the handlers

# Message handling functions
profanity_handler = MessageHandler(Filters.text & (~Filters.command),
                                   filter_messages)
