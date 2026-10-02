# =========================================================
# OpenHealth - ML Prediction Functions
# =========================================================

import numpy as np
import tensorflow as tf

from app.ml.model_loader import (
    brain_model,
    brain_class_names,
    kidney_model,
    kidney_class_names,
    malaria_model,
    models,
    scalers,
    liver_threshold,
    parkinsons_model,
    parkinsons_features,
    parkinsons_threshold
)


# =========================================================
# BRAIN TUMOR PREDICTION
# =========================================================

def predict_brain_tumor(image_path):

    if brain_model is None:
        raise RuntimeError(
            "Brain Tumor model is not loaded."
        )

    # Load MRI image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224),
        color_mode='rgb'
    )

    # Convert image to array
    image_array = tf.keras.utils.img_to_array(
        image
    )

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # IMPORTANT:
    # Do NOT divide by 255.
    # EfficientNetB0 handles preprocessing internally.

    predictions = brain_model.predict(
        image_array,
        verbose=0
    )[0]

    # Get highest probability class
    predicted_index = int(
        np.argmax(predictions)
    )

    predicted_class = brain_class_names[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    # Store probability of every class
    probabilities = {
        class_name: float(probability)
        for class_name, probability
        in zip(
            brain_class_names,
            predictions
        )
    }

    return (
        predicted_class,
        confidence,
        probabilities
    )

# =========================================================
# KIDNEY DISEASE PREDICTION
# =========================================================

def predict_kidney_disease(image_path):

    if kidney_model is None:
        raise RuntimeError(
            "Kidney Disease model is not loaded."
        )

    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224),
        color_mode='rgb'
    )

    image_array = tf.keras.utils.img_to_array(
        image
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # EfficientNetB0 handles preprocessing internally.
    # Do NOT divide by 255.

    predictions = kidney_model.predict(
        image_array,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    predicted_class = kidney_class_names[
        predicted_index
    ]

    confidence = float(
        predictions[predicted_index]
    )

    probabilities = {
        class_name: float(probability)
        for class_name, probability
        in zip(
            kidney_class_names,
            predictions
        )
    }

    return (
        predicted_class,
        confidence,
        probabilities
    )

# =========================================================
# MALARIA PREDICTION
# =========================================================

def predict_malaria(image_path):

    if malaria_model is None:
        raise RuntimeError(
            "Malaria model is not loaded."
        )

    # Load image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(128, 128),
        color_mode='rgb'
    )

    # Convert image to NumPy array
    image_array = tf.keras.utils.img_to_array(
        image
    )

    # IMPORTANT:
    # The CNN was trained with image / 255.0
    # Therefore prediction must use the same preprocessing.

    image_array = image_array / 255.0

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Model prediction
    prediction_probability = float(
        malaria_model.predict(
            image_array,
            verbose=0
        )[0][0]
    )

    # Class mapping:
    # 0 = Parasitized
    # 1 = Uninfected

    uninfected_probability = prediction_probability

    parasitized_probability = (
        1.0 - prediction_probability
    )

    # Determine predicted class

    if prediction_probability >= 0.5:

        predicted_class = "Uninfected"

        confidence = uninfected_probability

    else:

        predicted_class = "Parasitized"

        confidence = parasitized_probability

    # Store both probabilities

    probabilities = {
        "Parasitized": parasitized_probability,
        "Uninfected": uninfected_probability
    }

    return (
        predicted_class,
        confidence,
        probabilities
    )

# =========================================================
# LIVER DISEASE PREDICTION
# =========================================================

def predict_liver_disease(
    age,
    gender,
    tb,
    db,
    alkphos,
    sgpt,
    sgot,
    tp,
    alb,
    ag_ratio
):

    if models.get('liver') is None:
        raise RuntimeError(
            "Liver Disease model is not loaded."
        )

    # Feature order MUST match training order
    features = np.array([[
        float(age),
        float(gender),
        float(tb),
        float(db),
        float(alkphos),
        float(sgpt),
        float(sgot),
        float(tp),
        float(alb),
        float(ag_ratio)
    ]])

    # Apply the same scaler used during training
    features_scaled = scalers['liver'].transform(
        features
    )

    # Get probability of Liver Disease (class 1)
    probability = float(
        models['liver'].predict_proba(
            features_scaled
        )[0][1]
    )

    # Apply optimized threshold
    if probability >= liver_threshold:

        prediction = "Liver Disease Detected"
        predicted_class = 1

    else:

        prediction = "No Liver Disease Detected"
        predicted_class = 0

    # Confidence of selected prediction
    confidence = (
        probability
        if predicted_class == 1
        else 1 - probability
    )

    return (
        prediction,
        probability,
        confidence
    )

# =========================================================
# PARKINSON'S DISEASE PREDICTION
# =========================================================

def predict_parkinsons(features):

    if parkinsons_model is None:
        raise RuntimeError(
            "Parkinson's model is not loaded."
        )

    # Make sure exactly the expected number
    # of features are supplied
    if len(features) != len(parkinsons_features):
        raise ValueError(
            f"Expected {len(parkinsons_features)} features, "
            f"but received {len(features)}."
        )

    # Convert to NumPy array
    feature_array = np.array(
        [features],
        dtype=float
    )

    # Check invalid values
    if not np.isfinite(feature_array).all():
        raise ValueError(
            "All Parkinson's feature values must be valid numbers."
        )

    # parkinsons_model is already the complete
    # trained pipeline.
    probability = float(
        parkinsons_model.predict_proba(
            feature_array
        )[0][1]
    )

    # Apply training threshold
    if probability >= parkinsons_threshold:

        prediction = (
            "Possible Parkinson's Pattern Detected"
        )

    else:

        prediction = (
            "No Parkinson's Pattern Detected"
        )

    # Confidence of selected class
    confidence = (
        probability
        if probability >= parkinsons_threshold
        else 1.0 - probability
    )

    return (
        prediction,
        probability,
        confidence
    )

# =========================================================
# BREAST CANCER PREDICTION
# =========================================================

def predict_breast_cancer(
    radius_mean,
    texture_mean,
    perimeter_mean,
    area_mean,
    smoothness_mean,
    compactness_mean
):

    if models.get('breast_cancer') is None:
        raise RuntimeError(
            "Breast Cancer model is not loaded."
        )

    # 6 most important features
    features = np.array([[
        float(radius_mean),
        float(texture_mean),
        float(perimeter_mean),
        float(area_mean),
        float(smoothness_mean),
        float(compactness_mean)
    ]])

    # Scale features
    features_scaled = scalers[
        'breast_cancer'
    ].transform(features)

    # Get prediction probability
    pred_proba = models[
        'breast_cancer'
    ].predict_proba(features_scaled)

    result = round(
        float(pred_proba[0][1]),
        2
    )

    # Risk level
    if result >= 0.7:

        risk_level = "High Risk ⚠️"

    elif result >= 0.4:

        risk_level = "Medium Risk ⚡"

    else:

        risk_level = "Low Risk ✅"

    return (
        result,
        risk_level
    )

# =========================================================
# HEART DISEASE PREDICTION
# =========================================================

def predict_heart_disease(
    age,
    sex,
    cp,
    trestbps,
    chol,
    fbs,
    restecg,
    thalach,
    exang,
    oldpeak,
    slope,
    ca,
    thal
):

    if models.get('heart') is None:
        raise RuntimeError(
            "Heart Disease model is not loaded."
        )

    features = np.array([[
        float(age),
        float(sex),
        float(cp),
        float(trestbps),
        float(chol),
        float(fbs),
        float(restecg),
        float(thalach),
        float(exang),
        float(oldpeak),
        float(slope),
        float(ca),
        float(thal)
    ]])

    # Scale features
    features_scaled = scalers[
        'heart'
    ].transform(features)

    # Get prediction probability
    pred_proba = models[
        'heart'
    ].predict_proba(features_scaled)

    result = round(
        float(pred_proba[0][1]),
        2
    )

    # Risk level
    if result >= 0.7:

        risk_level = "High Risk ⚠️"

    elif result >= 0.4:

        risk_level = "Medium Risk ⚡"

    else:

        risk_level = "Low Risk ✅"

    return (
        result,
        risk_level
    )

# =========================================================
# DIABETES PREDICTION
# =========================================================

def predict_diabetes(
    pregnancies,
    glucose,
    blood_pressure,
    skin_thickness,
    insulin,
    bmi,
    diabetes_pedigree,
    age
):

    if models.get('diabetes') is None:
        raise RuntimeError(
            "Diabetes model is not loaded."
        )

    features = np.array([[
        float(pregnancies),
        float(glucose),
        float(blood_pressure),
        float(skin_thickness),
        float(insulin),
        float(bmi),
        float(diabetes_pedigree),
        float(age)
    ]])

    # Scale features
    features_scaled = scalers[
        'diabetes'
    ].transform(features)

    # Get prediction probability
    pred_proba = models[
        'diabetes'
    ].predict_proba(features_scaled)

    result = round(
        float(pred_proba[0][1]),
        2
    )

    # Risk level
    if result >= 0.7:

        risk_level = "High Risk ⚠️"

    elif result >= 0.4:

        risk_level = "Medium Risk ⚡"

    else:

        risk_level = "Low Risk ✅"

    return (
        result,
        risk_level
    )