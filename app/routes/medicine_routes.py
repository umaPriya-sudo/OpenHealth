import json
import os

from flask import (
    Blueprint,
    current_app,
    render_template,
    request
)
from werkzeug.utils import secure_filename

from app.services.medicine_service import (
    extract_text_from_image,
    get_medicine_info,
    recognize_medicine_from_text
)

from app.utils.file_utils import allowed_file


medicine_bp = Blueprint(
    'medicine',
    __name__
)


@medicine_bp.route(
    '/recognition',
    methods=['GET', 'POST']
)
def recognition():

    if request.method == 'POST':

        manual_medicine = request.form.get(
            'manual_medicine',
            ''
        ).strip()

        # ====================================================
        # MANUAL MEDICINE SEARCH
        # ====================================================

        if manual_medicine:

            medicine_result = recognize_medicine_from_text(
                manual_medicine
            )

            medicine_info = get_medicine_info(
                manual_medicine
            )

            return render_template(
                'medicine/recognition.html',
                medicine_info=medicine_info,
                medicine_result=medicine_result,
                extracted_text=manual_medicine,
                show_result=True,
                manual_entry=manual_medicine
            )

        # ====================================================
        # IMAGE UPLOAD VALIDATION
        # ====================================================

        if 'file' not in request.files:

            return render_template(
                'medicine/recognition.html',
                error='No file selected'
            )

        file = request.files['file']

        if file.filename == '':

            return render_template(
                'medicine/recognition.html',
                error='No file selected'
            )

        # ====================================================
        # IMAGE PROCESSING
        # ====================================================

        if file and allowed_file(file.filename):

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                filename
            )

            file.save(filepath)

            # ------------------------------------------------
            # OCR
            # ------------------------------------------------

            ocr_result = extract_text_from_image(
                filepath
            )

            extracted_text = ocr_result.get(
                "text",
                ""
            )

            ocr_confidence = ocr_result.get(
                "confidence",
                0.0
            )

            ocr_quality = ocr_result.get(
                "quality_score",
                0.0
            )

            # ------------------------------------------------
            # SMART MEDICINE RECOGNITION
            # ------------------------------------------------

            medicine_result = recognize_medicine_from_text(
                extracted_text,
                ocr_confidence=ocr_confidence
            )

            # ------------------------------------------------
            # OLD FORMATTED RESULT
            # ------------------------------------------------

            medicine_info = get_medicine_info(
                extracted_text
            )

            print(
                "\n========== STRUCTURED MEDICINE RESULT =========="
            )

            print(
                json.dumps(
                    medicine_result,
                    indent=4,
                    ensure_ascii=False
                )
            )

            print(
                "=================================================\n"
            )

            os.remove(filepath)

            return render_template(
                'medicine/recognition.html',
                extracted_text=extracted_text,
                medicine_info=medicine_info,
                medicine_result=medicine_result,
                show_result=True
            )

        else:

            return render_template(
                'medicine/recognition.html',
                error=(
                    'Invalid file type. '
                    'Please upload PNG, JPG, or JPEG.'
                )
            )

    return render_template(
        'medicine/recognition.html',
        show_result=False
    )