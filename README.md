# Telegram Bot Features

## Profanity Filter

The bot includes a profanity filter to ensure a respectful environment within the group chat When a user sends a message containing offensive language:

- The bot detects the inappropriate content.
- Deletes the offensive message.
- Sends a warning message in the group, tagging the user who posted the offensive content.
- Remove the warning message after a specified time period.

## Image Approval System

The bot incorporates an image approval system to control the posting of images within the group. When a user uploads an image:

- The bot forwards the image to the admin for approval.
- Includes buttons for the admin to approve or deny the image.
- If approved:
    - Reposts the image in the group with the original caption.
    - Tags the uploader's username in the caption.

## Usage

1. **Profanity Filter:**
    - The filter runs automatically. No specific commands are required.
    - Ensure the bot is added to the group where you want to apply the profanity filter.

2. **Image Approval:**
    - Users upload images as usual.
    - Admin receives forwarded images with approval buttons.
    - Admin selects "Approve" or "Deny" as needed.

## Installation

1. Clone the repository.
2. Install necessary dependencies:
    - `python-telegram-bot`
    - `better_profanity`
3. Set up the bot using your API token.
4. Run the bot.

## Dependencies

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): The Python interface for the Telegram Bot API.
- [better_profanity](https://pypi.org/project/better-profanity/): A library for filtering offensive words and phrases.

## Future Enhancements

- **Command Handling:** Implement commands for more interactive bot functionalities.
- **Content Moderation:** Extend content moderation capabilities beyond profanity filtering.
- **User Interaction:** Develop more user engagement features.

## Contributors

- [Khalid Mohammed](https://github.com/pilanop)
