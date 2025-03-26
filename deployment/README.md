# Voice Height Guesser - Deployment Options

This directory contains files for deploying the Voice Height Guesser application to various platforms.

## Deployment Options

### 1. Vercel (Serverless)

Deploy to Vercel using their serverless platform:

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

Note: Audio processing might be limited on Vercel due to serverless constraints.

### 2. Heroku

Deploy to Heroku:

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create voice-height-guesser

# Initialize Git repository if not already done
git init
git add .
git commit -m "Initial commit"

# Set the remote and push to Heroku
heroku git:remote -a voice-height-guesser
git push heroku main
```

### 3. Docker Container (for Cloud Run, Render, Digital Ocean, etc.)

Build and run using Docker:

```bash
# Build the Docker image
docker build -t voice-height-guesser -f deployment/Dockerfile .

# Run the container
docker run -p 5000:5000 voice-height-guesser
```

### 4. Docker Compose

Run using Docker Compose:

```bash
# Start the application
docker-compose -f deployment/docker-compose.yml up

# Stop the application
docker-compose -f deployment/docker-compose.yml down
```

### 5. PythonAnywhere

1. Create a PythonAnywhere account
2. Upload your code or clone from Git
3. Set up a virtual environment with your dependencies
4. Configure a web app pointing to the `wsgi.py` file

## Environment Variables

The application uses the following environment variables:

- `FLASK_ENV`: Set to 'production' for production deployments
- `UPLOAD_FOLDER`: Directory for temporary file uploads (default: /tmp/height_guesser_uploads)

## Troubleshooting

If you encounter issues with audio processing libraries:

1. Ensure libsndfile is installed on the server
2. Check if FFmpeg is available for audio conversion
3. Some platforms might need custom buildpacks for audio processing 