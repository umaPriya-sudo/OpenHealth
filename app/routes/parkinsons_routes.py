import numpy as np

from flask import Blueprint, render_template, request, session

from app.ml.model_loader import (
    parkinsons_model,
    parkinsons_features,
    parkinsons_threshold,
    parkinsons_model_name
)

from app.ml.predictions import predict_parkinsons
from app.services.health_record_service import save_prediction_record

parkinsons_bp = Blueprint(
    'parkinsons',
    __name__
)


@parkinsons_bp.route('/parkinsons', methods=["GET", "POST"])
def parkinsons():

    if request.method == "POST":

        try:

            if parkinsons_model is None:
                return render_template(
                    "diseases/parkinsons.html",
                    page="parkinsons",
                    show_result=False,
                    error=(
                        "Parkinson's model is not available. "
                        "Please check the model files."
                    )
                )

            features = []

            for feature_name in parkinsons_features:

                value = request.form.get(feature_name)

                if value is None or value.strip() == "":
                    raise ValueError(
                        f"Missing value for: {feature_name}"
                    )

                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(
                        f"{feature_name} must be a number."
                    )

                if not np.isfinite(value):
                    raise ValueError(
                        f"{feature_name} contains an invalid value."
                    )

                features.append(value)

            prediction, probability, confidence = (
                predict_parkinsons(features)
            )

            probability_percent = round(
                probability * 100,
                2
            )

            confidence_percent = round(
                confidence * 100,
                2
            )

            if probability >= parkinsons_threshold:
                risk_level = "Higher Risk ⚠️"

            elif probability >= 0.50:
                risk_level = "Intermediate Risk ⚡"

            else:
                risk_level = "Lower Risk ✅"

            if "user_id" in session:
                save_prediction_record(
                    user_id=session["user_id"],
                    disease_name="Parkinson's Disease",
                    prediction_type="Disease Prediction",
                    input_data={
                        feature_name: features[index]
                        for index, feature_name in enumerate(parkinsons_features)
                    },
                    prediction_result=probability_percent,
                    result_details={
                        "prediction": prediction,
                        "risk_level": risk_level,
                        "confidence": confidence_percent,
                        "threshold": round(parkinsons_threshold * 100, 2),
                        "model": parkinsons_model_name
                    }
                )

            return render_template(
                "diseases/parkinsons.html",
                page="parkinsons",
                show_result=True,
                prediction=prediction,
                probability=probability_percent,
                confidence=confidence_percent,
                risk_level=risk_level,
                threshold=round(
                    parkinsons_threshold * 100,
                    2
                ),
                model_name=parkinsons_model_name
            )

        except ValueError as e:

            return render_template(
                "diseases/parkinsons.html",
                page="parkinsons",
                show_result=True,
                error=f"Invalid input: {str(e)}"
            )

        except Exception as e:

            print(
                "❌ Parkinson's prediction error:",
                e
            )

            return render_template(
                "diseases/parkinsons.html",
                page="parkinsons",
                show_result=True,
                error=(
                    "Unable to process the Parkinson's "
                    "prediction. Please check your inputs."
                )
            )

    return render_template(
        "diseases/parkinsons.html",
        page="parkinsons",
        show_result=False
    )