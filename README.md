# chatbot-example
An example chatbot demonstrating different tools and technologies.

This repo is accompanied by a blog post that explains how to build a chatbot using different tools and technologies. The blog post is divided into multiple parts. In this part, we will see how to build a simple chatbot using AWS Lambda and Pulumi.
Check out the blog post [here](https://omerholz.com/blog/serverless-telegram-bot/).

## Prerequisites

- Python 3.12
- AWS Account
- [Pulumi CLI installed and configured](https://www.pulumi.com/docs/install/)
- Telegram Bot Token

### AWS Prerequisites

- [AWS CLI installed, configured and logged in](https://github.com/aws/aws-cli)

### Google Cloud Platform Prerequisites

* [GCP gcloud CLI Installed configured and logged in](https://cloud.google.com/sdk/docs/install)
* gcloud CLI and the service account you use must have all the required permissions to the project and the APIs



## Multi-Cloud

This project demonstrates using pulumi for multi-cloud deployment. Multi-cloud deployment can be useful to avoid vendor lock-in and allow you to leverage more power when negotiating with cloud providers. Currently multi-cloud is only demonstrated for stateless serverless services, but we intend to add examples for stateful multi-cloud services in the near future

## Setup

Clone the repository and cd into the infra directory.

```bash
git clone git@github.com:omerholz/chatbot-example.git
cd chatbot-example
```

Create a pulumi stack. We recommend creating a separate stack for each cloud provider and env

```bash
pulumi stack init gcp-dev
pulumi stack init aws-dev
```

Select the stack and set relevant configuration values

```bash
pulumi stack select aws-dev
pulumi config set cloud_provider aws
pulumi config set aws:region <region>
```

```bash
pulumi stack select gcp-dev
pulumi config set cloud_provider gcp
pulumi config set gcp:project <project_id>
pulumi config set region <region>
pulumi config set telegram-bot-bucket <bucket>
```

Set your Telegram Bot Token as a Pulumi secret for both stacks:

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
