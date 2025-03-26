# Voice-based Height Guesser

A web application that predicts a person's height based on their voice characteristics.

## Overview

This project implements a machine learning approach to guess someone's height by analyzing their voice. It extracts acoustic features from audio recordings and uses a model to predict height with a confidence range.

## Quick Start

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python run_height_guesser.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000`
5. Upload or record your voice and see the height prediction

## How It Works

The application works by:
1. Extracting acoustic features from voice recordings (pitch, timbre, etc.)
2. Analyzing those features with a model that understands the relationship between voice characteristics and height
3. Providing a height prediction with a confidence range

## Features

- Browser-based voice recording
- Audio file upload support
- Real-time audio analysis
- Height prediction with confidence range
- Gender-specific adjustments
- Mobile-friendly UI
- Results in both metric (cm) and imperial (feet/inches) units

## Requirements

- Python 3.7+
- Flask
- Librosa
- NumPy
- scikit-learn
- SoundDevice
- matplotlib
- SoundFile

## Project Structure

```
height-guesser/
├── height_guesser/           # Application directory
│   ├── app.py                # Main Flask application
│   ├── feature_extractor.py  # Voice feature extraction
│   ├── height_predictor.py   # Height prediction model
│   ├── requirements.txt      # Python dependencies
│   ├── run.py                # Application runner
│   ├── test_prediction.py    # Command-line testing tool
│   ├── wsgi.py               # WSGI entry point for deployment
│   ├── static/               # Static files (CSS, JS)
│   └── templates/            # HTML templates
│       └── index.html        # Main UI template
├── deployment/               # Deployment-related files
│   ├── Dockerfile            # For Docker-based deployments
│   ├── docker-compose.yml    # For Docker Compose deployments
│   ├── Procfile              # For Heroku deployments
│   └── README.md             # Deployment instructions
├── requirements.txt          # Project dependencies for deployment
├── vercel.json               # Configuration for Vercel deployment
└── run_height_guesser.py     # Main startup script
```

## Testing from Command Line

You can also test the height prediction from the command line:

```
cd height_guesser
python test_prediction.py path/to/audio_file.wav --gender male --plot
```

## Deployment

This application can be deployed to various platforms:

1. **Vercel**: Simple serverless deployment (see vercel.json)
   ```
   npm install -g vercel
   vercel login
   vercel
   ```

2. **Heroku**: Easy deployment with Git
   ```
   heroku create
   git push heroku main
   ```

3. **Docker**: For more control and better audio processing support
   ```
   docker build -t voice-height-guesser -f deployment/Dockerfile .
   docker run -p 5000:5000 voice-height-guesser
   ```

4. **PythonAnywhere**: Good for Python web apps

See the [deployment README](deployment/README.md) for detailed deployment instructions.

## Limitations

This is a demonstration application with several limitations:
- Predictions are based on general voice-height correlations, not a comprehensive trained model
- Background noise can affect prediction accuracy
- Voice disguise or altered speech patterns may lead to inaccurate results

## Future Improvements

- Training on datasets like HeightCeleb or TIMIT
- Implementing more sophisticated machine learning models
- Adding noise reduction techniques
- Supporting more languages and accents 