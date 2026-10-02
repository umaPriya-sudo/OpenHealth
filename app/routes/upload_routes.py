from flask import Blueprint, current_app, send_from_directory

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename
    )