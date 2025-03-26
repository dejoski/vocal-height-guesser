import numpy as np
from sklearn.ensemble import RandomForestRegressor

class HeightPredictor:
    def __init__(self):
        """
        Initialize the height predictor model
        """
        # Create a simple random forest regressor
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        # Since we don't have real training data, we'll use a simple rule-based approach
        # and pretend we have a trained model
        self.is_trained = False
        
    def predict(self, features, gender=None):
        """
        Predict height from voice features
        
        Parameters:
        -----------
        features : dict or numpy.ndarray
            Voice features extracted from audio
        gender : str, optional
            Gender of the speaker ('male' or 'female')
            
        Returns:
        --------
        height : float
            Predicted height in centimeters
        confidence : float
            Confidence level (0-1)
        """
        # Extract fundamental frequency features
        if isinstance(features, dict):
            f0_mean = features.get('f0_mean', 0)
        else:
            # Assuming the first element in the array is f0_mean
            f0_mean = features[0]
        
        # Simple heuristic based on research:
        # Lower voice frequencies typically correlate with taller heights
        # Female avg height range: 155-170 cm, male: 170-185 cm
        
        # Determine gender based on f0 if not provided
        if gender is None:
            # Average male F0: 85-155 Hz, female F0: 165-255 Hz
            gender = 'male' if f0_mean < 160 else 'female'
        
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
        if f0_mean > 0:
            if gender.lower() == 'male':
                # Normalize f0 within expected range
                normalized_f0 = min(max(f0_mean, low_f0), high_f0)
                # Map to height (inversely proportional)
                height_modifier = (high_f0 - normalized_f0) / (high_f0 - low_f0) * 13
                height = base_height + height_modifier - 6.5  # Centered around average
            else:
                # Normalize f0 within expected range
                normalized_f0 = min(max(f0_mean, low_f0), high_f0)
                # Map to height (inversely proportional)
                height_modifier = (high_f0 - normalized_f0) / (high_f0 - low_f0) * 12
                height = base_height + height_modifier - 6  # Centered around average
        else:
            # Default to average height if no f0 detected
            height = base_height
        
        # Ensure height is within reasonable bounds
        height = min(max(height, min_height), max_height)
        
        # Calculate a fake confidence level
        # Higher for values closer to the average
        distance_from_avg = abs(height - base_height) / (max_height - min_height)
        confidence = max(0.5, 1 - distance_from_avg)
        
        # In a real model, we would use all features and a trained model
        # self.model.predict(features)
        
        return round(height, 1), round(confidence, 2)
    
    def predict_with_range(self, features, gender=None):
        """
        Predict height with a confidence range
        
        Returns:
        --------
        height : float
            Predicted height in centimeters
        lower_bound : float
            Lower bound of the confidence interval
        upper_bound : float
            Upper bound of the confidence interval
        """
        height, confidence = self.predict(features, gender)
        
        # Create range based on confidence (lower confidence = wider range)
        range_width = (1 - confidence) * 14 + 2  # Min range of 2 cm, max of 16 cm
        
        lower_bound = height - range_width / 2
        upper_bound = height + range_width / 2
        
        return height, round(lower_bound, 1), round(upper_bound, 1)
    
    @staticmethod
    def cm_to_imperial(cm_value):
        """
        Convert centimeters to feet and inches
        
        Parameters:
        -----------
        cm_value : float
            Height value in centimeters
            
        Returns:
        --------
        feet : int
            Feet component of the height
        inches : float
            Inches component of the height (rounded to 1 decimal)
        total_inches : float
            Total height in inches (rounded to 1 decimal)
        """
        inches_total = cm_value / 2.54
        feet = int(inches_total // 12)
        inches = round(inches_total % 12, 1)
        
        return feet, inches, round(inches_total, 1) 