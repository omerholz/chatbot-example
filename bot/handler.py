# bot/handler.py
import asyncio
import json
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot. How can I assist you today?")


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received group message: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a response to a group chat message.")

async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received private message: {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a response to a private message :)")

async def async_lambda_handler(event):
    logger.info("This is an info log")
    logger.info(f"Received event: {event}")
    application = Application.builder().token(TOKEN).build()

    # Register your handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND, handle_group_message))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_private_message))

    # Decode the incoming Telegram message
    if event.get('body'):
        update_dict = json.loads(event['body'])
        async with application:
            update = Update.de_json(update_dict, application.bot)
            await application.process_update(update)


def lambda_handler(event, context):
    logger.info("Received event: %s", event)
    try:
        asyncio.run(async_lambda_handler(event))
    except Exception as e:
        import traceback
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return {'statusCode': 501}

    logger.info("Successfully processed event")
    return {'statusCode': 200}
