from flask import Blueprint, render_template, session, redirect, url_for
from app.database.connection import get_db_connection


doctor_bp = Blueprint(
    "doctor",
    __name__,
    url_prefix="/doctor"
)


@doctor_bp.route("/dashboard")
def doctor_dashboard():

    # -----------------------------------------
    # Check login
    # -----------------------------------------

    if "user_id" not in session:
        return redirect(url_for("general.index"))


    user_id = session["user_id"]

    connection = get_db_connection()

    if not connection:
        return "Database connection failed.", 500

    cursor = connection.cursor(dictionary=True)

    try:

        # -----------------------------------------
        # Check whether logged-in user is a doctor
        # -----------------------------------------

        cursor.execute(
            """
            SELECT
                u.id,
                u.full_name,
                u.email,
                u.role,
                d.id AS doctor_db_id,
                d.registration_number AS doctor_id,
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
            LEFT JOIN doctors d
                ON d.user_id = u.id
            WHERE u.id = %s
            """,
            (user_id,)
        )

        doctor = cursor.fetchone()


        # -----------------------------------------
        # Doctor-only protection
        # -----------------------------------------

        if not doctor or doctor["role"] != "doctor":
            return redirect(url_for("general.index"))


        doctor_db_id = doctor["doctor_db_id"]
        doctor_registration_number = doctor["doctor_id"]


        # -----------------------------------------
        # Today's appointments
        # -----------------------------------------

        cursor.execute(
            """
            SELECT
                a.id,
                a.appointment_id,
                a.user_id,
                a.appointment_date,
                a.appointment_time,
                a.consultation_type,
                a.reason,
                a.status,
                u.full_name AS patient_name,
                u.email AS patient_email
            FROM appointments a
            LEFT JOIN users u
                ON u.id = a.user_id
            WHERE a.doctor_id IN (%s, %s)
                AND STR_TO_DATE(
                    a.appointment_date,
                    '%Y-%m-%d'
                  ) = CURDATE()
            ORDER BY a.appointment_time ASC
            """,
            (
                str(doctor_db_id),
                str(doctor_registration_number)
            )
        )

        today_appointments = cursor.fetchall()


        # -----------------------------------------
        # Upcoming appointments
        # -----------------------------------------

        cursor.execute(
            """
            SELECT
                a.id,
                a.appointment_id,
                a.user_id,
                a.appointment_date,
                a.appointment_time,
                a.consultation_type,
                a.reason,
                a.status,
                u.full_name AS patient_name,
                u.email AS patient_email
            FROM appointments a
            LEFT JOIN users u
                ON u.id = a.user_id
            WHERE a.doctor_id IN (%s, %s)
              AND STR_TO_DATE(
                    a.appointment_date,
                    '%Y-%m-%d'
                  ) > CURDATE()
                  AND a.status = 'Confirmed'
            ORDER BY
                STR_TO_DATE(
                    a.appointment_date,
                    '%Y-%m-%d'
                ) ASC,
                a.appointment_time ASC
            LIMIT 10
            """,
            (
                str(doctor_db_id),
                str(doctor_registration_number)
            )
        )

        upcoming_appointments = cursor.fetchall()


        # -----------------------------------------
        # Total patients
        # -----------------------------------------

        cursor.execute(
            """
            SELECT COUNT(DISTINCT user_id) AS total_patients
            FROM appointments
            WHERE doctor_id IN (%s, %s)
            """,
            (
                str(doctor_db_id),
                str(doctor_registration_number)
            )
        )

        patient_result = cursor.fetchone()

        total_patients = patient_result["total_patients"] or 0


        # -----------------------------------------
        # Total appointments
        # -----------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total_appointments
            FROM appointments
            WHERE doctor_id IN (%s, %s)
            """,
            (
                str(doctor_db_id),
                str(doctor_registration_number)
            )
        )

        appointment_result = cursor.fetchone()

        total_appointments = (
            appointment_result["total_appointments"] or 0
        )


        return render_template(
            "doctor/dashboard.html",
            doctor=doctor,
            today_appointments=today_appointments,
            upcoming_appointments=upcoming_appointments,
            total_patients=total_patients,
            total_appointments=total_appointments
        )


    except Exception as e:

        print(f"Doctor dashboard error: {e}")

        return "Unable to load doctor dashboard.", 500


    finally:

        cursor.close()
        connection.close()