from flask import Blueprint, render_template, request, session

from app.ml.model_loader import models
from app.ml.predictions import predict_diabetes

from app.services.health_record_service import (
    save_prediction_record
)


diabetes_bp = Blueprint(
    'diabetes',
    __name__
)


@diabetes_bp.route('/diabetes', methods=["GET", "POST"])
def diabetes():

    if request.method == "POST":
        try:

            if models.get('diabetes') is not None:

                result, risk_level = predict_diabetes(
                    request.form.get('pregnancies', 0),
                    request.form.get('Glucose', 0),
                    request.form.get('BloodPressure', 0),
                    request.form.get('skin_thickness', 0),
                    request.form.get('insulin', 0),
                    request.form.get('BMI', 0),
                    request.form.get('DiabetesPedigreeFunction', 0),
                    request.form.get('Age', 0)
                )

                # ---------------------------------------------------------
                # Save prediction to Health Records
                # ---------------------------------------------------------

                if "user_id" in session:
                
                    input_data = {
                        "pregnancies": request.form.get(
                            "pregnancies", 0
                        ),
                        "glucose": request.form.get(
                            "Glucose", 0
                        ),
                        "blood_pressure": request.form.get(
                            "BloodPressure", 0
                        ),
                        "skin_thickness": request.form.get(
                            "skin_thickness", 0
                        ),
                        "insulin": request.form.get(
                            "insulin", 0
                        ),
                        "bmi": request.form.get(
                            "BMI", 0
                        ),
                        "diabetes_pedigree_function": request.form.get(
                            "DiabetesPedigreeFunction", 0
                        ),
                        "age": request.form.get(
                            "Age", 0
                        )
                    }


                    save_prediction_record(
                        user_id=session["user_id"],
                        disease_name="Diabetes",
                        prediction_result=result,
                        prediction_type="Disease Prediction",
                        input_data=input_data,
                        result_details={
                            "risk_level": risk_level
                        }
                    )

                return render_template(
                    'diseases/diabetes.html',
                    page='diabetes',
                    final_result=result,
                    risk_level=risk_level,
                    show_result=True
                )

            else:

                return render_template(
                    'diseases/diabetes.html',
                    page='error'
                )

        except Exception as e:

            print(f"Error: {e}")

            return render_template(
                'diseases/diabetes.html',
                page='error'
            )

    return render_template(
        'diseases/diabetes.html',
        page='diabetes',
        show_result=False
    )