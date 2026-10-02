from flask import Blueprint, render_template, request, session
from app.ml.model_loader import models
from app.ml.predictions import predict_breast_cancer
from app.services.health_record_service import save_prediction_record


breast_cancer_bp = Blueprint(
    'breast_cancer',
    __name__
)


@breast_cancer_bp.route('/breast_cancer', methods=["GET", "POST"])
def breast_cancer():

    if request.method == 'POST':
        try:

            if models.get('breast_cancer') is not None:

                result, risk_level = predict_breast_cancer(
                    request.form.get('radius_mean', 0),
                    request.form.get('texture_mean', 0),
                    request.form.get('perimeter_mean', 0),
                    request.form.get('area_mean', 0),
                    request.form.get('smoothness_mean', 0),
                    request.form.get('compactness_mean', 0)
                )

                if "user_id" in session:
                    save_prediction_record(
                        user_id=session["user_id"],
                        disease_name="Breast Cancer",
                        prediction_type="Disease Prediction",
                        input_data={
                            "radius_mean": request.form.get("radius_mean", 0),
                            "texture_mean": request.form.get("texture_mean", 0),
                            "perimeter_mean": request.form.get("perimeter_mean", 0),
                            "area_mean": request.form.get("area_mean", 0),
                            "smoothness_mean": request.form.get("smoothness_mean", 0),
                            "compactness_mean": request.form.get("compactness_mean", 0)
                        },
                        prediction_result=result,
                        result_details={
                            "risk_level": risk_level
                        }
                    )

                return render_template(
                    'diseases/breast_cancer.html',
                    page='breast_cancer',
                    final_result=result,
                    risk_level=risk_level,
                    show_result=True
                )

            else:

                return render_template(
                    'diseases/breast_cancer.html',
                    page='breast_cancer',
                    error='Breast Cancer model not found. Please train the model first.',
                    show_result=False
                )

        except Exception as e:

            print(f"Error: {e}")

            return render_template(
                'diseases/breast_cancer.html',
                page='breast_cancer',
                error=f'Error: {str(e)}',
                show_result=False
            )

    return render_template(
        'diseases/breast_cancer.html',
        page='breast_cancer',
        show_result=False
    )