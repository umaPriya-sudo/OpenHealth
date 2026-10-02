import os
import uuid

from flask import Blueprint, render_template, request, session
from werkzeug.utils import secure_filename

from app.ml.predictions import predict_malaria
from app.ml.model_loader import malaria_model
from app.services.health_record_service import save_prediction_record


malaria_bp = Blueprint(
    'malaria',
    __name__
)


@malaria_bp.route('/malaria', methods=['GET', 'POST'])
def malaria():

    if request.method == 'POST':

        if malaria_model is None:
            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                error=(
                    'Malaria model is not available. '
                    'Please check the model file.'
                )
            )

        if 'file' not in request.files:
            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                error='Please select a malaria blood-cell image.'
            )

        file = request.files['file']

        if file.filename == '':
            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                error='Please select a malaria blood-cell image.'
            )

        allowed_malaria_extensions = {
            'jpg',
            'jpeg',
            'png'
        }

        extension = file.filename.rsplit(
            '.',
            1
        )[-1].lower()

        if extension not in allowed_malaria_extensions:
            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                error=(
                    'Invalid file type. '
                    'Please upload JPG, JPEG, or PNG.'
                )
            )

        malaria_upload_folder = os.path.join(
            'uploads',
            'malaria'
        )

        os.makedirs(
            malaria_upload_folder,
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
            malaria_upload_folder,
            filename
        )

        file.save(filepath)

        try:

            (
                predicted_class,
                confidence,
                probabilities
            ) = predict_malaria(
                filepath
            )

            if predicted_class == "Parasitized":
                prediction = "Parasitized"
            else:
                prediction = "Uninfected"

            probability_percent = {
                class_name: round(
                    probability * 100,
                    2
                )
                for class_name, probability
                in probabilities.items()
            }

            confidence_percent = round(
                confidence * 100,
                2
            )

            if "user_id" in session:
                save_prediction_record(
                    user_id=session["user_id"],
                    disease_name="Malaria",
                    prediction_type="Disease Prediction",
                    input_data={
                        "uploaded_image": filename,
                        "predicted_class": predicted_class
                    },
                    prediction_result=prediction,
                    result_details={
                        "prediction": prediction,
                        "confidence": confidence_percent,
                        "class_probabilities": probability_percent
                    }
                )
            
            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                prediction=prediction,
                predicted_class=predicted_class,
                confidence=confidence_percent,
                probabilities=probability_percent,
                uploaded_image='malaria/' + filename
            )

        except Exception as e:

            print(
                "❌ Malaria prediction error:",
                e
            )

            return render_template(
                'diseases/malaria.html',
                page='malaria',
                show_result=True,
                error=(
                    'Unable to analyze the malaria image. '
                    'Please try another JPG, JPEG, or PNG image.'
                )
            )

    return render_template(
        'diseases/malaria.html',
        page='malaria',
        show_result=False
    )