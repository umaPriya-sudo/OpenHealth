from flask import Blueprint, jsonify, request, session

from app.services.symptom_service import (
    get_symptoms,
    predict_disease
)

from app.services.medicine_recommendation_service import (
    get_associated_medicines
)

from app.services.health_record_service import save_prediction_record

symptom_bp = Blueprint(
    "symptom",
    __name__,
    url_prefix="/api/symptoms"
)


# =========================================================
# GET AVAILABLE SYMPTOMS
# =========================================================

@symptom_bp.route("", methods=["GET"])
def symptoms():

    try:
        available_symptoms = get_symptoms()

        return jsonify({
            "success": True,
            "symptoms": available_symptoms
        }), 200

    except Exception as e:

        print(f"Symptom list error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to load symptoms."
        }), 500


# =========================================================
# PREDICT DISEASE
# =========================================================

@symptom_bp.route("/predict", methods=["POST"])
def predict():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please sign in to use Symptom Checker.",
            "requires_login": True
        }), 401


    # -----------------------------------------------------
    # Read request
    # -----------------------------------------------------

    data = request.get_json(silent=True)

    if not data:

        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400


    selected_symptoms = data.get("symptoms")


    # -----------------------------------------------------
    # Validate symptoms
    # -----------------------------------------------------

    if not isinstance(selected_symptoms, list):

        return jsonify({
            "success": False,
            "message": "Symptoms must be provided as a list."
        }), 400


    if len(selected_symptoms) == 0:

        return jsonify({
            "success": False,
            "message": "Please select at least one symptom."
        }), 400


    # -----------------------------------------------------
    # Validate against available symptoms
    # -----------------------------------------------------

    available_symptoms = set(get_symptoms())

    invalid_symptoms = [
        symptom
        for symptom in selected_symptoms
        if symptom not in available_symptoms
    ]

    if invalid_symptoms:

        return jsonify({
            "success": False,
            "message": "One or more selected symptoms are invalid.",
            "invalid_symptoms": invalid_symptoms
        }), 400


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    try:

        result = predict_disease(
            selected_symptoms
        )

        associated_medicines = get_associated_medicines(
        result.get("disease")
)

        result["associated_medicines"] = associated_medicines

        save_prediction_record(
            user_id=session["user_id"],
            disease_name=result.get("disease", "Unknown"),
            prediction_type="Symptom Checker Prediction",
            input_data={
                "selected_symptoms": selected_symptoms
            },
            prediction_result=result.get("disease"),
            result_details={
                key: value
                for key, value in result.items()
                if key != "associated_medicines"
            }
        )

        return jsonify({
            "success": True,
            "result": result
        }), 200

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:

        print(f"Symptom prediction error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to make the prediction."
        }), 500