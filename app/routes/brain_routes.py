import os
import uuid

from flask import Blueprint, render_template, request, session
from werkzeug.utils import secure_filename

from app.ml.predictions import predict_brain_tumor
from app.services.health_record_service import save_prediction_record


brain_bp = Blueprint(
    'brain',
    __name__
)


@brain_bp.route('/brain', methods=['GET', 'POST'])
def brain():

    if request.method == 'POST':

        if 'brain_image' not in request.files:
            return render_template(
                'diseases/brain.html',
                page='brain',
                show_result=True,
                error='Please select a brain MRI image.'
            )

        file = request.files['brain_image']

        if file.filename == '':
            return render_template(
                'diseases/brain.html',
                page='brain',
                show_result=True,
                error='Please select a brain MRI image.'
            )

        allowed_brain_extensions = {
            'jpg',
            'jpeg',
            'png'
        }

        extension = file.filename.rsplit('.', 1)[-1].lower()

        if extension not in allowed_brain_extensions:
            return render_template(
                'diseases/brain.html',
                page='brain',
                show_result=True,
                error='Invalid file type. Please upload JPG, JPEG, or PNG.'
            )

        brain_upload_folder = os.path.join(
            'uploads',
            'brain'
        )

        os.makedirs(
            brain_upload_folder,
            exist_ok=True
        )

        safe_name = secure_filename(file.filename)

        filename = (
            uuid.uuid4().hex
            + '_'
            + safe_name
        )

        filepath = os.path.join(
            brain_upload_folder,
            filename
        )

        file.save(filepath)

        try:

            predicted_class, confidence, probabilities = (
                predict_brain_tumor(filepath)
            )

            display_names = {
                'glioma': 'Glioma',
                'meningioma': 'Meningioma',
                'notumor': 'No Tumor Detected',
                'pituitary': 'Pituitary Tumor'
            }

            display_class = display_names.get(
                predicted_class,
                predicted_class.title()
            )

            if "user_id" in session:
                save_prediction_record(
                    user_id=session["user_id"],
                    disease_name="Brain Tumor",
                    prediction_type="Disease Prediction",
                    input_data={
                        "uploaded_image": filename,
                        "predicted_class": predicted_class
                    },
                    prediction_result=display_class,
                    result_details={
                        "confidence": round(confidence * 100, 2),
                        "prediction": display_class,
                        "class_probabilities": probabilities
                    }
                )

            return render_template(
                'diseases/brain.html',
                page='brain',
                show_result=True,
                prediction=display_class,
                predicted_class=predicted_class,
                confidence=confidence * 100,
                probabilities=probabilities,
                uploaded_image='brain/' + filename
            )

        except Exception as e:

            print("❌ Brain Tumor prediction error:", e)

            return render_template(
                'diseases/brain.html',
                page='brain',
                show_result=True,
                error=(
                    'Unable to analyze the MRI image. '
                    'Please try another JPG, JPEG, or PNG image.'
                )
            )

    return render_template(
        'diseases/brain.html',
        page='brain',
        show_result=False
    )