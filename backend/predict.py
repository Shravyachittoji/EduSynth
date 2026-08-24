# ==========================================
# EduSynth - Prediction Engine
# ==========================================

import joblib
import numpy as np

# Load trained model
model = joblib.load("models/knowledge_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


def predict_knowledge(quiz_score, time_taken, attempts, previous_accuracy):
    """
    Predict student knowledge level
    """

    # Create feature array
    features = np.array([[quiz_score, time_taken, attempts, previous_accuracy]])

    # Predict
    prediction = model.predict(features)

    # Convert numeric label back to text
    knowledge_level = label_encoder.inverse_transform(prediction)[0]

    return knowledge_level
