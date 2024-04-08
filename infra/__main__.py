import bot_lambda

# Setup telegram bot
lambda_layer = bot_lambda.setup_lambda_layer()
lambda_iam_role = bot_lambda.setup_iam_role_for_lambda()
lambda_function = bot_lambda.setup_lambda_function(lambda_layer, role=lambda_iam_role)
api = bot_lambda.setup_api_gateway(lambda_function)
bot_lambda.register_webhook(api)
