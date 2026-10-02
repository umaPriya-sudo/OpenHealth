# =========================================================
# OpenHealth - Machine Learning Model Loader
# =========================================================

import pickle
import os
import json
import joblib
import tensorflow as tf


def load_models():

    models = {}
    scalers = {}

    print("\n📁 Loading Models...")
    print("=" * 40)

    # -----------------------------------------------------
    # Breast Cancer Model
    # -----------------------------------------------------
    try:
        with open(
            'artifacts/Breast_Cancer_Model/breast_cancer_model.pkl',
            'rb'
        ) as f:
            models['breast_cancer'] = pickle.load(f)

        with open(
            'artifacts/Breast_Cancer_Model/scaler.pkl',
            'rb'
        ) as f:
            scalers['breast_cancer'] = pickle.load(f)

        print("✅ Breast Cancer model loaded (93% accuracy)")

    except Exception as e:

        models['breast_cancer'] = None
        scalers['breast_cancer'] = None

        print("❌ Breast Cancer model could not be loaded")
        print("Breast Cancer Error:", e)

    # -----------------------------------------------------
    # Heart Disease Model
    # -----------------------------------------------------
    try:
        with open(
            'artifacts/Heart_Model/heart_model.pkl',
            'rb'
        ) as f:
            models['heart'] = pickle.load(f)

        with open(
            'artifacts/Heart_Model/scaler.pkl',
            'rb'
        ) as f:
            scalers['heart'] = pickle.load(f)

        print("✅ Heart Disease model loaded (85% accuracy)")

    except:

        models['heart'] = None
        scalers['heart'] = None

        print("❌ Heart Disease model not found")

    # -----------------------------------------------------
    # Diabetes Model
    # -----------------------------------------------------
    try:
        with open(
            'artifacts/Diabetes_Model/diabetes_model.pkl',
            'rb'
        ) as f:
            models['diabetes'] = pickle.load(f)

        with open(
            'artifacts/Diabetes_Model/scaler.pkl',
            'rb'
        ) as f:
            scalers['diabetes'] = pickle.load(f)

        print("✅ Diabetes model loaded (72% accuracy)")

    except:

        models['diabetes'] = None
        scalers['diabetes'] = None

        print("❌ Diabetes model not found")

    # -----------------------------------------------------
    # Liver Disease Model
    # -----------------------------------------------------
   
    try:
        models['liver'] = joblib.load(
            'artifacts/Liver_Disease/Liver_Model.pkl'
        )
    
        scalers['liver'] = joblib.load(
            'artifacts/Liver_Disease/scaler.pkl'
        )
    
        print("✅ Liver Disease model loaded successfully")
    
    except Exception as e:
    
        models['liver'] = None
        scalers['liver'] = None
    
        print("❌ Liver Disease model not found")
        print("Error:", e)

    return models, scalers


models, scalers = load_models()

# =========================================================
# PARKINSON'S DISEASE MODEL
# =========================================================

PARKINSON_MODEL_PATH = os.path.join(
    'artifacts',
    'Parkinsons_Model',
    'parkinsons_model.pkl'
)

PARKINSON_FEATURES_PATH = os.path.join(
    'artifacts',
    'Parkinsons_Model',
    'feature_names.json'
)

PARKINSON_METADATA_PATH = os.path.join(
    'artifacts',
    'Parkinsons_Model',
    'model_metadata.json'
)

parkinsons_model = None
parkinsons_features = []
parkinsons_threshold = 0.50
parkinsons_model_name = "Unknown"

try:

    parkinsons_model = joblib.load(
        PARKINSON_MODEL_PATH
    )

    with open(
        PARKINSON_FEATURES_PATH,
        'r',
        encoding='utf-8'
    ) as f:
        parkinsons_features = json.load(f)

    with open(
        PARKINSON_METADATA_PATH,
        'r',
        encoding='utf-8'
    ) as f:
        parkinsons_metadata = json.load(f)

    parkinsons_threshold = float(
        parkinsons_metadata.get(
            'deployment_threshold',
            0.50
        )
    )

    parkinsons_model_name = parkinsons_metadata.get(
        'selected_model',
        'Unknown'
    )

    print("✅ Parkinson's model loaded successfully")
    print(
        f"   Model: {parkinsons_model_name}"
    )
    print(
        f"   Features: {len(parkinsons_features)}"
    )
    print(
        f"   Threshold: {parkinsons_threshold:.3f}"
    )

except Exception as e:

    parkinsons_model = None
    parkinsons_features = []

    print("❌ Parkinson's model could not be loaded")
    print("Error:", e)


# =========================================================
# LIVER DISEASE THRESHOLD
# =========================================================

LIVER_THRESHOLD_PATH = os.path.join(
    'artifacts',
    'Liver_Disease',
    'threshold.pkl'
)

liver_threshold = 0.59

try:

    with open(
        LIVER_THRESHOLD_PATH,
        'rb'
    ) as f:
        liver_threshold = pickle.load(f)

    print(
        f"✅ Liver Disease threshold loaded: "
        f"{liver_threshold}"
    )

except Exception as e:

    print(
        "⚠️ Liver threshold could not be loaded."
    )

    print(
        "Using default threshold:",
        liver_threshold
    )


# =========================================================
# BRAIN TUMOR MODEL
# =========================================================

BRAIN_MODEL_PATH = os.path.join(
    'artifacts',
    'Brain_Tumour',
    'BrainModel.keras'
)

BRAIN_CLASS_NAMES_PATH = os.path.join(
    'artifacts',
    'Brain_Tumour',
    'class_names.json'
)

brain_model = None
brain_class_names = []

try:

    brain_model = tf.keras.models.load_model(
        BRAIN_MODEL_PATH
    )

    with open(
        BRAIN_CLASS_NAMES_PATH,
        'r'
    ) as f:
        brain_class_names = json.load(f)

    print(
        "✅ Brain Tumor model loaded successfully"
    )

    print(
        "🧠 Brain Tumor classes:",
        brain_class_names
    )

except Exception as e:

    print(
        "❌ Brain Tumor model could not be loaded"
    )

    print(
        "Error:",
        e
    )


# =========================================================
# KIDNEY DISEASE MODEL
# =========================================================

KIDNEY_MODEL_PATH = os.path.join(
    'artifacts',
    'Kidney',
    'KidneyModel.keras'
)

KIDNEY_CLASS_NAMES_PATH = os.path.join(
    'artifacts',
    'Kidney',
    'class_names.json'
)

kidney_model = None
kidney_class_names = []

try:

    kidney_model = tf.keras.models.load_model(
        KIDNEY_MODEL_PATH
    )

    with open(
        KIDNEY_CLASS_NAMES_PATH,
        'r'
    ) as f:
        kidney_class_names = json.load(f)

    print(
        "✅ Kidney Disease model loaded successfully"
    )

    print(
        "🩺 Kidney Disease classes:",
        kidney_class_names
    )

except Exception as e:

    print(
        "❌ Kidney Disease model could not be loaded"
    )

    print(
        "Error:",
        e
    )


# =========================================================
# MALARIA DETECTION MODEL
# =========================================================

MALARIA_MODEL_PATH = os.path.join(
    'artifacts',
    'Malaria_Model',
    'malaria_model.keras'
)

malaria_model = None

try:

    malaria_model = tf.keras.models.load_model(
        MALARIA_MODEL_PATH
    )

    print(
        "✅ Malaria model loaded successfully"
    )

    print(
        "🦠 Malaria model: CNN"
    )

    print(
        "🦠 Malaria input size: 128x128 RGB"
    )

except Exception as e:

    malaria_model = None

    print(
        "❌ Malaria model could not be loaded"
    )

    print(
        "Error:",
        e
    )