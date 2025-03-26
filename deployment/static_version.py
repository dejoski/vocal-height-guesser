import os
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, 
    template_folder='../height_guesser/templates',
    static_folder='../height_guesser/static'
)

# Simple height prediction based on frequency values
def predict_height(frequency, gender=None):
    """Simple height prediction without audio processing"""
    # Default values
    if gender is None:
        gender = 'male' if frequency < 160 else 'female'
    
    # Base height ranges by gender
    if gender.lower() == 'male':
        base_height = 177  # Average male height
        min_height = 164
        max_height = 190
        # Frequency ranges
        low_f0 = 85
        high_f0 = 155
    else:  # female
        base_height = 164  # Average female height
        min_height = 152
        max_height = 176
        # Frequency ranges
        low_f0 = 165
        high_f0 = 255
    
    # Invert the relationship (lower frequency -> taller)
    if frequency > 0:
        if gender.lower() == 'male':
            # Normalize f0 within expected range
            normalized_f0 = min(max(frequency, low_f0), high_f0)
            # Map to height (inversely proportional)
            height_modifier = (high_f0 - normalized_f0) / (high_f0 - low_f0) * 13
            height = base_height + height_modifier - 6.5  # Centered around average
        else:
            # Normalize f0 within expected range
            normalized_f0 = min(max(frequency, low_f0), high_f0)
            # Map to height (inversely proportional)
            height_modifier = (high_f0 - normalized_f0) / (high_f0 - low_f0) * 12
            height = base_height + height_modifier - 6  # Centered around average
    else:
        # Default to average height if no f0 detected
        height = base_height
    
    # Ensure height is within reasonable bounds
    height = min(max(height, min_height), max_height)
    
    # Calculate a confidence level
    distance_from_avg = abs(height - base_height) / (max_height - min_height)
    confidence = max(0.5, 1 - distance_from_avg)
    
    # Create range based on confidence
    range_width = (1 - confidence) * 14 + 2  # Min range of 2 cm, max of 16 cm
    lower_bound = height - range_width / 2
    upper_bound = height + range_width / 2
    
    return round(height, 1), round(lower_bound, 1), round(upper_bound, 1), round(confidence, 2)

def cm_to_imperial(cm_value):
    """Convert centimeters to feet and inches"""
    inches_total = cm_value / 2.54
    feet = int(inches_total // 12)
    inches = round(inches_total % 12, 1)
    return feet, inches, round(inches_total, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_height_endpoint():
    try:
        # For static version, accept frequency directly
        if 'frequency' in request.form:
            frequency = float(request.form.get('frequency'))
        else:
            # Default value if no frequency provided
            frequency = 120  # Default male voice frequency
        
        # Get gender if provided
        gender = request.form.get('gender')
        
        # Predict height
        height, lower_bound, upper_bound, confidence = predict_height(frequency, gender)
        
        # Convert to imperial
        feet, inches, total_inches = cm_to_imperial(height)
        lower_feet, lower_inches, _ = cm_to_imperial(lower_bound)
        upper_feet, upper_inches, _ = cm_to_imperial(upper_bound)
        
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
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Export app for deployment
application = app 