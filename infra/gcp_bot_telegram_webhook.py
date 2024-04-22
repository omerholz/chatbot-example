import pulumi
import pulumi_aws as aws
import pulumi_gcp as gcp
from pulumi import Config

from telegram_webhook_provider import Webhook
from utils import python_version, prepare_code

PY_VER = aws.lambda_.Runtime(python_version)
bot_dir = '../bot'
config = Config()
bucket_name = config.require("telegram-bot-bucket")
pulumi.log.info(f'bucket_name {bucket_name}')
bot_token = pulumi.Config().require_secret("telegram_bot_token")
region = config.require('region')

def setup_cloud_function(cloud_provider):
    zip_file = 'target/gcp_bot_code.zip'
    prepare_code(bot_dir, zip_file, cloud_provider=cloud_provider)
    # GCP Storage Bucket
    bucket = gcp.storage.Bucket(
        bucket_name,
        location=region,
    )
    pulumi.export('bucketSelfLink', bucket.self_link)

    # Upload the zipped file to the bucket
    bucket_object = gcp.storage.BucketObject("zipped-bot",
                                             bucket=bucket.name,
                                             source=pulumi.FileAsset(zip_file),
                                             )

    # Deploy the Cloud Function
    function = gcp.cloudfunctions.Function("telegram-bot-function",
                                           source_archive_bucket=bucket.name,
                                           source_archive_object=bucket_object.name,
                                           entry_point="cloud_function_handler",
                                           runtime="python312",
                                           # Ensure this is the correct version as supported by GCP
                                           trigger_http=True,
                                           available_memory_mb=128,
                                           region=region,
                                           environment_variables={
                                               "TELEGRAM_BOT_TOKEN": bot_token,
                                           },
                                           )

    # Add IAM policy binding to allow public access
    public_access_binding = gcp.cloudfunctions.FunctionIamMember(
        "telegram-bot-function-public-invoker",
        cloud_function=function.name,
        project=function.project,
        region=function.region,
        role="roles/cloudfunctions.invoker",
        member="allUsers",
    )

    pulumi.export('cloud_function_url', function.https_trigger_url)

    return function


def register_webhook(function, token_config_key="telegram_bot_token"):
    # Register the Telegram webhook using the full URL including the route
    webhook_url = pulumi.Output.concat(function.https_trigger_url, "/bot")
    webhook = Webhook("telegramWebhookRegistration",
                      token=pulumi.Config().require_secret(token_config_key),
                      url=webhook_url)

    # Export the API endpoint URL including the /bot route
    pulumi.export('api_url_with_bot', webhook_url)

