#!/usr/bin/env python3

import os
import sys
import argparse
import librosa
import matplotlib.pyplot as plt
import numpy as np

# Add current directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feature_extractor import extract_features
from height_predictor import HeightPredictor

def plot_audio_features(audio_path):
    """Plot various audio features for visualization"""
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    
    # Plot waveform
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.title('Waveform')
    librosa.display.waveshow(y, sr=sr)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    
    # Plot spectrogram
    plt.subplot(3, 1, 2)
    plt.title('Spectrogram')
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    
    # Plot Mel Spectrogram
    plt.subplot(3, 1, 3)
    plt.title('Mel Spectrogram')
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Test height prediction from voice')
    parser.add_argument('audio_file', help='Path to audio file to analyze')
    parser.add_argument('--gender', choices=['male', 'female'], help='Specify gender (optional)')
    parser.add_argument('--plot', action='store_true', help='Plot audio features')
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: File '{args.audio_file}' not found.")
        return 1
    
    # Extract features
    print(f"Extracting features from '{args.audio_file}'...")
    features = extract_features(args.audio_file)
    
    # Initialize predictor
    predictor = HeightPredictor()
    
    # Make prediction
    height, lower, upper = predictor.predict_with_range(features, args.gender)
    _, confidence = predictor.predict(features, args.gender)
    
    # Determine detected gender
    detected_gender = "male" if features['f0_mean'] < 160 else "female"
    if args.gender:
        gender_text = f"Provided gender: {args.gender}"
    else:
        gender_text = f"Detected gender: {detected_gender}"
    
    # Print results
    print("\n===== Voice Height Prediction =====")
    print(f"Audio file: {args.audio_file}")
    print(f"Fundamental frequency (F0): {features['f0_mean']:.2f} Hz")
    print(gender_text)
    print(f"Predicted height: {height} cm (range: {lower}-{upper} cm)")
    print(f"Confidence: {confidence*100:.1f}%")
    print("===================================\n")
    
    # Plot features if requested
    if args.plot:
        try:
            plot_audio_features(args.audio_file)
        except Exception as e:
            print(f"Error plotting features: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 