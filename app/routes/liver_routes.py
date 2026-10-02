from flask import Blueprint, render_template, request, session

from app.ml.model_loader import models, liver_threshold
from app.ml.predictions import predict_liver_disease
from app.services.health_record_service import save_prediction_record


liver_bp = Blueprint(
    'liver',
    __name__
)


@liver_bp.route('/liver', methods=['GET', 'POST'])
def liver():

    if request.method == 'POST':

        try:

            if models.get('liver') is None:
                return render_template(
                    'diseases/liver.html',
                    page='liver',
                    show_result=False,
                    error='Liver Disease model not found. Please train the model first.'
                )

            age = float(request.form.get('age', 0))
            gender = float(request.form.get('gender', 0))
            tb = float(request.form.get('tb', 0))
            db = float(request.form.get('db', 0))
            alkphos = float(request.form.get('alkphos', 0))
            sgpt = float(request.form.get('sgpt', 0))
            sgot = float(request.form.get('sgot', 0))
            tp = float(request.form.get('tp', 0))
            alb = float(request.form.get('alb', 0))
            ag_ratio = float(request.form.get('ag_ratio', 0))

            if age <= 0:
                raise ValueError("Age must be greater than 0.")

            if tb < 0 or db < 0:
                raise ValueError("Bilirubin values cannot be negative.")

            if alkphos < 0 or sgpt < 0 or sgot < 0:
                raise ValueError("Enzyme values cannot be negative.")

            if tp < 0 or alb < 0 or ag_ratio < 0:
                raise ValueError("Protein values cannot be negative.")

            prediction, probability, confidence = predict_liver_disease(
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
            )

            probability_percent = round(
                probability * 100,
                2
            )

            confidence_percent = round(
                confidence * 100,
                2
            )

            if prediction == "Liver Disease Detected":
                risk_level = "Higher Risk ⚠️"
            else:
                risk_level = "Lower Risk ✅"

            if "user_id" in session:

                save_prediction_record(
                    user_id=session["user_id"],
                    disease_name="Liver Disease",
                    prediction_type="Disease Prediction",
                    input_data={
                        "age": age,
                        "gender": gender,
                        "tb": tb,
                        "db": db,
                        "alkphos": alkphos,
                        "sgpt": sgpt,
                        "sgot": sgot,
                        "tp": tp,
                        "alb": alb,
                        "ag_ratio": ag_ratio
                    },
                    prediction_result=probability_percent,
                    result_details={
                        "prediction": prediction,
                        "risk_level": risk_level,
                        "confidence": confidence_percent,
                        "threshold": round(
                            liver_threshold * 100,
                            2
                        )
                    }
                )

            return render_template(
                'diseases/liver.html',
                page='liver',
                show_result=True,
                prediction=prediction,
                probability=probability_percent,
                confidence=confidence_percent,
                risk_level=risk_level,
                threshold=round(
                    liver_threshold * 100,
                    2
                )
            )

        except ValueError as e:

            return render_template(
                'diseases/liver.html',
                page='liver',
                show_result=True,
                error=f"Invalid input: {str(e)}"
            )

        except Exception as e:

            print(
                "❌ Liver Disease prediction error:",
                e
            )

            return render_template(
                'diseases/liver.html',
                page='liver',
                show_result=True,
                error=(
                    "Unable to process the liver disease prediction. "
                    "Please check your inputs and try again."
                )
            )

    return render_template(
        'diseases/liver.html',
        page='liver',
        show_result=False
    )