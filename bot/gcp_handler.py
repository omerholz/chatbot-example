# bot/gcp_handler.py
import asyncio
import json
import logging
import functions_framework


from bot.telegram_handler import handle_webhook

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@functions_framework.http
def cloud_function_handler(request):
    logger.info("Received event: %s", request)
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            request_json = request.get_json(silent=True)
            asyncio.run(handle_webhook(request_json))
        except Exception as e:
            import traceback
            logger.error(f"An error occurred: {str(e)}")
            logger.error(traceback.format_exc())
            return {'statusCode': 501}

    logger.info("Successfully processed event")
    return 'Success', 200
