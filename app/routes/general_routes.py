from flask import Blueprint, render_template


general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def index():
    return render_template('home/index.html')


@general_bp.route('/services')
def services():
    return render_template('services/services.html')

@general_bp.route('/symptom-checker')
def symptom_checker():
    return render_template('symptom_checker.html')