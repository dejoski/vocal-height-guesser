FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=height_guesser/app.py
ENV PORT=5000

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the application
CMD gunicorn --bind 0.0.0.0:${PORT} height_guesser.app:app 