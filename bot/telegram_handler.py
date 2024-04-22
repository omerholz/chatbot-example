# bot/telgram_handler.py
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot. How can I assist you today?")


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received group message: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a response to a group chat message.")

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received private message: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a response to a private message :)")


async def handle_webhook(post_json_body: dict) -> None:
    logger.info("Telegram handle_webhook received a message. Processing...")
    application = Application.builder().token(TOKEN).build()

    # Register your handlers
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND, handle_group_message))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_private_message))

    # Decode the incoming Telegram message
    async with application:
        update = Update.de_json(post_json_body, application.bot)
        await application.process_update(update)