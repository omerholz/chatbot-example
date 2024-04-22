# bot/main.py
import asyncio
import json
import logging
import functions_framework
import google.cloud.logging



from .telegram_handler import handle_webhook

# Enable logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
client = google.cloud.logging.Client()
client.setup_logging()

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
