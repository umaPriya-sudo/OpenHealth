from flask import Blueprint, render_template, request, session, redirect

from datetime import date, timedelta, datetime

from app.services.doctor_service import (
    get_all_doctors_from_db
)

from app.services.doctor_availability_service import (
    get_doctor_availability
)

from app.services.appointment_service import (
    create_appointment,
    get_user_appointments,
    cancel_appointment,
    get_appointment_by_id,
    reschedule_appointment
)

appointment_bp = Blueprint(
    "appointment",
    __name__
)


@appointment_bp.route("/doctor-appointment")
def doctor_appointment():
    return render_template(
        "appointment/appointment.html"
    )


@appointment_bp.route("/doctor-appointment/doctors")
def doctor_listing():

    specialty = request.args.get(
        "specialty",
        ""
    ).strip()

    search = request.args.get(
        "search",
        ""
    ).strip()

    doctors = get_all_doctors_from_db()

    if specialty:
        doctors = [
            doctor
            for doctor in doctors
            if (doctor.get("specialty") or "").strip().lower()
            == specialty.strip().lower()
        ]
    
    elif search:
        from app.services.doctor_service import (
            search_doctors
        )
    
        doctors = search_doctors(
            search
        )

    return render_template(
        "appointment/doctors.html",
        doctors=doctors,
        specialty=specialty,
        search=search
    )


@appointment_bp.route("/doctor-appointment/doctor/<doctor_id>")
def doctor_profile(doctor_id):

    from app.services.doctor_service import (
        get_doctor_from_db_by_id
    )

    doctor = get_doctor_from_db_by_id(
        doctor_id
    )

    if not doctor:
        return "Doctor not found", 404

    availability = get_doctor_availability(
        doctor["registration_number"]
    )

    # -----------------------------------------------------
    # Consultation types available for this doctor
    # -----------------------------------------------------

    available_consultation_types = set()

    for item in availability:

        consultation_type = (
            item.get("consultation_type") or ""
        ).strip()

        if consultation_type == "Both":
            available_consultation_types.add("In-person")
            available_consultation_types.add("Online")

        elif consultation_type == "In-person":
            available_consultation_types.add("In-person")

        elif consultation_type == "Video Consultation":
            available_consultation_types.add("Online")

    available_dates = []

    today = date.today()

    booking_window_start = today
    booking_window_end = today + timedelta(days=34)

    for offset in range(35):

        current_date = today + timedelta(days=offset)

        weekday = current_date.strftime("%A")

        if any(
            item["day_of_week"] == weekday
            for item in availability
        ):

            available_dates.append(
                {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": current_date.strftime("%a"),
                    "day_number": current_date.strftime("%d"),
                    "month": current_date.strftime("%b")
                }
            )

        if len(available_dates) >= 5:
            break

    
        available_time_slots = []
    
        for item in availability:
        
            start_time = item["start_time"]
            end_time = item["end_time"]
            
            try:
                start = datetime.strptime(
                    start_time,
                    "%I:%M %p"
                )
            except ValueError:
                start = datetime.strptime(
                    start_time,
                    "%H:%M"
                )
            
            try:
                end = datetime.strptime(
                    end_time,
                    "%I:%M %p"
                )
            except ValueError:
                end = datetime.strptime(
                    end_time,
                    "%H:%M"
                )
    
            current_time = start
    
            while current_time <= end:
            
                available_time_slots.append(
                    current_time.strftime("%I:%M %p")
                )
    
                current_time += timedelta(minutes=30)

    return render_template(
        "appointment/doctor_profile.html",
        doctor=doctor,
        availability=availability,
        available_dates=available_dates,
        available_time_slots=available_time_slots,
        booking_window_start=booking_window_start,
        booking_window_end=booking_window_end,
        available_consultation_types=available_consultation_types
    )


@appointment_bp.route(
    "/doctor-appointment/details",
    methods=["GET", "POST"]
)
def appointment_details():

    if request.method == "POST":

        doctor_id = request.form.get(
            "doctor_id",
            ""
        ).strip()

        appointment_date = request.form.get(
            "appointment_date",
            ""
        ).strip()

        appointment_time = request.form.get(
            "appointment_time",
            ""
        ).strip()

        consultation_type = request.form.get(
            "consultation_type",
            ""
        ).strip()

        from app.services.doctor_service import (
            get_doctor_by_id
        )

        doctor = get_doctor_by_id(
            doctor_id
        )

        if not doctor:
            return "Doctor not found", 404

        return render_template(
            "appointment/appointment_details.html",
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            consultation_type=consultation_type
        )

    return "Invalid appointment request", 400

@appointment_bp.route(
    "/doctor-appointment/confirmation",
    methods=["POST"]
)
def appointment_confirmation():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to book an appointment.", 401


    # -----------------------------------------------------
    # Get logged-in user
    # -----------------------------------------------------

    user_id = session["user_id"]


    # -----------------------------------------------------
    # Read appointment details
    # -----------------------------------------------------

    doctor_id = request.form.get(
        "doctor_id",
        ""
    ).strip()

    appointment_date = request.form.get(
        "appointment_date",
        ""
    ).strip()

    appointment_time = request.form.get(
        "appointment_time",
        ""
    ).strip()

    consultation_type = request.form.get(
        "consultation_type",
        ""
    ).strip()

    reason = request.form.get(
        "reason",
        ""
    ).strip()


    # -----------------------------------------------------
    # Get doctor
    # -----------------------------------------------------

    from app.services.doctor_service import (
        get_doctor_by_id
    )

    doctor = get_doctor_by_id(
        doctor_id
    )


    if not doctor:

        return "Doctor not found", 404


    # -----------------------------------------------------
    # Create appointment in database
    # -----------------------------------------------------

    appointment = create_appointment(
        user_id=user_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        consultation_type=consultation_type,
        reason=reason
    )


    # -----------------------------------------------------
    # Database error
    # -----------------------------------------------------

    if not appointment:

        return (
            "Unable to create appointment. "
            "Please try again.",
            500
        )


    # -----------------------------------------------------
    # Show success page
    # -----------------------------------------------------

    return render_template(
        "appointment/appointment_success.html",
        appointment_id=appointment["appointment_id"],
        doctor=doctor,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        consultation_type=consultation_type
    )


@appointment_bp.route(
    "/my-appointments"
)
def my_appointments():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to view your appointments.", 401


    # -----------------------------------------------------
    # Get logged-in user's appointments
    # -----------------------------------------------------

    user_id = session["user_id"]

    appointments = get_user_appointments(
        user_id
    )


    # -----------------------------------------------------
    # Attach doctor information
    # -----------------------------------------------------

    from app.services.doctor_service import (
        get_doctor_by_id
    )

    for appointment in appointments:

        appointment["doctor"] = get_doctor_by_id(
            appointment["doctor_id"]
        )


    # -----------------------------------------------------
    # Render page
    # -----------------------------------------------------

    return render_template(
        "appointment/my_appointments.html",
        appointments=appointments
    )


@appointment_bp.route(
    "/my-appointments/cancel",
    methods=["POST"]
)
def cancel_my_appointment():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to manage your appointments.", 401


    # -----------------------------------------------------
    # Get logged-in user
    # -----------------------------------------------------

    user_id = session["user_id"]


    # -----------------------------------------------------
    # Read appointment details
    # -----------------------------------------------------

    appointment_id = request.form.get(
        "appointment_id",
        ""
    ).strip()

    cancellation_reason = request.form.get(
        "cancellation_reason",
        ""
    ).strip()


    if not appointment_id:

        return "Appointment ID is required.", 400


    # -----------------------------------------------------
    # Cancel appointment
    # -----------------------------------------------------

    success = cancel_appointment(
        appointment_id=appointment_id,
        user_id=user_id,
        cancellation_reason=cancellation_reason
    )


    if not success:

        return (
            "Unable to cancel appointment. "
            "The appointment may not exist or may already be cancelled.",
            400
        )


    # -----------------------------------------------------
    # Return to My Appointments
    # -----------------------------------------------------

    return redirect(
        "/my-appointments"
    )


@appointment_bp.route(
    "/my-appointments/<appointment_id>"
)
def my_appointment_details(
    appointment_id
):

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to view your appointment.", 401


    # -----------------------------------------------------
    # Get logged-in user's appointment
    # -----------------------------------------------------

    user_id = session["user_id"]

    appointment = get_appointment_by_id(
        appointment_id,
        user_id
    )


    if not appointment:

        return "Appointment not found.", 404


    # -----------------------------------------------------
    # Get doctor information
    # -----------------------------------------------------

    from app.services.doctor_service import (
        get_doctor_by_id
    )

    doctor = get_doctor_by_id(
        appointment["doctor_id"]
    )


    # -----------------------------------------------------
    # Render details page
    # -----------------------------------------------------

    return render_template(
        "appointment/my_appointment_details.html",
        appointment=appointment,
        doctor=doctor
    )

@appointment_bp.route(
    "/my-appointments/reschedule",
    methods=["POST"]
)
def reschedule_my_appointment():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to reschedule your appointment.", 401


    # -----------------------------------------------------
    # Get form data
    # -----------------------------------------------------

    appointment_id = request.form.get(
        "appointment_id",
        ""
    ).strip()

    new_date = request.form.get(
        "appointment_date",
        ""
    ).strip()

    new_time = request.form.get(
        "appointment_time",
        ""
    ).strip()


    # -----------------------------------------------------
    # Validate required fields
    # -----------------------------------------------------

    if not appointment_id or not new_date or not new_time:

        return "Please select a new date and time.", 400


    # -----------------------------------------------------
    # Reschedule appointment
    # -----------------------------------------------------

    success = reschedule_appointment(
        appointment_id=appointment_id,
        user_id=session["user_id"],
        new_date=new_date,
        new_time=new_time
    )


    if not success:

        return "Unable to reschedule this appointment.", 400


    # -----------------------------------------------------
    # Return to appointment details
    # -----------------------------------------------------

    return redirect(
        f"/my-appointments/{appointment_id}"
    )