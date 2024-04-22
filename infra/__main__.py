from utils import cloud_provider

if cloud_provider == 'aws':
    import aws_bot_telegram_webhook

    # Setup telegram bot
    lambda_layer = aws_bot_telegram_webhook.setup_lambda_layer(cloud_provider)
    lambda_iam_role = aws_bot_telegram_webhook.setup_iam_role_for_lambda()
    lambda_function = aws_bot_telegram_webhook.setup_lambda_function(lambda_layer, role=lambda_iam_role)
    api = aws_bot_telegram_webhook.setup_api_gateway(lambda_function)
    # Register the webhook
    aws_bot_telegram_webhook.register_webhook(api)

elif cloud_provider == 'gcp':
    import gcp_bot_telegram_webhook

    # Setup telegram bot
    cloud_function = gcp_bot_telegram_webhook.setup_cloud_function(cloud_provider)
    # Register the webhook
    gcp_bot_telegram_webhook.register_webhook(cloud_function)

