from datetime import datetime, date, time

from flask import Blueprint, render_template, session, redirect

from app.services.appointment_service import get_user_appointments


patient_dashboard_bp = Blueprint(
    "patient_dashboard",
    __name__
)


def parse_appointment_date(value):
    """
    Convert appointment date into a Python date object.

    Supports:
    - datetime.date
    - datetime.datetime
    - YYYY-MM-DD
    - DD-MM-YYYY
    - DD/MM/YYYY
    - ISO datetime strings
    """

    if not value:
        return None

    # Already a datetime
    if isinstance(value, datetime):
        return value.date()

    # Already a date
    if isinstance(value, date):
        return value

    # String value
    if isinstance(value, str):

        value = value.strip()

        formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%Y-%m-%d %H:%M:%S"
        ]

        for date_format in formats:

            try:

                parsed = datetime.strptime(
                    value,
                    date_format
                )

                return parsed.date()

            except ValueError:
                continue

    return None


def parse_appointment_time(value):
    """
    Convert appointment time into a Python time object.

    Supports:
    - datetime.time
    - HH:MM:SS
    - HH:MM
    """

    if not value:
        return time(0, 0)

    # Already a time object
    if isinstance(value, time):
        return value

    # String value
    if isinstance(value, str):

        value = value.strip()

        formats = [
            "%H:%M:%S",
            "%H:%M",
            "%I:%M %p",
            "%I:%M:%S %p"
        ]

        for time_format in formats:

            try:

                return datetime.strptime(
                    value,
                    time_format
                ).time()

            except ValueError:
                continue

    return time(0, 0)


@patient_dashboard_bp.route("/patient/dashboard")
def patient_dashboard():

    # ==========================================
    # USER MUST BE LOGGED IN
    # ==========================================

    if "user_id" not in session:
        return redirect("/")


    # ==========================================
    # ONLY PATIENTS CAN ACCESS THIS DASHBOARD
    # ==========================================

    if session.get("role") != "patient":
        return redirect("/")


    # ==========================================
    # GET LOGGED-IN PATIENT
    # ==========================================

    user_id = session.get("user_id")


    # ==========================================
    # GET PATIENT APPOINTMENTS
    # ==========================================

    appointments = get_user_appointments(user_id)

    print("\n========== PATIENT APPOINTMENTS ==========")
    print(appointments)
    print("==========================================\n")


    # ==========================================
    # FIND UPCOMING CONFIRMED APPOINTMENT
    # ==========================================

    upcoming_appointment = None

    now = datetime.now()

    for appointment in appointments:

        # Only confirmed appointments
        if appointment.get("status") != "Confirmed":
            continue


        # --------------------------------------
        # Parse appointment date
        # --------------------------------------

        appointment_date = parse_appointment_date(
            appointment.get("appointment_date")
        )

        if not appointment_date:
            continue


        # --------------------------------------
        # Parse appointment time
        # --------------------------------------

        appointment_time = parse_appointment_time(
            appointment.get("appointment_time")
        )


        # --------------------------------------
        # Combine date + time
        # --------------------------------------

        appointment_datetime = datetime.combine(
            appointment_date,
            appointment_time
        )


        # --------------------------------------
        # Find first future appointment
        # --------------------------------------

        if appointment_datetime >= now:

            upcoming_appointment = appointment

            break


    # ==========================================
    # RENDER PATIENT DASHBOARD
    # ==========================================

    return render_template(
        "patient/dashboard.html",
    
        user={
            "id": session.get("user_id"),
            "full_name": session.get("full_name"),
            "email": session.get("email"),
            "role": session.get("role")
        },
    
        appointments=appointments,
    
        upcoming_appointment=upcoming_appointment,
    
        appointment_count=len(appointments)
    )