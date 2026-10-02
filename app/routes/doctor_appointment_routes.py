from flask import Blueprint, jsonify, session, request, render_template, redirect, url_for
from app.database.connection import get_db_connection


doctor_appointment_bp = Blueprint(
    "doctor_appointment",
    __name__,
    url_prefix="/doctor/appointments"
)


# =========================================================
# DOCTOR ACCESS CHECK
# =========================================================

def get_logged_in_doctor():

    if "user_id" not in session:
        return None

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                u.id AS user_id,
                u.role,
                d.registration_number AS doctor_id
            FROM users u
            INNER JOIN doctors d
                ON d.user_id = u.id
            WHERE u.id = %s
              AND u.role = 'doctor'
            """,
            (session["user_id"],)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


@doctor_appointment_bp.route("/manage", methods=["GET"])
def appointment_management_page():

    doctor = get_logged_in_doctor()

    if not doctor:
        return redirect(url_for("general.index"))

    return render_template(
        "doctor/appointments.html"
    )

# =========================================================
# GET ALL DOCTOR APPOINTMENTS
# =========================================================

@doctor_appointment_bp.route("", methods=["GET"])
def get_appointments():

    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Doctor authentication required."
        }), 401


    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500


    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                a.id,
                a.appointment_id,
                a.user_id AS patient_id,
                a.doctor_id,
                a.appointment_date,
                a.appointment_time,
                a.consultation_type,
                a.reason,
                a.status,
                a.booking_created_at,
                a.appointment_notes,
                a.cancellation_reason,

                u.full_name AS patient_name,
                u.email AS patient_email

            FROM appointments a

            INNER JOIN users u
                ON u.id = a.user_id

            WHERE a.doctor_id = %s

            ORDER BY
                a.appointment_date DESC,
                a.appointment_time DESC
            """,
            (doctor["doctor_id"],)
        )

        appointments = cursor.fetchall()


        return jsonify({
            "success": True,
            "appointments": appointments
        }), 200


    except Exception as e:

        print(f"Get doctor appointments error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to load appointments."
        }), 500


    finally:
        cursor.close()
        connection.close()


# =========================================================
# UPDATE APPOINTMENT STATUS
# =========================================================

@doctor_appointment_bp.route(
    "/<int:appointment_id>/status",
    methods=["POST"]
)
def update_appointment_status(appointment_id):

    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Doctor authentication required."
        }), 401


    data = request.get_json(silent=True) or {}

    new_status = data.get("status", "").strip()


    allowed_statuses = {
        "Confirmed",
        "Rejected",
        "Completed"
    }


    if new_status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid appointment status."
        }), 400


    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500


    cursor = connection.cursor(dictionary=True)

    try:

        # -----------------------------------------
        # Make sure appointment belongs to doctor
        # -----------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                appointment_id,
                status
            FROM appointments
            WHERE id = %s
              AND doctor_id = %s
            """,
            (
                appointment_id,
                doctor["doctor_id"]
            )
        )

        appointment = cursor.fetchone()


        if not appointment:

            return jsonify({
                "success": False,
                "message": "Appointment not found."
            }), 404


        # -----------------------------------------
        # Update status
        # -----------------------------------------

        cursor.execute(
            """
            UPDATE appointments
            SET
                status = %s
            WHERE id = %s
              AND doctor_id = %s
            """,
            (
                new_status,
                appointment_id,
                doctor["doctor_id"]
            )
        )


        connection.commit()


        return jsonify({
            "success": True,
            "message": f"Appointment marked as {new_status}.",
            "status": new_status
        }), 200


    except Exception as e:

        connection.rollback()

        print(
            f"Update appointment status error: {e}"
        )

        return jsonify({
            "success": False,
            "message": "Unable to update appointment."
        }), 500


    finally:
        cursor.close()
        connection.close()