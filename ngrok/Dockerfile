FROM debian:bullseye-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip -o ngrok.zip \
    && unzip ngrok.zip -d /usr/local/bin \
    && rm ngrok.zip

ENTRYPOINT ["ngrok"]
