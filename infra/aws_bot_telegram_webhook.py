import json
import os

import pulumi
import pulumi_aws as aws
from pulumi_aws import iam

from telegram_webhook_provider import Webhook
from utils import install_dependencies_and_prepare_layer, python_version, prepare_code

PY_VER = aws.lambda_.Runtime(python_version)
bot_dir = '../bot'
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')


def setup_lambda_layer(cloud_provider):
    # Define AWS resources
    lambda_layer_zip_file = 'target/dependencies_layer.zip'
    layer_requirements_path = os.path.join(bot_dir, cloud_provider, 'requirements.txt')

    # Prepare the Lambda layer package with dependencies
    install_dependencies_and_prepare_layer(layer_requirements_path, lambda_layer_zip_file)

    zipped_code = pulumi.FileArchive(lambda_layer_zip_file)
    # Create the Lambda layer
    lambda_layer = aws.lambda_.LayerVersion("telegramLambdaLayer",
                                            layer_name="telegram-dependencies-layer",
                                            code=zipped_code,
                                            compatible_runtimes=[PY_VER],
                                            )
    pulumi.export('lambda_layer_arn', lambda_layer.arn)

    return lambda_layer

def setup_iam_role_for_lambda():

    # Create an IAM role for the Lambda function
    role = iam.Role("lambdaRole",
                    assume_role_policy=json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Action": "sts:AssumeRole",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Effect": "Allow"
                        }]
                    }))

    iam.RolePolicyAttachment("lambdaLogs",
                             role=role.name,
                             policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

    return role

def setup_lambda_function(lambda_layer, role):

    # Function code zip (excluding dependencies)
    zip_file = 'target/aws_bot_code.zip'
    prepare_code(bot_dir, zip_file, cloud_provider='aws')

    # Create the Lambda function
    lambda_function = aws.lambda_.Function("TelegramBot",
                                        handler="aws_telegram_handler.lambda_handler",
                                        role=role.arn,
                                        runtime=PY_VER,
                                        code=pulumi.FileArchive(zip_file),
                                        layers=[lambda_layer.arn],
                                        environment=aws.lambda_.FunctionEnvironmentArgs(
                                            variables={
                                                "TELEGRAM_BOT_TOKEN": bot_token
                                            }
                                        ))

    pulumi.export('lambda_function_name', lambda_function.name)

    return lambda_function


def setup_api_gateway(lambda_function):
    # Create the HTTP API Gateway
    api = aws.apigatewayv2.Api("telegramBotApi",
        protocol_type="HTTP",
        route_key="POST /bot",
        target=lambda_function.invoke_arn)


    # Set Lambda permission for API Gateway
    lambda_permission = aws.lambda_.Permission("ApiGatewayPermission",
                                               action="lambda:InvokeFunction",
                                               function=lambda_function.name,
                                               principal="apigateway.amazonaws.com",
                                               source_arn=api.execution_arn.apply(lambda arn: f"{arn}/*/*"))

    # Export the API endpoint URL
    pulumi.export('api_url', api.api_endpoint)

    return api

def register_webhook(api, token_config_key="telegram_bot_token"):
    # Register the Telegram webhook using the full URL including the route
    webhook_url = pulumi.Output.concat(api.api_endpoint, "/bot")
    webhook = Webhook("telegramWebhookRegistration",
                      token=bot_token,
                      url=webhook_url)

    # Export the API endpoint URL including the /bot route
    pulumi.export('api_url_with_bot', webhook_url)

