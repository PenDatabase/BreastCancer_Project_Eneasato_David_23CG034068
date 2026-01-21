"""
Breast Cancer Prediction System - Flask Web Application
========================================================

A production-grade web application for predicting breast cancer diagnosis
using a pre-trained Logistic Regression model.

Author: David Eneasato
Matric No: 23CG034068
Algorithm: Logistic Regression
Persistence: Joblib

DISCLAIMER: This system is for EDUCATIONAL PURPOSES ONLY and should NOT 
be used for actual medical diagnosis.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JSON_SORT_KEYS'] = False

# Configuration
MODEL_DIR = Path(__file__).parent / 'model'
MODEL_PATH = MODEL_DIR / 'breast_cancer_model.pkl'
SCALER_PATH = MODEL_DIR / 'scaler.pkl'
FEATURE_NAMES_PATH = MODEL_DIR / 'feature_names.pkl'

# Global variables for model artifacts
model = None
scaler = None
feature_names = None

# Feature metadata for validation and display
FEATURE_METADATA = {
    'mean radius': {
        'display_name': 'Mean Radius',
        'description': 'Mean of distances from center to points on the perimeter',
        'unit': 'units',
        'min': 0,
        'max': 50,
        'typical_range': (6.0, 28.0)
    },
    'mean texture': {
        'display_name': 'Mean Texture',
        'description': 'Standard deviation of gray-scale values',
        'unit': 'units',
        'min': 0,
        'max': 50,
        'typical_range': (9.0, 40.0)
    },
    'mean perimeter': {
        'display_name': 'Mean Perimeter',
        'description': 'Mean size of the core tumor',
        'unit': 'units',
        'min': 0,
        'max': 200,
        'typical_range': (43.0, 188.0)
    },
    'mean compactness': {
        'display_name': 'Mean Compactness',
        'description': 'Perimeter² / Area - 1.0',
        'unit': 'units',
        'min': 0,
        'max': 1,
        'typical_range': (0.02, 0.35)
    },
    'mean concavity': {
        'display_name': 'Mean Concavity',
        'description': 'Severity of concave portions of the contour',
        'unit': 'units',
        'min': 0,
        'max': 1,
        'typical_range': (0.0, 0.43)
    }
}


class ModelLoadError(Exception):
    """Custom exception for model loading errors"""
    pass


class PredictionError(Exception):
    """Custom exception for prediction errors"""
    pass


def load_model_artifacts():
    """
    Load the trained model, scaler, and feature names from disk.
    
    Returns:
        tuple: (model, scaler, feature_names)
        
    Raises:
        ModelLoadError: If any model artifact cannot be loaded
    """
    try:
        logger.info("Loading model artifacts...")
        
        # Check if files exist
        if not MODEL_PATH.exists():
            raise ModelLoadError(f"Model file not found: {MODEL_PATH}")
        if not SCALER_PATH.exists():
            raise ModelLoadError(f"Scaler file not found: {SCALER_PATH}")
        if not FEATURE_NAMES_PATH.exists():
            raise ModelLoadError(f"Feature names file not found: {FEATURE_NAMES_PATH}")
        
        # Load artifacts
        loaded_model = joblib.load(MODEL_PATH)
        loaded_scaler = joblib.load(SCALER_PATH)
        loaded_features = joblib.load(FEATURE_NAMES_PATH)
        
        logger.info(f"✓ Model loaded successfully from {MODEL_PATH}")
        logger.info(f"✓ Scaler loaded successfully from {SCALER_PATH}")
        logger.info(f"✓ Feature names loaded: {loaded_features}")
        
        return loaded_model, loaded_scaler, loaded_features
        
    except Exception as e:
        logger.error(f"Error loading model artifacts: {str(e)}")
        raise ModelLoadError(f"Failed to load model artifacts: {str(e)}")


def validate_input_features(features_dict):
    """
    Validate input features for prediction.
    
    Args:
        features_dict (dict): Dictionary of feature names and values
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not features_dict:
        return False, "No features provided"
    
    # Check if all required features are present
    missing_features = set(feature_names) - set(features_dict.keys())
    if missing_features:
        return False, f"Missing features: {', '.join(missing_features)}"
    
    # Validate each feature value
    for feature_name, value in features_dict.items():
        if feature_name not in FEATURE_METADATA:
            return False, f"Unknown feature: {feature_name}"
        
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            return False, f"Invalid value for {feature_name}: must be a number"
        
        # Check range
        metadata = FEATURE_METADATA[feature_name]
        if float_value < metadata['min'] or float_value > metadata['max']:
            return False, (f"{metadata['display_name']} must be between "
                          f"{metadata['min']} and {metadata['max']}")
        
        # Warning for values outside typical range (not an error)
        if not (metadata['typical_range'][0] <= float_value <= metadata['typical_range'][1]):
            logger.warning(f"{feature_name} value {float_value} is outside typical range "
                         f"{metadata['typical_range']}")
    
    return True, None


def make_prediction(features_dict):
    """
    Make a prediction using the loaded model.
    
    Args:
        features_dict (dict): Dictionary of feature names and values
        
    Returns:
        dict: Prediction results including diagnosis and probability
        
    Raises:
        PredictionError: If prediction fails
    """
    try:
        # Validate inputs
        is_valid, error_message = validate_input_features(features_dict)
        if not is_valid:
            raise PredictionError(error_message)
        
        # Create feature array in correct order
        feature_values = [float(features_dict[feature]) for feature in feature_names]
        X = np.array([feature_values])
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        
        # Map prediction to diagnosis
        diagnosis = 'Benign' if prediction == 1 else 'Malignant'
        confidence = probabilities[prediction] * 100
        
        result = {
            'diagnosis': diagnosis,
            'prediction_code': int(prediction),
            'confidence': round(confidence, 2),
            'probabilities': {
                'malignant': round(probabilities[0] * 100, 2),
                'benign': round(probabilities[1] * 100, 2)
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.info(f"Prediction made: {diagnosis} (confidence: {confidence:.2f}%)")
        return result
        
    except PredictionError:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise PredictionError(f"Failed to make prediction: {str(e)}")


# Flask Routes

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', 
                         features=FEATURE_METADATA,
                         feature_names=feature_names)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    
    Expected JSON payload:
    {
        "mean radius": 14.5,
        "mean texture": 18.2,
        "mean perimeter": 95.3,
        "mean compactness": 0.15,
        "mean concavity": 0.08
    }
    
    Returns:
        JSON response with prediction results or error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Make prediction
        result = make_prediction(data)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
        
    except PredictionError as e:
        logger.warning(f"Prediction validation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please try again.'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check if model is loaded
        if model is None or scaler is None or feature_names is None:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Model not loaded'
            }), 503
        
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'features': feature_names,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


@app.route('/info', methods=['GET'])
def model_info():
    """Provide information about the model"""
    return jsonify({
        'project': 'Breast Cancer Prediction System',
        'algorithm': 'Logistic Regression',
        'persistence_method': 'Joblib',
        'features': feature_names,
        'feature_count': len(feature_names),
        'classes': ['Malignant (0)', 'Benign (1)'],
        'disclaimer': 'This system is for EDUCATIONAL PURPOSES ONLY'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# Application initialization

def initialize_app():
    """Initialize the application by loading model artifacts"""
    global model, scaler, feature_names
    
    try:
        logger.info("Initializing Breast Cancer Prediction System...")
        model, scaler, feature_names = load_model_artifacts()
        logger.info("✓ Application initialized successfully")
        return True
        
    except ModelLoadError as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        logger.error("Please ensure the model files exist in the 'model' directory")
        return False


if __name__ == '__main__':
    # Initialize the application
    if not initialize_app():
        logger.error("Application initialization failed. Exiting.")
        sys.exit(1)
    
    # Run the Flask app
    logger.info("Starting Flask application...")
    logger.info("=" * 60)
    logger.info("Breast Cancer Prediction System")
    logger.info("DISCLAIMER: For Educational Purposes Only")
    logger.info("=" * 60)
    
    # Development server settings
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=False  # Set to False in production
    )
