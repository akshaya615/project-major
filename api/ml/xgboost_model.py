import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "ml")

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(os.path.join(DATA_DIR, "processed_accident.csv"))

# -----------------------------
# Encode Severity Score
# -----------------------------
label_encoder = LabelEncoder()
df["Severity_Label"] = label_encoder.fit_transform(df["Severity_Score"])

print("Severity label mapping:")
for original, encoded in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)):
    print(f"Severity {original} -> Class {encoded}")

# -----------------------------
# Drop non-ML columns
# -----------------------------
df = df.drop(columns=["Accident_ID", "Severity_Score", "Date", "Time"])

# -----------------------------
# Features and Target
# -----------------------------
X = df.drop("Severity_Label", axis=1)
y = df["Severity_Label"]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# XGBoost Model
# -----------------------------
model = XGBClassifier(
    objective="multi:softmax",
    num_class=len(y.unique()),
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="mlogloss"
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nXGBoost Model Accuracy:", accuracy)

# -----------------------------
# Save model & encoder
# -----------------------------
joblib.dump(model, os.path.join(MODEL_DIR, "xgb_model.pkl"))
joblib.dump(label_encoder, os.path.join(MODEL_DIR, "severity_label_encoder.pkl"))

print("\nSaved:")
print(" - xgb_model.pkl")
print(" - severity_label_encoder.pkl")