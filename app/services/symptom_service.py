import json
import os
import joblib
import pandas as pd


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "artifacts",
    "Symptom_Model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "symptom_model.pkl"
)

FEATURE_PATH = os.path.join(
    MODEL_DIR,
    "symptom_features.json"
)


# =========================================================
# LOAD MODEL
# =========================================================

_model = None
_features = None


def _load_model():

    global _model

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Symptom model not found: {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)

    return _model


# =========================================================
# LOAD SYMPTOM FEATURES
# =========================================================

def _load_features():

    global _features

    if _features is None:

        if not os.path.exists(FEATURE_PATH):
            raise FileNotFoundError(
                f"Symptom feature file not found: {FEATURE_PATH}"
            )

        with open(
            FEATURE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            _features = json.load(f)

    return _features


# =========================================================
# GET AVAILABLE SYMPTOMS
# =========================================================

def get_symptoms():

    return _load_features()


# =========================================================
# PREDICT DISEASE
# =========================================================

def predict_disease(selected_symptoms):

    if not selected_symptoms:
        raise ValueError(
            "Please select at least one symptom."
        )

    features = _load_features()
    model = _load_model()

    # Normalize selected symptom names
    selected = {
        str(symptom).strip().lower()
        for symptom in selected_symptoms
    }

    # Create a 132-feature input row
    input_data = {
        feature: 1 if feature.lower() in selected else 0
        for feature in features
    }

    input_df = pd.DataFrame(
        [input_data],
        columns=features
    )

    # Predict disease
    prediction = model.predict(input_df)

    disease = str(prediction[0])

    # Probability/confidence if supported
    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            input_df
        )[0]

        confidence = float(
            max(probabilities) * 100
        )

    return {
        "disease": disease,
        "confidence": confidence,
        "selected_symptoms": list(selected_symptoms)
    }