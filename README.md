# 🚦 A Real-Time Accident Severity Prediction and Hotspot Detection Framework Using HDBSCAN with Context-Aware Voice Alerts

---

## 📌 Project Description

This project presents a complete **Real-Time Road Accident Severity Prediction and Hotspot Detection System** designed to enhance transportation safety using Machine Learning and Spatial Data Analysis.

The system predicts accident severity levels, detects accident-prone hotspots using **HDBSCAN clustering**, and provides real-time route-based risk visualization with intelligent voice alerts.

It is a full-stack implementation built with:

* **FastAPI** (Backend API)
* **React + Vite** (Frontend UI)
* **XGBoost & GNN Models** (Severity Prediction)
* **HDBSCAN** (Hotspot Detection)
* **Leaflet.js** (Map Visualization)

This framework is developed as an academic major project focusing on real-time predictive safety systems.

---

## 🎯 Objectives

The primary objectives of this project are:

1. Predict accident severity in real time.
2. Detect accident-prone locations using density-based clustering.
3. Provide route-level risk evaluation.
4. Trigger contextual voice alerts for high-risk areas.
5. Build a scalable ML-powered web application.

---

## 🏗️ Complete Project Structure

```
project-major/
│
├── 📂 api/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── __init__.py
│   ├── .env
│   ├── .env.txt
│   ├── important.txt
│   ├── Day.docx
│   │
│   ├── 📂 routes/
│   │     ├── predict.py
│   │     ├── alerts.py
│   │     ├── hotspots.py
│   │     └── auth.py
│   │
│   ├── 📂 core/
│   │     ├── database.py
│   │     ├── dependencies.py
│   │     ├── security.py
│   │     └── secretkey.py
│   │
│   ├── 📂 jobs/
│   │     ├── scheduler.py
│   │     └── hotspot_job.py
│   │
│   ├── 📂 schemas/
│   │     └── schemas.py
│   │
│   ├── 📂 services/
│   │     (existing service files)
│   │
│   ├── 📂 utils/
│   │     └── distance.py
│   │
│   ├── 📂 ml/
│   │     ├── gnn_model.py
│   │     ├── gnnn_model.py
│   │     ├── xgboost_model.py
│   │     ├── hybrid_predictor.py
│   │     ├── gnn_model.pt
│   │     ├── gnn_severity_encoder.pt
│   │     ├── xgb_model.pkl
│   │     └── severity_label_encoder.pkl
│   │
│   ├── 📂 preprocessing/
│   │     ├── clean_dataset.py
│   │     ├── feature_engineering.py
│   │     ├── build_graph.py
│   │     ├── add_coordinates.py
│   │     ├── load_dataset.py
│   │     ├── load_accident_data.py
│   │     └── reload_accident_data.py
│   │
│   ├── 📂 analytics/
│   │     ├── hdbscan_hotspots.py
│   │     ├── kde_heatmap.py
│   │     ├── mongo_test.py
│   │     ├── check_mongo_fields.py
│   │     └── check_nodes_columns.py
│   │
│   └── 📂 data/
│         ├── accident.csv
│         ├── cleaned_accident.csv
│         ├── processed_accident.csv
│         ├── processed_accident_with_coords.csv
│         ├── nodes.csv
│         └── graph_edges.csv
│
├── 📂 frontend/
│   │
│   ├── public/
│   ├── node_modules/
│   │
│   ├── 📂 src/
│   │   │
│   │   ├── 📂 components/
│   │   │   ├── AccidentTrend.jsx
│   │   │   ├── Alerts.jsx
│   │   │   ├── Feedback.jsx
│   │   │   ├── Hotspots.jsx
│   │   │   ├── LiveMap.jsx
│   │   │   ├── LocationDetails.jsx
│   │   │   ├── MapView.jsx
│   │   │   ├── RouteMap.jsx
│   │   │   ├── SeverityPie.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   └── VoiceAlert.jsx
│   │   │
│   │   ├── 📂 pages/
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── Alerts.jsx
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── UserDashboard.jsx
│   │   │
│   │   ├── 📂 styles/
│   │   │   ├── userdashboard.css
│   │   │   ├── admindashboard.css
│   │   │   └── theme.css
│   │   │
│   │   ├── 📂 api/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── index.html
│   ├── eslint.config.js
│   └── README.md
│
├── package.json
└── README.md
```

---

## 🧠 System Architecture

```
Frontend (React + Leaflet)
        ↓
FastAPI Backend (REST APIs)
        ↓
Machine Learning Layer
   • XGBoost Severity Predictor
   • GNN Model
   • Hybrid Predictor
   • HDBSCAN Hotspot Detection
        ↓
Processed Accident Dataset
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone <your-repository-url>
cd project-major
```

---

### 2️⃣ Backend Setup

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:
**[http://localhost:8000](http://localhost:8000)**

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:
**[http://localhost:5173](http://localhost:5173)**

---

## 🔐 Authentication Flow

1. User/Admin registers.
2. Data is stored securely in database.
3. On login, credentials are verified.
4. JWT token is generated.
5. Protected routes validate token.
6. Role-based dashboard is loaded.

---

## 📊 Core Functional Modules

### 1️⃣ Severity Prediction

* Uses trained XGBoost & GNN models
* Classifies accidents into Low, Medium, High
* Returns probability scores

### 2️⃣ Hotspot Detection

* HDBSCAN clustering
* Detects dense accident regions
* Automatically ignores noise

### 3️⃣ Route Risk Analysis

* Evaluates user-selected route
* Calculates severity-weighted risk score

### 4️⃣ Voice Alert System

* Uses Web Speech API
* Alerts when entering high-risk zones

---

## 🚀 API Endpoints

| Endpoint         | Method | Description               |
| ---------------- | ------ | ------------------------- |
| `/predict`       | POST   | Predict accident severity |
| `/hotspots`      | GET    | Get clustered hotspots    |
| `/alerts`        | GET    | Retrieve risk alerts      |
| `/auth/login`    | POST   | Login                     |
| `/auth/register` | POST   | Register                  |
| `/docs`          | GET    | Swagger Documentation     |

---

## 📚 Technologies Used

### 🔹 Backend

* FastAPI
* Uvicorn
* Pydantic
* Python

### 🔹 Machine Learning

* XGBoost
* PyTorch
* HDBSCAN
* Scikit-learn
* Pandas
* NumPy

### 🔹 Frontend

* React
* Vite
* Leaflet.js
* JavaScript (ES6+)
* CSS3

---

## 📈 Future Enhancements

* Real-time traffic data integration
* Mobile application version
* Cloud deployment (AWS/Azure)
* Advanced deep learning ensemble models
* Integration with smart city systems

---

## 🎓 Conclusion

This project demonstrates a complete real-time accident prediction and hotspot detection framework combining supervised learning, unsupervised clustering, geospatial analysis, and full-stack web deployment.

It provides a scalable and intelligent safety monitoring system that can assist in proactive accident prevention and smart transportation planning.

---

## 📄 License

This project is developed for academic and educational purposes.

**All Rights Reserved © 2026*

If you want, I can now make it look even more “final-year topper level” professional 😄

