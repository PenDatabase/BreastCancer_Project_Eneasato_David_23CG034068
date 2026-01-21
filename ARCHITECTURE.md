# PROJECT ARCHITECTURE
# Breast Cancer Prediction System

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (Browser)                     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │               index.html + style.css                        │   │
│  │  • Input Form (5 tumor features)                           │   │
│  │  • Real-time Validation                                    │   │
│  │  • Results Display                                         │   │
│  │  • Probability Visualization                               │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              │ HTTP Request (JSON)                  │
│                              ▼                                      │
└──────────────────────────────────────────────────────────────────────┘
                               │
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                      FLASK WEB SERVER (app.py)                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Routes & Controllers                                        │  │
│  │  • GET  /        → Serve web interface                      │  │
│  │  • POST /predict → Make prediction                          │  │
│  │  • GET  /health  → Health check                             │  │
│  │  • GET  /info    → Model information                        │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Input Validation Layer                                      │  │
│  │  • Feature validation                                        │  │
│  │  • Range checking                                           │  │
│  │  • Type conversion                                          │  │
│  │  • Error handling                                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Prediction Service                                          │  │
│  │  • Load model artifacts                                      │  │
│  │  • Feature scaling                                          │  │
│  │  • Make prediction                                          │  │
│  │  • Calculate probabilities                                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
└──────────────────────────────────────────────────────────────────────┘
                               │
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                    MODEL ARTIFACTS (model/)                          │
│                                                                      │
│  ┌──────────────────────┐  ┌──────────────────────┐               │
│  │ breast_cancer_       │  │ scaler.pkl           │               │
│  │ model.pkl            │  │                      │               │
│  │                      │  │ StandardScaler       │               │
│  │ Logistic Regression  │  │ (mean=0, std=1)     │               │
│  │ • 5 features         │  │                      │               │
│  │ • Binary classifier  │  │ Fitted on training  │               │
│  │ • Balanced weights   │  │ data                │               │
│  └──────────────────────┘  └──────────────────────┘               │
│                                                                      │
│  ┌──────────────────────┐                                          │
│  │ feature_names.pkl    │                                          │
│  │                      │                                          │
│  │ ['mean radius',      │                                          │
│  │  'mean texture',     │                                          │
│  │  'mean perimeter',   │                                          │
│  │  'mean compactness', │                                          │
│  │  'mean concavity']   │                                          │
│  └──────────────────────┘                                          │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  User    │──1──▶│  Flask   │──2──▶│  Scaler  │──3──▶│  Model   │
│  Input   │      │  App     │      │          │      │          │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
     ▲                                                       │
     │                                                       │
     │                                                      4│
     │                                                       │
     │                ┌──────────┐                          │
     └────────────5───│ Response │◀─────────────────────────┘
                      │  JSON    │
                      └──────────┘

Legend:
1. User submits form with 5 feature values
2. Flask validates and passes to scaler
3. Scaler normalizes features
4. Model makes prediction and calculates probabilities
5. Response sent back to user with results
```

## Machine Learning Pipeline

```
┌───────────────────────────────────────────────────────────────────┐
│                    MODEL DEVELOPMENT PIPELINE                      │
│                    (model_building.ipynb)                          │
└───────────────────────────────────────────────────────────────────┘

┌──────────────┐
│ Load Dataset │  ← Breast Cancer Wisconsin (Diagnostic)
│ 569 samples  │     • 30 features available
│ 2 classes    │     • No missing values
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Feature Select│  ← Select 5 features:
│              │     1. mean radius
│              │     2. mean texture
│              │     3. mean perimeter
│              │     4. mean compactness
│              │     5. mean concavity
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Train/Test    │  ← 80% train, 20% test
│Split         │     Stratified sampling
│              │     Random state: 42
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Scale Features│  ← StandardScaler
│              │     mean = 0, std = 1
│              │     Fit on training data
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Train Model   │  ← Logistic Regression
│              │     • max_iter: 1000
│              │     • solver: lbfgs
│              │     • class_weight: balanced
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Evaluate      │  ← Metrics:
│              │     • Accuracy: ~96%
│              │     • Precision: ~97%
│              │     • Recall: ~96%
│              │     • F1-Score: ~96%
│              │     • ROC AUC: ~0.99
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Save Model    │  ← Joblib serialization
│              │     • model.pkl
│              │     • scaler.pkl
│              │     • feature_names.pkl
└──────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY LAYERS                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER                                          │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│ │   HTML5     │ │    CSS3     │ │ JavaScript  │          │
│ │ Semantic    │ │ Modern      │ │ ES6+        │          │
│ │ Markup      │ │ Styling     │ │ Fetch API   │          │
│ └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ APPLICATION LAYER                                           │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│ │   Flask     │ │   Gunicorn  │ │   Python    │          │
│ │   3.0+      │ │   WSGI      │ │   3.8+      │          │
│ │   Routes    │ │   Server    │ │   Core      │          │
│ └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ MACHINE LEARNING LAYER                                      │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│ │ scikit-learn│ │   NumPy     │ │   Pandas    │          │
│ │ Logistic    │ │ Arrays &    │ │ DataFrames  │          │
│ │ Regression  │ │ Math        │ │ Analysis    │          │
│ └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ PERSISTENCE LAYER                                           │
│ ┌─────────────┐ ┌─────────────┐                           │
│ │   Joblib    │ │   Model     │                           │
│ │ Serializer  │ │   Storage   │                           │
│ │             │ │   .pkl      │                           │
│ └─────────────┘ └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                        │
└─────────────────────────────────────────────────────────────┘

Option 1: Render.com
┌──────────────────────────────────┐
│  GitHub Repository               │
│  ↓                               │
│  Render.com Build               │
│  ├─ pip install requirements    │
│  └─ gunicorn app:app            │
│  ↓                               │
│  Live Application               │
│  https://yourapp.onrender.com   │
└──────────────────────────────────┘

Option 2: PythonAnywhere
┌──────────────────────────────────┐
│  Upload Files                    │
│  ↓                               │
│  Create Virtual Environment      │
│  ├─ Install dependencies        │
│  └─ Configure WSGI              │
│  ↓                               │
│  Live Application               │
│  https://user.pythonanywhere.com│
└──────────────────────────────────┘

Option 3: Streamlit Cloud
┌──────────────────────────────────┐
│  GitHub Repository               │
│  ↓                               │
│  Streamlit Cloud Deploy         │
│  └─ Auto-detect requirements    │
│  ↓                               │
│  Live Application               │
│  https://yourapp.streamlit.app  │
└──────────────────────────────────┘

Option 4: Vercel
┌──────────────────────────────────┐
│  GitHub Repository               │
│  ↓                               │
│  Vercel Serverless Deploy       │
│  └─ Python runtime              │
│  ↓                               │
│  Live Application               │
│  https://yourapp.vercel.app     │
└──────────────────────────────────┘
```

## Security & Error Handling

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐
│ Input Validation Layer           │
│ • Type checking                  │
│ • Range validation               │
│ • Required field checks          │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Sanitization Layer               │
│ • Remove malicious input         │
│ • Float conversion               │
│ • Error messages                 │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Application Layer                │
│ • Try-catch blocks               │
│ • Logging                        │
│ • Custom exceptions              │
└────────────┬─────────────────────┘
             │
             ▼
┌──────────────────────────────────┐
│ Response Layer                   │
│ • Standard JSON responses        │
│ • HTTP status codes              │
│ • User-friendly messages         │
└──────────────────────────────────┘
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────┐
│                  PERFORMANCE OPTIMIZATIONS                   │
└─────────────────────────────────────────────────────────────┘

1. Model Loading
   • Loaded once at startup (not per request)
   • Cached in memory
   • Fast prediction time (<10ms)

2. Static Files
   • CSS minification possible
   • Browser caching enabled
   • CDN-ready

3. API Response
   • Lightweight JSON
   • Gzip compression
   • Fast serialization

4. Scalability
   • Stateless design
   • Horizontal scaling ready
   • Multiple workers supported
```

---

This architecture supports:
✓ High availability
✓ Fast response times
✓ Easy maintenance
✓ Simple deployment
✓ Production-ready
