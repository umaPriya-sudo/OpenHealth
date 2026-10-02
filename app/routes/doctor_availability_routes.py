from flask import Blueprint, jsonify, render_template, request, session
from app.database.connection import get_db_connection

from datetime import date, timedelta

doctor_availability_bp = Blueprint(
    "doctor_availability",
    __name__,
    url_prefix="/doctor/availability"
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
                d.registration_number AS doctor_id
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


@doctor_availability_bp.route("/manage")
def manage_availability():
    doctor = get_logged_in_doctor()

    if not doctor:
        return "Unauthorized", 401

    # Patient booking window
    booking_window_start = date.today()
    booking_window_end = booking_window_start + timedelta(days=34)

    return render_template(
        "doctor/availability.html",
        doctor=doctor,
        booking_window_start=booking_window_start,
        booking_window_end=booking_window_end
    )


@doctor_availability_bp.route("/api", methods=["GET"])
def get_availability():

    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id,
                doctor_id,
                day_of_week,
                start_time,
                end_time,
                consultation_type,
                is_available
            FROM doctor_availability
            WHERE doctor_id = %s
            ORDER BY
                FIELD(
                    day_of_week,
                    'Monday',
                    'Tuesday',
                    'Wednesday',
                    'Thursday',
                    'Friday',
                    'Saturday',
                    'Sunday'
                ),
                start_time
        """, (doctor["doctor_id"],))

        availability = cursor.fetchall()

        return jsonify({
            "success": True,
            "availability": availability
        })

    except Exception as e:

        print(f"Availability fetch error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to load availability."
        }), 500

    finally:
        cursor.close()
        connection.close()


@doctor_availability_bp.route("/api", methods=["POST"])
def add_availability():

    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    day_of_week = str(
        data.get("day_of_week", "")
    ).strip()

    start_time = str(
        data.get("start_time", "")
    ).strip()

    end_time = str(
        data.get("end_time", "")
    ).strip()

    consultation_type = str(
        data.get("consultation_type", "Both")
    ).strip()


    if not day_of_week:
        return jsonify({
            "success": False,
            "message": "Please select a day."
        }), 400

    if not start_time or not end_time:
        return jsonify({
            "success": False,
            "message": "Please provide start and end time."
        }), 400


    valid_days = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    }

    if day_of_week not in valid_days:
        return jsonify({
            "success": False,
            "message": "Invalid day selected."
        }), 400


    valid_consultation_types = {
        "Both",
        "In-person",
        "Video Consultation"
    }

    if consultation_type not in valid_consultation_types:
        return jsonify({
            "success": False,
            "message": "Invalid consultation type."
        }), 400


    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            INSERT INTO doctor_availability
            (
                doctor_id,
                day_of_week,
                start_time,
                end_time,
                consultation_type,
                is_available
            )
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (
            doctor["doctor_id"],
            day_of_week,
            start_time,
            end_time,
            consultation_type
        ))

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Availability added successfully.",
            "availability_id": cursor.lastrowid
        })

    except Exception as e:

        connection.rollback()

        print(f"Availability insert error: {e}")

        if "Duplicate entry" in str(e):
            message = "This availability schedule already exists."
        else:
            message = "Unable to add availability."

        return jsonify({
            "success": False,
            "message": message
        }), 400

    finally:
        cursor.close()
        connection.close()


@doctor_availability_bp.route(
    "/api/<int:availability_id>",
    methods=["DELETE"]
)
def delete_availability(availability_id):

    doctor = get_logged_in_doctor()

    if not doctor:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    connection = get_db_connection()

    if not connection:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute("""
            DELETE FROM doctor_availability
            WHERE id = %s
              AND doctor_id = %s
        """, (
            availability_id,
            doctor["doctor_id"]
        ))

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "Availability not found."
            }), 404

        return jsonify({
            "success": True,
            "message": "Availability removed successfully."
        })

    except Exception as e:

        connection.rollback()

        print(f"Availability delete error: {e}")

        return jsonify({
            "success": False,
            "message": "Unable to remove availability."
        }), 500

    finally:
        cursor.close()
        connection.close()