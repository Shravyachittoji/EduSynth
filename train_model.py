# ==========================================
# EduSynth - Improved Knowledge Model Training
# (CPU Friendly | No Breaking Changes)
# ==========================================

import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("Loading dataset...")

# Load dataset
data = pd.read_csv("data/student_data.csv")

print("Dataset Loaded Successfully!\n")

# Separate features and target
X = data.drop("knowledge_level", axis=1)
y = data["knowledge_level"]

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Stratified Split (better than normal split)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("Training Random Forest Model (CPU)...")

# Slightly tuned but safe parameters
model = RandomForestClassifier(
    n_estimators=150,        # Slightly increased
    max_depth=10,            # Prevent overfitting
    random_state=42,
    n_jobs=-1                # Use all CPU cores
)

# Train model
model.fit(X_train, y_train)

print("Model Training Completed!\n")

# -------------------------
# Cross Validation (Professional touch)
# -------------------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y_encoded, cv=cv, scoring="accuracy")

print("Cross Validation Accuracy:", round(np.mean(cv_scores) * 100, 2), "%\n")

# -------------------------
# Evaluate on test data
# -------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Test Accuracy:", round(accuracy * 100, 2), "%\n")

print("Classification Report:\n")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# -------------------------
# Feature Importance (Viva Friendly)
# -------------------------
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:\n")
print(importance)

# -------------------------
# Save model (No change in format)
# -------------------------
joblib.dump(model, "models/knowledge_model.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\nModel saved successfully in models/ folder!")
