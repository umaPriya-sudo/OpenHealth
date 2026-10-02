import os

from flask import Flask


def create_app():

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.config['MAX_CONTENT_LENGTH'] = (
        16 * 1024 * 1024
    )

    app.config['ALLOWED_EXTENSIONS'] = {
        'png',
        'jpg',
        'jpeg',
        'gif',
        'bmp'
    }

    os.makedirs(
        app.config['UPLOAD_FOLDER'],
        exist_ok=True
    )

    return app