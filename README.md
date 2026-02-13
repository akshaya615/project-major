A Real-Time Accident Severity Prediction and Hotspot Detection Framework Using HDBSCAN with Context-Aware Voice Alerts
A real-time machine learning–based road safety system for predicting accident severity and identifying accident-prone locations with proactive voice alerts.
________________________________________
Table of Contents
•	About
•	Features
•	Technologies Used
•	System Overview
•	Installation
•	Usage
•	Screenshots
•	Project Structure
•	Contributing
•	License
________________________________________
About
This project implements a real-time intelligent road safety framework that predicts accident severity and detects high-risk road segments using machine learning and spatial clustering techniques. It combines supervised severity classification with HDBSCAN-based hotspot detection to provide route-aware risk assessment.
The system integrates a FastAPI backend, a React (Vite) frontend, and context-aware voice alerts to deliver proactive safety warnings. Unlike traditional post-incident analysis systems, this framework focuses on real-time inference and preventive decision support for intelligent transportation applications.
________________________________________
Features
•	Real-time accident severity prediction (Low, Medium, High)
•	Hotspot detection using HDBSCAN clustering
•	Route-aware risk visualization
•	Interactive map-based interface
•	Context-aware voice alerts
•	User and administrator dashboards
•	RESTful API-based backend
________________________________________
Technologies Used
Backend
•	Python 3.9+
•	FastAPI
•	Uvicorn
•	Pydantic
Machine Learning
•	XGBoost
•	Scikit-learn
•	HDBSCAN
•	Pandas
•	NumPy
Frontend
•	React (Vite)
•	JavaScript (ES6+)
•	Leaflet.js
•	Fetch API
•	Web Speech API
•	CSS
________________________________________
System Overview
The system follows a modular architecture consisting of a frontend presentation layer, a backend processing layer, and a machine learning analytics layer. User route inputs are processed by the backend, where severity prediction and hotspot clustering are performed. The processed results are returned to the frontend for visualization and alert generation.
________________________________________
Installation
Step 1: Clone the Repository
git clone <repository-url>
cd project-major
________________________________________
Step 2: Backend Setup
cd api
pip install -r requirements.txt
________________________________________
Step 3: Frontend Setup
cd frontend
npm install
________________________________________
Running the Project (Single Command)
This project uses concurrently to run both backend and frontend together.
npm init -y
npm install concurrently --save-dev
Update the root package.json:
{
  "name": "project-major",
  "version": "1.0.0",
  "scripts": {
    "backend": "cd api && uvicorn main:app --reload",
    "frontend": "cd frontend && npm run dev",
    "dev": "concurrently \"npm run backend\" \"npm run frontend\""
  }
}
Run the application:
npm run dev
Backend runs at:
http://localhost:8000
Frontend runs at:
http://localhost:5173
________________________________________
Usage
1.	Open the frontend application in a browser.
2.	Select source and destination locations.
3.	Allow location access when prompted.
4.	View the route with severity indicators and hotspot markers.
5.	Receive voice alerts when approaching high-risk regions.
6.	Administrators can access dashboards for monitoring severity trends and hotspots.
________________________________________
Screenshots
Screenshots are recommended for projects with a visual interface.
Suggested images:
•	User dashboard with route and hotspots
•	Admin dashboard analytics
•	Voice alert interface
Suggested directory structure:
assets/
├── architecture.png
├── user_dashboard.png
├── admin_dashboard.png
└── alert.png
________________________________________
Project Structure
project-major/
│
├── api/   (Complete Backend – No Changes)
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── __init__.py
│   ├── .env
│   ├── .env.txt
│   ├── important.txt
│   ├── Day.docx
│   │
│   ├── routes/
│   │     predict.py
│   │     alerts.py
│   │     hotspots.py
│   │     auth.py
│   │
│   ├── core/
│   │     database.py
│   │     dependencies.py
│   │     security.py
│   │     secretkey.py
│   │
│   ├── jobs/
│   │     scheduler.py
│   │     hotspot_job.py
│   │
│   ├── schemas/
│   │     schemas.py
│   │
│   ├── services/
│   │     (existing files)
│   │
│   ├── utils/
│   │     distance.py
│   │
│   ├── ml/
│   │     gnn_model.py
│   │     gnnn_model.py
│   │     xgboost_model.py
│   │     hybrid_predictor.py
│   │     gnn_model.pt
│   │     gnn_severity_encoder.pt
│   │     xgb_model.pkl
│   │     severity_label_encoder.pkl
│   │
│   ├── preprocessing/
│   │     clean_dataset.py
│   │     feature_engineering.py
│   │     build_graph.py
│   │     add_coordinates.py
│   │     load_dataset.py
│   │     load_accident_data.py
│   │     reload_accident_data.py
│   │
│   ├── analytics/
│   │     hdbscan_hotspots.py
│   │     kde_heatmap.py
│   │     mongo_test.py
│   │     check_mongo_fields.py
│   │     check_nodes_columns.py
│   │
│   └── data/
│         accident.csv
│         cleaned_accident.csv
│         processed_accident.csv
│         processed_accident_with_coords.csv
│         nodes.csv
│         graph_edges.csv
│
├── frontend/   (No Changes – Only ONE new file added)
│   │
│   ├── node_modules/
│   ├── public/
│   │
│   ├── src/
│   │   │
│   │   ├── assets/
│   │   │
│   │   ├── components/
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
│   │   ├── pages/
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── Alerts.jsx
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── UserDashboard.jsx
│   │   │
│   │   ├── styles/
│   │   │   ├── userdashboard.css
│   │   │   ├── admindashboard.css
│   │   │   └── theme.css
│   │   │
│   │   ├── api/                ← ONLY NEW FOLDER ADDED
│   │   │   └── api.js          ← ONLY NEW FILE ADDED
│   │   │
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
│
├── package.json
└── README.md
________________________________________
Contributing
This project is developed primarily for academic and research purposes. Contributions may be made by forking the repository and submitting well-documented pull requests.
________________________________________
License
This project is intended for academic and educational use. All rights reserved by the author(s).

