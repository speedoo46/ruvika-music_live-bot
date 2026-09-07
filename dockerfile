FROM python:3.11-slim

# Install system dependencies required by pytgcalls (ntgcalls) & WebRTC
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libx11-6 \
    libopus0 \
    libasound2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . .

# Run the bot
CMD ["python", "bot.py"]
