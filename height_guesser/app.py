import os
import uuid
import tempfile
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import soundfile as sf
import numpy as np
import io

from feature_extractor import extract_features
from height_predictor import HeightPredictor

app = Flask(__name__)

# For Vercel deployment, use /tmp directory which is writable in serverless environments
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join('/tmp', 'height_guesser_uploads'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize our height predictor
height_predictor = HeightPredictor()

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'webm'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_height():
    # Check if the request has a file
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    
    # If no file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Please upload one of: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Get gender if provided
    gender = request.form.get('gender')
    
    # Save file with a secure name to avoid file path manipulation
    filename = str(uuid.uuid4()) + os.path.splitext(secure_filename(file.filename))[1]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Extract features
        features = extract_features(filepath)
        
        # Get prediction
        height, lower_bound, upper_bound = height_predictor.predict_with_range(features, gender)
        
        # Get confidence
        _, confidence = height_predictor.predict(features, gender)
        
        # Convert to imperial measurements
        feet, inches, total_inches = height_predictor.cm_to_imperial(height)
        lower_feet, lower_inches, lower_total_inches = height_predictor.cm_to_imperial(lower_bound)
        upper_feet, upper_inches, upper_total_inches = height_predictor.cm_to_imperial(upper_bound)
        
        # Format imperial strings
        imperial_height = f"{feet}'{inches}\""
        imperial_range = f"{lower_feet}'{lower_inches}\" - {upper_feet}'{upper_inches}\""
        
        # Prepare result
        result = {
            'height': height,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'confidence': confidence,
            'unit': 'cm',
            'imperial': {
                'height': imperial_height,
                'total_inches': total_inches,
                'range': imperial_range
            }
        }
        
        # Clean up the temporary file
        try:
            os.remove(filepath)
        except:
            # Ignore errors removing temp files in serverless environments
            pass
        
        return jsonify(result)
    
    except Exception as e:
        # Clean up the temporary file if it exists
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            # Ignore errors removing temp files in serverless environments
            pass
        
        # Return error
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Export app for Vercel
application = app 