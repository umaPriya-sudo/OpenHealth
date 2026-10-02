from flask import Blueprint, jsonify, render_template, request

from app.services.chatbot_service import get_health_response


chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form.get('message', '')

        if user_message:
            response = get_health_response(user_message)
            return jsonify({'response': response})

        return jsonify({'response': 'Please ask a question!'})

    return render_template(
        'chatbot/chatbot.html',
        page='chatbot'
    )