from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)


@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('main.html', page='error'), 404


@error_bp.app_errorhandler(500)
def internal_error(e):
    return render_template('main.html', page='error'), 500