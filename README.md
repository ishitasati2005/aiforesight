# 🌾 AgroPredict AI — Crop Recommendation System

> An end-to-end machine learning application that analyses soil and climate data to recommend the most suitable crop — powered by a trained ML model, a FastAPI backend, a Streamlit frontend, and a Gemini AI farming assistant.
## 📁 Project Structure


AgroPredict-AI/
│
├── app.py                  # Streamlit frontend (UI + Gemini chatbot)
├── style.css               # Earthy design system (all custom CSS)
├── main.py                 # FastAPI backend (prediction API)
├── model.pkl               # Trained ML model (saved via joblib)
├── crop_recommendation.csv # Raw dataset used for training
├── analysis.ipynb          # EDA + data cleaning + model training notebook
└── README.md               # Project documentation

## 📊 Dataset

**Source:** Crop Recommendation Dataset  
**File:** `crop_recommendation.csv`

The dataset contains **2,234 rows** and **8 columns** representing real-world agricultural conditions:

| Column       | Type    | Description                              |
|--------------|---------|------------------------------------------|
| `N`          | float   | Nitrogen content in soil (kg/ha)         |
| `P`          | float   | Phosphorus content in soil (kg/ha)       |
| `K`          | float   | Potassium content in soil (kg/ha)        |
| `temperature`| float   | Average temperature (°C)                 |
| `humidity`   | float   | Relative humidity (%)                    |
| `ph`         | float   | Soil pH value (0–14)                     |
| `rainfall`   | float   | Annual rainfall (mm)                     |
| `label`      | string  | Target crop (22 unique crop classes)     |

**22 Crop Classes:** rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee



## 🔍 Data Analysis & Cleaning

Performed in `analysis.ipynb` — steps carried out:

### 1. Exploratory Data Analysis (EDA)

- Loaded the CSV using `pandas` and inspected shape, dtypes, and `.describe()` statistics
- Checked class distribution across the 22 crop labels — found the dataset is **perfectly balanced** (100 samples per class)
- Plotted correlation heatmap between features to identify multicollinearity
- Visualised feature distributions using histograms and boxplots for each numeric column
- Identified the value ranges for each nutrient and environmental feature per crop

### 2. Data Cleaning

- **Missing values:** Checked with `df.isnull().sum()` — no null values found in any column
- **Duplicate rows:** Checked with `df.duplicated().sum()` — no duplicates present
- **Outlier detection:** Used IQR method on each numeric feature; mild outliers were retained as they represent natural agricultural variance
- **Label encoding:** The target column `label` (crop name) was encoded using `LabelEncoder` for model training
- **Feature scaling:** Applied `StandardScaler` to all 7 input features to normalise their ranges before model training

### 3. Feature Engineering

- All 7 original features were used as-is (no dimensionality reduction needed)
- Verified that features have sufficient variance and low intercorrelation
- Split data into **80% training / 20% testing** using `train_test_split` with `random_state=42`

---

## 🤖 Model Training

Multiple models were evaluated:

| Model                    | Accuracy  |
|--------------------------|-----------|
| Logistic Regression      | ~96%      |
| Decision Tree            | ~98%      |
| Random Forest            | ~99.26% ✅ |
| K-Nearest Neighbours     | ~97%      |
| Support Vector Machine   | ~97%      |

**Selected Model: Random Forest Classifier**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Encode labels
le = LabelEncoder()
y = le.fit_transform(df['label'])

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model + scaler + encoder
joblib.dump(model,  "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le,     "label_encoder.pkl")
```

**Evaluation:**
```
Accuracy  : ~99.26%
Precision : ~99%

---

## ⚡ FastAPI Backend

**File:** `main.py`

The trained model is served as a REST API using **FastAPI** + **Uvicorn**.

### Endpoint

```
POST /predict
```

**Request body (JSON):**
```json
{
  "n": 50,
  "p": 50,
  "k": 50,
  "temp": 25.0,
  "humidity": 60.0,
  "ph": 6.5,
  "rainfall": 120.0
}
```

**Response:**
```json
{
  "prediction": "rice"
}
```

### Running the API

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### `main.py` — Core Logic

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app    = FastAPI()
model  = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
le     = joblib.load("label_encoder.pkl")

class CropInput(BaseModel):
    n: float
    p: float
    k: float
    temp: float
    humidity: float
    ph: float
    rainfall: float

@app.post("/predict")
def predict(data: CropInput):
    features = np.array([[data.n, data.p, data.k,
                          data.temp, data.humidity,
                          data.ph, data.rainfall]])
    scaled    = scaler.transform(features)
    pred_idx  = model.predict(scaled)[0]
    crop_name = le.inverse_transform([pred_idx])[0]
    return {"prediction": crop_name}
```

---

## 🌿 Streamlit Frontend

**File:** `app.py` | **Styles:** `style.css`

The frontend is built with **Streamlit** and styled with a fully custom earthy CSS design system.

### Features

- **Hero section** with badge, animated title, and stat chips
- **Soil composition inputs** (N, P, K) with visual NPK blocks
- **Environmental sliders** for temperature, pH, humidity, rainfall
- **Live soil health meters** — real-time colour-coded progress bars (red → orange → green)
- **Prediction result card** — animated dark-green card with crop name and reasoning
- **Gemini AI Chatbot** — context-aware farming assistant that uses your predicted crop + soil data to give tailored advice

### Running the Frontend

```bash
streamlit run app.py
```

> ⚠️ Make sure the FastAPI server is running first on `http://127.0.0.1:8000`

---

## 🤝 Gemini AI Assistant

Integrated using the `google-generativeai` Python SDK.  
Model used: `gemini-3.1-flash-lite`

The assistant is crop-aware — once a crop is predicted, every question is sent to Gemini with full context:

```python
context = (
    f"The farmer's ML model recommended '{crop}' based on "
    f"N:{n}, P:{p}, K:{k}, pH:{ph}, Temp:{temp}°C, "
    f"Humidity:{humidity}%, Rainfall:{rainfall}mm."
)
prompt = f"{context} Question: {user_question}. Give practical farming advice."
response = gemini.generate_content(prompt)
```

Sample questions the assistant handles:
- *"What fertilizer should I use for rice?"*
- *"How often should I irrigate given high humidity?"*
- *"How do I prevent pests for this crop?"*
- *"When is the best time to sow?"*

---

## 🛠 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AgroPredict-AI.git
cd AgroPredict-AI
```

### 2. Install dependencies

```bash
pip install streamlit fastapi uvicorn scikit-learn pandas numpy joblib google-generativeai requests
```

### 3. Train the model (or use pre-trained files)

Open `analysis.ipynb` in Jupyter and run all cells. This generates:
- `model.pkl`
- `label_encoder.pkl`

### 4. Start the FastAPI server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Start the Streamlit app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🔑 Environment & API Keys

The Gemini API key is currently hardcoded in `app.py`. For production, move it to an environment variable:

```bash
export GEMINI_API_KEY="your-key-here"
```

```python
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

Get a free Gemini API key at: [https://aistudio.google.com](https://aistudio.google.com)

---

## 📦 Dependencies

| Package               | Purpose                            |
|-----------------------|------------------------------------|
| `streamlit`           | Frontend web UI                    |
| `fastapi`             | REST API backend                   |
| `uvicorn`             | ASGI server for FastAPI            |
| `scikit-learn`        | Model training & preprocessing     |
| `pandas`              | Data loading and manipulation      |
| `numpy`               | Numerical operations               |
| `joblib`              | Model serialisation                |
| `google-generativeai` | Gemini AI chatbot integration      |
| `requests`            | HTTP calls from Streamlit → FastAPI|

---

## 🌍 Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Streamlit Frontend              │
│  app.py + style.css                         │
│  - Soil inputs (N, P, K, temp, pH, etc.)    │
│  - Live health meters                        │
│  - Prediction result card                   │
│  - Gemini AI chatbot                        │
└───────────────────┬─────────────────────────┘
                    │ POST /predict (JSON)
                    ▼
┌─────────────────────────────────────────────┐
│           FastAPI Backend (main.py)          │
│  - Loads model.pkl, scaler.pkl, encoder.pkl │
│  - Scales input → predicts → decodes label  │
│  - Returns crop name as JSON                │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         Random Forest Classifier             │
│  Trained on crop_recommendation.csv         │
│  99.5% accuracy · 22 crop classes           │
└─────────────────────────────────────────────┘
                    +
┌─────────────────────────────────────────────┐
│          Google Gemini AI (Flash)            │
│  Context-aware farming advice chatbot        │
│  Uses predicted crop + soil data as context  │
└─────────────────────────────────────────────┘
```

---

## 📸 App Preview

| Section | Description |
|---|---|
| 🌾 Hero | Title, stat chips, project badges |
| 🪱 Soil Inputs | NPK blocks + number inputs |
| 🌦 Environment | Temperature, pH, humidity, rainfall sliders |
| 📊 Soil Meters | Live colour-coded health bars |
| ✅ Result Card | Animated crop recommendation with reasoning |
| 🌿 AI Assistant | Gemini-powered context-aware chatbot |

---

## 📄 License

This project is for educational and agricultural research purposes.

---

*Built with ❤️ for farmers, fields & the future of sustainable agriculture.*  
*Powered by Machine Learning · Grounded in Nature*