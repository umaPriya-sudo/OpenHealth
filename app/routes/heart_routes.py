from flask import Blueprint, render_template, request, session

from app.ml.model_loader import models
from app.ml.predictions import predict_heart_disease
from app.services.health_record_service import save_prediction_record


heart_bp = Blueprint(
    'heart',
    __name__
)


@heart_bp.route('/heart', methods=["GET", "POST"])
def heart():

    if request.method == "POST":
        try:

            if models.get('heart') is not None:

                result, risk_level = predict_heart_disease(
                    request.form.get('age', 0),
                    request.form.get('sex', 0),
                    request.form.get('cp', 0),
                    request.form.get('trestbps', 0),
                    request.form.get('chol', 0),
                    request.form.get('fbs', 0),
                    request.form.get('restecg', 0),
                    request.form.get('thalach', 0),
                    request.form.get('exang', 0),
                    request.form.get('oldpeak', 0),
                    request.form.get('slope', 0),
                    request.form.get('ca', 0),
                    request.form.get('thal', 0)
                )

                if "user_id" in session:

                    save_prediction_record(
                        user_id=session["user_id"],
                        disease_name="Heart Disease",
                        prediction_type="Disease Prediction",
                        input_data={
                            "age": request.form.get("age", 0),
                            "sex": request.form.get("sex", 0),
                            "cp": request.form.get("cp", 0),
                            "trestbps": request.form.get("trestbps", 0),
                            "chol": request.form.get("chol", 0),
                            "fbs": request.form.get("fbs", 0),
                            "restecg": request.form.get("restecg", 0),
                            "thalach": request.form.get("thalach", 0),
                            "exang": request.form.get("exang", 0),
                            "oldpeak": request.form.get("oldpeak", 0),
                            "slope": request.form.get("slope", 0),
                            "ca": request.form.get("ca", 0),
                            "thal": request.form.get("thal", 0)
                        },
                        prediction_result=result,
                        result_details={
                            "risk_level": risk_level
                        }
                    )

                return render_template(
                    'diseases/heart.html',
                    page='heart',
                    final_result=result,
                    risk_level=risk_level,
                    show_result=True
                )

            else:

                return render_template(
                    'diseases/heart.html',
                    page='error'
                )

        except Exception as e:

            print(f"Error: {e}")

            return render_template(
                'diseases/heart.html',
                page='error'
            )

    return render_template(
        'diseases/heart.html',
        page='heart',
        show_result=False
    )