# bot/lambda_handler.py
import asyncio
import json
import logging

from bot.telegram_handler import handle_webhook

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info("Received event: %s", event)
    try:
        if event.get('body'):
            event_json_body = json.loads(event['body'])
            asyncio.run(handle_webhook(event_json_body))
    except Exception as e:
        import traceback
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return {'statusCode': 501}

    logger.info("Successfully processed event")
    return {'statusCode': 200}
