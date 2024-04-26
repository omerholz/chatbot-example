FROM python:3.12-slim-bookworm

# Set a working directory
WORKDIR /app/infra
RUN python3.12 -m venv .venv
RUN .venv/bin/pip install --upgrade pip
RUN apt-get update && apt-get install -y curl

# Install Pulumi
RUN curl -fsSL https://get.pulumi.com | sh

# Set the path
ENV PATH="/root/.pulumi/bin:/app/infra/.venv/bin:$PATH"

## Install Python dependencies
COPY infra/requirements.txt /app/infra/requirements.txt
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt
# Copy the Pulumi client init script
COPY docker/scripts/pulumi-client-init.sh /app/scripts/pulumi-client-init.sh
RUN chmod +x /app/scripts/pulumi-client-init.sh

# Copy your Pulumi project files into the container
COPY bot /app/bot
COPY infra /app/infra

# Start a bash session by default
CMD ["/app/scripts/pulumi-client-init.sh"]
