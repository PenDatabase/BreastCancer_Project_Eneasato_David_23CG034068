# Breast Cancer Prediction System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A production-grade machine learning web application for predicting breast cancer diagnosis (benign or malignant) based on tumor characteristics from the Breast Cancer Wisconsin (Diagnostic) dataset.

> **⚠️ DISCLAIMER**: This system is for **EDUCATIONAL PURPOSES ONLY** and should **NOT** be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project was developed as part of **COS331 - Artificial Intelligence** coursework. It demonstrates:

- Machine learning model development and evaluation
- Model persistence using Joblib
- Web application development with Flask
- Production-grade code structure and documentation
- Deployment-ready configuration

**Algorithm**: Logistic Regression  
**Dataset**: Breast Cancer Wisconsin (Diagnostic)  
**Features**: 5 selected tumor characteristics  
**Target**: Binary classification (Benign/Malignant)

---

## ✨ Features

- **Interactive Web Interface**: User-friendly form for entering tumor measurements
- **Real-time Predictions**: Instant classification results with confidence scores
- **Probability Breakdown**: Visual representation of prediction probabilities
- **Comprehensive Validation**: Input validation with helpful error messages
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Production-Ready**: Structured code with error handling and logging
- **Health Monitoring**: Built-in health check and model info endpoints

---

## 🛠 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0+**: Web framework
- **scikit-learn 1.3+**: Machine learning library
- **NumPy & Pandas**: Data manipulation
- **Joblib**: Model serialization

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript (ES6+)**: Interactive functionality
- **Fetch API**: Asynchronous requests

### Development Tools
- **Jupyter Notebook**: Model development and experimentation
- **Matplotlib & Seaborn**: Data visualization

---

## 📁 Project Structure

```
BreastCancer_Project_yourName_matricNo/
│
├── app.py                          # Flask application (main entry point)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file
├── BreastCancer_hosted_webGUI_link.txt  # Deployment information
│
├── model/                          # Model artifacts directory
│   ├── model_building.ipynb        # Jupyter notebook for model development
│   ├── breast_cancer_model.pkl     # Trained model (generated)
│   ├── scaler.pkl                  # Feature scaler (generated)
│   └── feature_names.pkl           # Feature names (generated)
│
├── templates/                      # HTML templates
│   └── index.html                  # Main web interface
│
└── static/                         # Static files
    └── style.css                   # Stylesheet
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd BreastCancer_Project_yourName_matricNo
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Model

Open and run the Jupyter notebook:

```bash
jupyter notebook model/model_building.ipynb
```

Execute all cells in the notebook to:
- Load and preprocess the dataset
- Train the Logistic Regression model
- Evaluate model performance
- Save model artifacts (`.pkl` files)

---

## 💻 Usage

### Running Locally

1. Ensure the model artifacts exist in the `model/` directory
2. Start the Flask application:

```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

4. Enter tumor feature values in the form
5. Click "Predict Diagnosis" to see the results

### Running in Production

Use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🧠 Model Details

### Algorithm
**Logistic Regression** with the following configuration:
- Solver: `lbfgs`
- Max iterations: 1000
- Class weight: `balanced` (handles class imbalance)
- Random state: 42 (for reproducibility)

### Features Used (5 selected)

1. **Mean Radius**: Mean of distances from center to points on the perimeter
2. **Mean Texture**: Standard deviation of gray-scale values
3. **Mean Perimeter**: Mean size of the core tumor
4. **Mean Compactness**: Perimeter² / Area - 1.0
5. **Mean Concavity**: Severity of concave portions of the contour

### Data Preprocessing

- **Feature Scaling**: StandardScaler (mean=0, std=1)
- **Train-Test Split**: 80-20 with stratification
- **Missing Values**: None found in the dataset

### Model Performance

Typical performance metrics (may vary slightly):

| Metric    | Score  |
|-----------|--------|
| Accuracy  | ~96%   |
| Precision | ~97%   |
| Recall    | ~96%   |
| F1-Score  | ~96%   |
| ROC AUC   | ~0.99  |

### Model Persistence

- **Method**: Joblib
- **Files**: 
  - `breast_cancer_model.pkl`: Trained model
  - `scaler.pkl`: StandardScaler fitted on training data
  - `feature_names.pkl`: Feature names for consistency

---

## 🌐 Deployment

This application can be deployed on various platforms:

### Option 1: Render.com

1. Create a new Web Service on [Render.com](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
4. Deploy

### Option 2: PythonAnywhere.com

1. Upload your project files
2. Create a new web app
3. Configure WSGI file to point to `app.py`
4. Reload the web app

### Option 3: Streamlit Cloud

Convert the Flask app to Streamlit or create a Streamlit version:

```python
import streamlit as st
# Streamlit implementation
```

### Option 4: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Deploy: `vercel --prod`

### Environment Variables

For production, set the following environment variables:

- `FLASK_ENV=production`
- `SECRET_KEY=<your-secret-key>`

---

## 📡 API Documentation

### Endpoints

#### `GET /`
Returns the main web interface.

**Response**: HTML page

---

#### `POST /predict`
Make a prediction based on tumor features.

**Request Body** (JSON):
```json
{
  "mean radius": 14.5,
  "mean texture": 18.2,
  "mean perimeter": 95.3,
  "mean compactness": 0.15,
  "mean concavity": 0.08
}
```

**Success Response** (200):
```json
{
  "success": true,
  "result": {
    "diagnosis": "Benign",
    "prediction_code": 1,
    "confidence": 95.32,
    "probabilities": {
      "malignant": 4.68,
      "benign": 95.32
    },
    "timestamp": "2026-01-21 14:30:45"
  }
}
```

**Error Response** (400):
```json
{
  "success": false,
  "error": "Missing features: mean radius"
}
```

---

#### `GET /health`
Health check endpoint for monitoring.

**Response** (200):
```json
{
  "status": "healthy",
  "model_loaded": true,
  "features": ["mean radius", "mean texture", ...],
  "timestamp": "2026-01-21T14:30:45.123456"
}
```

---

#### `GET /info`
Get information about the model.

**Response** (200):
```json
{
  "project": "Breast Cancer Prediction System",
  "algorithm": "Logistic Regression",
  "persistence_method": "Joblib",
  "features": ["mean radius", "mean texture", ...],
  "feature_count": 5,
  "classes": ["Malignant (0)", "Benign (1)"],
  "disclaimer": "This system is for EDUCATIONAL PURPOSES ONLY"
}
```

---

## 🧪 Testing

Run tests using pytest:

```bash
pytest tests/
```

### Example Test Cases

```python
def test_prediction_endpoint():
    """Test the prediction endpoint"""
    response = client.post('/predict', json={
        "mean radius": 14.5,
        "mean texture": 18.2,
        "mean perimeter": 95.3,
        "mean compactness": 0.15,
        "mean concavity": 0.08
    })
    assert response.status_code == 200
    assert response.json['success'] == True
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**[Your Name]**  
Matric No: [Your Matric Number]  
Course: COS331 - Artificial Intelligence  
Institution: Covenant University

---

## 🙏 Acknowledgments

- **Dataset**: Breast Cancer Wisconsin (Diagnostic) dataset from UCI Machine Learning Repository
- **Framework**: Flask web framework
- **ML Library**: scikit-learn
- **Inspiration**: Educational project for AI coursework

---

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Contact: [your-email@example.com]

---

## 🔒 Security & Privacy

- No user data is stored or transmitted
- All predictions are processed locally
- No external API calls
- HTTPS recommended for production deployment

---

## 📊 Future Enhancements

- [ ] Add more ML algorithms (SVM, Random Forest, Neural Networks)
- [ ] Implement model comparison dashboard
- [ ] Add feature importance visualization
- [ ] Include SHAP/LIME explainability
- [ ] Add user authentication
- [ ] Implement prediction history
- [ ] Add batch prediction capability
- [ ] Create mobile application
- [ ] Add multilingual support

---

**Remember**: This is an educational project. For actual medical diagnosis, always consult qualified healthcare professionals.
