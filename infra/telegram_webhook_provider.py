from pulumi.dynamic import ResourceProvider, Resource, CreateResult
import requests

class TelegramWebhookProvider(ResourceProvider):
    def create(self, props):
        webhook_url = props['url']
        token = props['token']
        response = requests.post(f'https://api.telegram.org/bot{token}/setWebhook', json={'url': webhook_url})
        if response.status_code != 200:
            raise Exception(f"Failed to set webhook: {response.text}")
        return CreateResult(id_="-", outs={})

class Webhook(Resource):
    def __init__(self, name, token, url, opts=None):
        super().__init__(TelegramWebhookProvider(), name, {"token": token, "url": url}, opts)
