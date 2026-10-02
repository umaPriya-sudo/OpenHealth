"""
OpenHealth - AI-Powered Disease Detection with Chatbot & Medicine Recognition
"""
import os
import warnings

from dotenv import load_dotenv
load_dotenv()

warnings.simplefilter('ignore')

from flask import Flask

from app.routes.medicine_routes import medicine_bp
from app.routes.chatbot_routes import chatbot_bp
from app.routes.general_routes import general_bp
from app.routes.breast_cancer_routes import breast_cancer_bp
from app.routes.heart_routes import heart_bp
from app.routes.diabetes_routes import diabetes_bp
from app.routes.brain_routes import brain_bp
from app.routes.kidney_routes import kidney_bp
from app.routes.liver_routes import liver_bp
from app.routes.parkinsons_routes import parkinsons_bp
from app.routes.malaria_routes import malaria_bp
from app.routes.upload_routes import upload_bp
from app.routes.error_routes import error_bp
from app.routes.auth_routes import auth_bp, oauth
from app.routes.symptom_routes import symptom_bp
from app.routes.medicine_info_routes import medicine_info_bp
from app.routes.appointment_routes import appointment_bp
from app.routes.health_record_routes import health_record_bp
from app.routes.profile_routes import profile_bp
from app.routes.doctor_routes import doctor_bp
from app.routes.doctor_appointment_routes import doctor_appointment_bp
from app.routes.doctor_availability_routes import doctor_availability_bp
from app.routes.doctor_profile_routes import doctor_profile_bp
from app.routes.patient_dashboard_routes import patient_dashboard_bp

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Google OAuth configuration
app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")

oauth.init_app(app)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email"
    }
)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(medicine_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(general_bp)
app.register_blueprint(breast_cancer_bp)
app.register_blueprint(heart_bp)
app.register_blueprint(diabetes_bp)
app.register_blueprint(brain_bp)
app.register_blueprint(kidney_bp)
app.register_blueprint(liver_bp)
app.register_blueprint(parkinsons_bp)
app.register_blueprint(malaria_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(error_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(symptom_bp)
app.register_blueprint(medicine_info_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(health_record_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(doctor_appointment_bp)
app.register_blueprint(doctor_availability_bp)
app.register_blueprint(doctor_profile_bp)
app.register_blueprint(patient_dashboard_bp)


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 OpenHealth Server Starting...")
    print("=" * 50)
    print("🎀 Breast Cancer Model: 96% accuracy ✅")
    print("❤️ Heart Disease Model: 85% accuracy ✅")
    print("💉 Diabetes Model: 72% accuracy ✅")
    print("💬 Chatbot: ✅ Enhanced Health Information")
    print("=" * 50)
    print("✅ Server running at: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)