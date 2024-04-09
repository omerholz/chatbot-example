# chatbot-example
An example chatbot demonstrating different tools and technologies.

This repo is accompanied by a blog post that explains how to build a chatbot using different tools and technologies. The blog post is divided into multiple parts. In this part, we will see how to build a simple chatbot using AWS Lambda and Pulumi.
Check out the blog post [here](https://omerholz.com/blog/serverless-telegram-bot/).

## Prerequisites

- Python 3.12
- AWS Account
- [AWS CLI installed and configured](https://github.com/aws/aws-cli)
- [Pulumi CLI installed and configured](https://www.pulumi.com/docs/install/)
- Telegram Bot Token

## Setup

Clone the repository and cd into the infra directory.

Set your Telegram Bot Token as a Pulumi secret.

```bash
pulumi config set --secret telegram_bot_token <YOUR_TELEGRAM_BOT_TOKEN> 
```

## Deploy

Run the following command to deploy the infrastructure.

```bash
pulumi up
```

Pulumi will diagnose the stack and prompt you to confirm the deployment. Type `yes` and hit enter. That's it! Pulumi will deploy the infrastructure and output the URL of the API Gateway. At this point your chatbot is up and running. Try and talk to it!

## Clean up

To clean up the resources, run the following command.

```bash
pulumi destroy
```

## Building your own chatbot

You can see how you can easily edit the code in the bot/handler.py file to customize the chatbot. You can add more intents and responses to make the chatbot more intelligent. In the next part of the accounpaning blog post, we will see how to use LLMs to make our bot more chatty and intelligent. Stay tuned!
