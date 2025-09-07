# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set timezone (fix time sync issues)
ENV TZ=UTC

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    git ffmpeg tzdata && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements if you have one
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Default command
CMD ["python3", "bot.py"]
