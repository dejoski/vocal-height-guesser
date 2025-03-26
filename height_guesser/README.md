# Voice-based Height Guesser

A simple web application that predicts a person's height based on voice characteristics.

## Overview

This application extracts acoustic features from voice recordings and uses them to predict the speaker's height. It provides a user-friendly web interface for uploading or recording audio and displays the predicted height with a confidence range.

## Features

- Voice recording directly in the browser
- Audio file upload support (.wav, .mp3, .ogg, .flac, .m4a)
- Real-time audio processing using librosa
- Height prediction with confidence range
- Gender-specific predictions

## Technical Details

The application uses:
- **Flask** for the web server
- **Librosa** for audio feature extraction
- **scikit-learn** for model implementation
- **Web Audio API** for browser recording

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`

## How it works

1. The application extracts acoustic features from the voice sample, including:
   - Fundamental frequency (F0)
   - Mel-frequency cepstral coefficients (MFCCs)
   - Spectral features (centroid, bandwidth, rolloff)
   - Zero-crossing rate
   - Energy features (RMS)

2. These features are analyzed to predict height, using knowledge from research that shows correlations between voice characteristics and physical attributes.

3. The prediction is displayed with a confidence range to acknowledge the inherent uncertainty in this type of estimation.

## Limitations

This is a demonstration application and has several limitations:
- The model is based on general voice-height correlations and not trained on a large dataset
- Predictions may be less accurate for voices with unusual characteristics
- Background noise can affect the accuracy of predictions
- The relationship between voice and height is not deterministic

## Future Improvements

- Training on a large dataset like HeightCeleb or TIMIT
- Adding more sophisticated machine learning models
- Improving noise reduction techniques
- Handling more types of voice inputs (different languages, accents, etc.) 