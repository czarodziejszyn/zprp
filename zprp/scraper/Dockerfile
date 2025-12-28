FROM python:3.11-slim

# Base instalations
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip jq xvfb \
    && rm -rf /var/lib/apt/lists/*

# Add google key
RUN mkdir -p /etc/apt/keyrings && \
    wget -q -O /etc/apt/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    chmod 644 /etc/apt/keyrings/google-linux-signing-key.gpg

# Repo for Google Chrome
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome stable
RUN apt-get update && apt-get install -y google-chrome-stable

# Install Chromedriver from Chrome for Testing
RUN CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+\.\d+") && \
    echo "Detected Chrome: $CHROME_VERSION" && \
    curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json \
      -o /tmp/chrome.json && \
    DRIVER_URL=$(cat /tmp/chrome.json | jq -r ".channels.Stable.downloads.chromedriver[] | select(.platform==\"linux64\") | .url") && \
    echo "Chromedriver URL: $DRIVER_URL" && \
    wget -q $DRIVER_URL -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Python requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Code
COPY . /app
WORKDIR /app

# DISPLAY for Xvfb
ENV DISPLAY=:99

# Run Xvfb and then main.py
CMD Xvfb :99 -screen 0 1920x1080x24 & \
    python main.py
