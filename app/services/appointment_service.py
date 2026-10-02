import uuid

from app.database.connection import get_db_connection


def generate_appointment_id():
    """
    Generate a unique user-facing appointment ID.
    Example: OH-APT-A1B2C3D4
    """

    unique_part = uuid.uuid4().hex[:8].upper()

    return f"OH-APT-{unique_part}"


def create_appointment(
    user_id,
    doctor_id,
    appointment_date,
    appointment_time,
    consultation_type,
    reason=""
):
    """
    Create and save a new appointment.
    """

    connection = get_db_connection()

    if not connection:
        return None

    try:
        appointment_id = generate_appointment_id()

        cursor = connection.cursor()

        query = """
            INSERT INTO appointments (
                appointment_id,
                user_id,
                doctor_id,
                appointment_date,
                appointment_time,
                consultation_type,
                reason,
                status
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (
            appointment_id,
            user_id,
            doctor_id,
            appointment_date,
            appointment_time,
            consultation_type,
            reason,
            "Confirmed"
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        return {
            "appointment_id": appointment_id,
            "user_id": user_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "consultation_type": consultation_type,
            "reason": reason,
            "status": "Confirmed"
        }

    except Exception as e:

        connection.rollback()

        print(
            f"Appointment creation error: {e}"
        )

        return None

    finally:

        try:
            cursor.close()
        except Exception:
            pass

        connection.close()

def get_user_appointments(user_id):
    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.appointment_id,
                a.user_id,
                a.doctor_id,
                a.appointment_date,
                a.appointment_time,
                a.consultation_type,
                a.reason,
                a.status,
                a.booking_created_at,
                a.appointment_notes,
                a.cancellation_reason,

                u.full_name AS doctor_name,
                d.specialization AS doctor_specialty,
                d.qualification AS doctor_qualification,
                d.experience_years AS doctor_experience,
                d.clinic_name AS doctor_clinic,
                d.city AS doctor_location

            FROM appointments a

            LEFT JOIN doctors d
                ON CAST(a.doctor_id AS CHAR) = CAST(d.id AS CHAR)
                OR CAST(a.doctor_id AS CHAR) = CAST(d.registration_number AS CHAR)

            LEFT JOIN users u
                ON d.user_id = u.id

            WHERE a.user_id = %s

            ORDER BY
                a.appointment_date ASC,
                a.appointment_time ASC
        """, (user_id,))

        appointments = cursor.fetchall()

        return appointments

    except Exception as e:
        print(f"Get user appointments error: {e}")
        return []

    finally:
        cursor.close()
        connection.close()
        connection.close()


def cancel_appointment(
    appointment_id,
    user_id,
    cancellation_reason=""
):
    """
    Cancel an appointment belonging to the logged-in user.
    """

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE appointments
            SET
                status = %s,
                cancellation_reason = %s
            WHERE
                appointment_id = %s
                AND user_id = %s
                AND status = %s
            """,
            (
                "Cancelled",
                cancellation_reason,
                appointment_id,
                user_id,
                "Confirmed"
            )
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return False

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(
            f"Cancel appointment error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()

def get_appointment_by_id(
    appointment_id,
    user_id
):
    """
    Get one appointment belonging to the logged-in user.
    """

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                appointment_id,
                user_id,
                doctor_id,
                appointment_date,
                appointment_time,
                consultation_type,
                reason,
                status,
                booking_created_at,
                appointment_notes,
                cancellation_reason
            FROM appointments
            WHERE
                appointment_id = %s
                AND user_id = %s
            """,
            (
                appointment_id,
                user_id
            )
        )

        appointment = cursor.fetchone()

        return appointment

    except Exception as e:

        print(
            f"Get appointment error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()

def reschedule_appointment(
    appointment_id,
    user_id,
    new_date,
    new_time
):
    """
    Reschedule an existing confirmed appointment
    belonging to the logged-in user.
    """

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            UPDATE appointments
            SET
                appointment_date = %s,
                appointment_time = %s
            WHERE
                appointment_id = %s
                AND user_id = %s
                AND status = %s
            """,
            (
                new_date,
                new_time,
                appointment_id,
                user_id,
                "Confirmed"
            )
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(
            f"Appointment rescheduling error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()