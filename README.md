# chatbot-example
An example chatbot demonstrating different tools and technologies.

This repo is accompanied by a blog post that explains how to build a chatbot using different tools and technologies. The blog post is divided into multiple parts. In this part, we will see how to build a simple chatbot using AWS Lambda and Pulumi.
Check out the blog post [here](https://omerholz.com/blog/serverless-telegram-bot/).

## Prerequisites

- Telegram Bot Token
- Pulumi Token
- Docker

### AWS Prerequisites

- AWS Account with Access Key ID and Secret

### Google Cloud Platform Prerequisites

* GCP Service Account with Credentials

## Pulumi and Docker

We use Pulumi to demonstrate and teach IaC using Pulumi, and so we use Pulumi to deploy infrastructure to the cloud. We use Docker to make sure the examples in this repo can work on any environment and to document the environment setup and configuration.

## Multi-Cloud

This project demonstrates using pulumi for multi-cloud deployment. Multi-cloud deployment can be useful to avoid vendor lock-in and allow you to leverage more power when negotiating with cloud providers. Currently multi-cloud is only demonstrated for stateless serverless services, but we intend to add examples for stateful multi-cloud services in the near future

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

Use the `docker/.secrets.env.example` file template to create a `docker/secrets.env`

```bash
cp docker/.secrets.env.example docker/.secrets.env
```

The edit the file with the relevant tokens and secrets

Update the `docker-compose.yml` file then build the image:

```bash
docker compose -f docker/docker-compose.yml build
```

## Deploy

#### AWS

Run your pulumi docker container

```bash
docker compose -f docker/docker-compose.yml run -it --rm pulumi
```

This will get you into the pulumi container where pulumi is installed and configured. Then select the desired Pulumi stack:

```bash
root@8ac05567f4ac:/app/infra# pulumi stack select aws
Logging in using access token from PULUMI_ACCESS_TOKEN
```

Now you are all set to deploy your function to AWS using `pulumi up`

```bash
pulumi up
```

This will deploy the necessary resources to AWS. You're up and running! Give your bot a try.

To take down the resource you deployed you can use 

```bash
pulumi destroy
```

#### GCP

To deploy to GCP, do the same but select the gcp stack before running `pulumi up` and `pulumi destroy`

```bash
docker compose -f docker/docker-compose.yml run -it --rm pulumi
pulumi stack select gcp
pulumi up
```

## Building your own chatbot

You can see how you can easily edit the code in the bot/handler.py file to customize the chatbot. You can add more intents and responses to make the chatbot more intelligent. In the next part of the accounpaning blog post, we will see how to use LLMs to make our bot more chatty and intelligent. Stay tuned!
