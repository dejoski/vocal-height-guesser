FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY height_guesser/ ./height_guesser/

# Set the environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=height_guesser/app.py

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "height_guesser/app.py"] 