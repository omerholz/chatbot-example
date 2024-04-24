FROM python:3.12-slim-bookworm
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y curl


# Install Pulumi
RUN curl -fsSL https://get.pulumi.com | sh

# Set the path
ENV PATH=$PATH:/root/.pulumi/bin

# Copy your Pulumi project files into the container
COPY ../bot /app/bot
COPY ../infra /app/infra
COPY ../docker/scripts/pulumi-client-init.sh /app/scripts/pulumi-client-init.sh
RUN chmod +x /app/scripts/pulumi-client-init.sh

# Set a working directory
WORKDIR /app/infra

## Install Python dependencies
RUN pip install -r requirements.txt

# Start a bash session by default
CMD ["/app/scripts/pulumi-client-init.sh"]
