import numpy as np
import os
import warnings

# Handle librosa import for deployment environments
try:
    import librosa
except ImportError:
    warnings.warn("Librosa not available - feature extraction will be limited")

def extract_features(audio_path, n_mfcc=13, n_mels=40):
    """
    Extract audio features from an audio file
    
    Parameters:
    -----------
    audio_path : str
        Path to the audio file
    n_mfcc : int
        Number of MFCC coefficients to extract
    n_mels : int
        Number of Mel bands to generate
        
    Returns:
    --------
    features : dict
        Dictionary containing extracted features
    """
    # Check if librosa is available
    if 'librosa' not in globals():
        # Provide a default set of features if librosa not available
        return {
            'f0_mean': 120, # Default value, will be auto-detected as male
            'f0_std': 5,
            'f0_min': 110,
            'f0_max': 130,
            'mfcc1_mean': 0.1,
            'mfcc1_std': 0.05,
        }
    
    # Load audio file with librosa
    y, sr = librosa.load(audio_path, sr=None)
    
    # Make sure audio is at least 1 second for reliable feature extraction
    if len(y) < sr:
        y = np.pad(y, (0, sr - len(y)), 'constant')
    
    # Extract features
    features = {}
    
    # Fundamental frequency (F0) using pitch tracking
    f0, voiced_flag, voiced_probs = librosa.pyin(y, 
                                               fmin=librosa.note_to_hz('C2'), 
                                               fmax=librosa.note_to_hz('C7'),
                                               sr=sr)
    f0 = f0[~np.isnan(f0)]  # Remove NaN values
    if len(f0) > 0:
        features['f0_mean'] = np.mean(f0)
        features['f0_std'] = np.std(f0)
        features['f0_min'] = np.min(f0)
        features['f0_max'] = np.max(f0)
    else:
        features['f0_mean'] = 0
        features['f0_std'] = 0
        features['f0_min'] = 0
        features['f0_max'] = 0
    
    # Extract MFCCs (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    for i in range(n_mfcc):
        features[f'mfcc{i+1}_mean'] = np.mean(mfccs[i])
        features[f'mfcc{i+1}_std'] = np.std(mfccs[i])
    
    # Mel spectrogram features
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    features['mel_mean'] = np.mean(mel_spec_db)
    features['mel_std'] = np.std(mel_spec_db)
    
    # Spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    features['spectral_centroid_mean'] = np.mean(spectral_centroid)
    features['spectral_centroid_std'] = np.std(spectral_centroid)
    
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
    features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
    
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
    features['spectral_rolloff_std'] = np.std(spectral_rolloff)
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_std'] = np.std(zcr)
    
    # Amplitude envelope (RMS energy)
    rms = librosa.feature.rms(y=y)[0]
    features['rms_mean'] = np.mean(rms)
    features['rms_std'] = np.std(rms)
    
    return features

def features_to_vector(features):
    """
    Convert features dictionary to a vector for model input
    """
    # Define the expected features in a specific order
    expected_features = [
        'f0_mean', 'f0_std', 'f0_min', 'f0_max',
        'spectral_centroid_mean', 'spectral_centroid_std',
        'spectral_bandwidth_mean', 'spectral_bandwidth_std',
        'spectral_rolloff_mean', 'spectral_rolloff_std',
        'zcr_mean', 'zcr_std',
        'rms_mean', 'rms_std',
        'mel_mean', 'mel_std'
    ]
    
    # Add MFCC features
    for i in range(13):
        expected_features.append(f'mfcc{i+1}_mean')
        expected_features.append(f'mfcc{i+1}_std')
    
    # Create vector
    vector = np.array([features.get(feature, 0) for feature in expected_features])
    return vector 