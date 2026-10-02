from flask import Blueprint, jsonify, render_template, request, session
from app.database.connection import get_db_connection


doctor_profile_bp = Blueprint(
    "doctor_profile",
    __name__,
    url_prefix="/doctor/profile"
)


def get_logged_in_doctor():
    user_id = session.get("user_id")

    if not user_id:
        return None

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                u.id AS user_id,
                u.role,
                d.id AS profile_id,
                d.registration_number,
                d.qualification,
                d.specialization,
                d.experience_years,
                d.bio,
                d.clinic_name,
                d.clinic_address,
                d.city,
                d.consultation_fee,
                d.consultation_types,
                d.verification_status
            FROM users u
            INNER JOIN doctors d
                ON d.user_id = u.id
            WHERE u.id = %s
              AND u.role = 'doctor'
        """, (user_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


@doctor_profile_bp.route("/edit")
def edit_profile():
    doctor = get_logged_in_doctor()

    if not doctor:
        return "Unauthorized", 401

    return render_template(
        "doctor/profile.html",
        doctor=doctor
    )


@doctor_profile_bp.route("/api", methods=["GET"])
def get_profile():
    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    return jsonify({
        "success": True,
        "doctor": doctor
    })


@doctor_profile_bp.route("/api", methods=["PUT"])
def update_profile():
    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    qualification = str(
        data.get("qualification", "")
    ).strip()

    specialization = str(
        data.get("specialization", "")
    ).strip()

    experience_years = data.get("experience_years", 0)

    bio = str(
        data.get("bio", "")
    ).strip()

    clinic_name = str(
        data.get("clinic_name", "")
    ).strip()

    clinic_address = str(
        data.get("clinic_address", "")
    ).strip()

    city = str(
        data.get("city", "")
    ).strip()

    consultation_fee = data.get("consultation_fee")

    consultation_types = str(
        data.get("consultation_types", "")
    ).strip()

    if not qualification:
        return jsonify({
            "success": False,
            "message": "Qualification is required."
        }), 400

    if not specialization:
        return jsonify({
            "success": False,
            "message": "Specialization is required."
        }), 400

    try:
        experience_years = int(experience_years)

        if experience_years < 0:
            raise ValueError

    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Experience must be a valid number."
        }), 400

    if consultation_fee in ("", None):
        consultation_fee = None
    else:
        try:
            consultation_fee = float(consultation_fee)

            if consultation_fee < 0:
                raise ValueError

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Consultation fee must be a valid amount."
            }), 400

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE doctors
            SET
                qualification = %s,
                specialization = %s,
                experience_years = %s,
                bio = %s,
                clinic_name = %s,
                clinic_address = %s,
                city = %s,
                consultation_fee = %s,
                consultation_types = %s
            WHERE id = %s
        """, (
            qualification,
            specialization,
            experience_years,
            bio,
            clinic_name,
            clinic_address,
            city,
            consultation_fee,
            consultation_types,
            doctor["profile_id"]
        ))

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Professional profile updated successfully."
        })

    except Exception as e:
        connection.rollback()

        print(f"Doctor profile update error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to update professional profile."
        }), 500

    finally:
        cursor.close()
        connection.close()