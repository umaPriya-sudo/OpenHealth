import os
import uuid

from flask import Blueprint, render_template, request, session
from werkzeug.utils import secure_filename

from app.ml.predictions import predict_kidney_disease
from app.services.health_record_service import save_prediction_record

kidney_bp = Blueprint(
    'kidney',
    __name__
)


@kidney_bp.route('/kidney', methods=['GET', 'POST'])
def kidney():

    if request.method == 'POST':

        if 'kidney_image' not in request.files:
            return render_template(
                'diseases/kidney.html',
                page='kidney',
                show_result=True,
                error='Please select a kidney CT image.'
            )

        file = request.files['kidney_image']

        if file.filename == '':
            return render_template(
                'diseases/kidney.html',
                page='kidney',
                show_result=True,
                error='Please select a kidney CT image.'
            )

        allowed_kidney_extensions = {
            'jpg',
            'jpeg',
            'png'
        }

        extension = file.filename.rsplit(
            '.',
            1
        )[-1].lower()

        if extension not in allowed_kidney_extensions:
            return render_template(
                'diseases/kidney.html',
                page='kidney',
                show_result=True,
                error=(
                    'Invalid file type. '
                    'Please upload JPG, JPEG, or PNG.'
                )
            )

        kidney_upload_folder = os.path.join(
            'uploads',
            'kidney'
        )

        os.makedirs(
            kidney_upload_folder,
            exist_ok=True
        )

        safe_name = secure_filename(
            file.filename
        )

        filename = (
            uuid.uuid4().hex
            + '_'
            + safe_name
        )

        filepath = os.path.join(
            kidney_upload_folder,
            filename
        )

        file.save(filepath)

        try:

            (
                predicted_class,
                confidence,
                probabilities
            ) = predict_kidney_disease(
                filepath
            )

            display_names = {
                'Cyst': 'Kidney Cyst',
                'Normal': 'Normal Kidney',
                'Stone': 'Kidney Stone',
                'Tumor': 'Kidney Tumor'
            }

            display_class = display_names.get(
                predicted_class,
                predicted_class
            )

            if "user_id" in session:
                save_prediction_record(
                    user_id=session["user_id"],
                    disease_name="Kidney Disease",
                    prediction_type="Disease Prediction",
                    input_data={
                        "uploaded_image": filename,
                        "predicted_class": predicted_class
                    },
                    prediction_result=display_class,
                    result_details={
                        "prediction": display_class,
                        "confidence": round(confidence * 100, 2),
                        "class_probabilities": probabilities
                    }
                )

            return render_template(
                'diseases/kidney.html',
                page='kidney',
                show_result=True,
                prediction=display_class,
                predicted_class=predicted_class,
                confidence=confidence * 100,
                probabilities=probabilities,
                uploaded_image='kidney/' + filename
            )

        except Exception as e:

            print(
                "❌ Kidney Disease prediction error:",
                e
            )

            return render_template(
                'diseases/kidney.html',
                page='kidney',
                show_result=True,
                error=(
                    'Unable to analyze the kidney image. '
                    'Please try another JPG, JPEG, or PNG image.'
                )
            )

    return render_template(
        'diseases/kidney.html',
        page='kidney',
        show_result=False
    )