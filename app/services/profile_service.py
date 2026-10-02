from app.database.connection import get_db_connection


def get_user_profile(user_id):
    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                id,
                full_name,
                email,
                auth_provider,
                profile_image,
                email_verified,
                last_login_at
            FROM users
            WHERE id = %s
            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    except Exception as e:

        print(
            f"User profile retrieval error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()

def get_user_activity(user_id):
    """
    Get recent activities of the logged-in user.
    """

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        activities = []

        # --------------------------------------------------
        # 1. Health prediction records
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT
                record_id,
                disease_name,
                prediction_type,
                created_at
            FROM health_prediction_records
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        prediction_records = cursor.fetchall()

        for record in prediction_records:

            activities.append({
                "type": record["prediction_type"],
                "title": record["disease_name"],
                "description": "AI health prediction completed",
                "date": record["created_at"],
                "icon": "fa-brain",
                "record_id": record["record_id"]
            })


        # --------------------------------------------------
        # 2. Appointments
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT
                appointment_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status,
                booking_created_at
            FROM appointments
            WHERE user_id = %s
            ORDER BY booking_created_at DESC
            """,
            (user_id,)
        )

        appointments = cursor.fetchall()

        for appointment in appointments:

            activities.append({
                "type": "Appointment",
                "title": "Doctor Appointment",
                "description": (
                    f"Appointment with Doctor ID "
                    f"{appointment['doctor_id']}"
                ),
                "date": appointment["booking_created_at"],
                "icon": "fa-calendar-check",
                "status": appointment["status"],
                "appointment_date": appointment["appointment_date"],
                "appointment_time": appointment["appointment_time"],
                "appointment_id": appointment["appointment_id"]
            })


        # --------------------------------------------------
        # Sort all activities by date
        # --------------------------------------------------

        activities.sort(
            key=lambda activity: activity["date"],
            reverse=True
        )

        return activities

    except Exception as e:

        print(
            f"User activity retrieval error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()


def update_user_profile(
    user_id,
    full_name,
    profile_image=None
):
    """
    Update basic profile information.
    """

    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:

        if profile_image is not None:

            cursor.execute(
                """
                UPDATE users
                SET
                    full_name = %s,
                    profile_image = %s
                WHERE id = %s
                """,
                (
                    full_name,
                    profile_image,
                    user_id
                )
            )

        else:

            cursor.execute(
                """
                UPDATE users
                SET
                    full_name = %s
                WHERE id = %s
                """,
                (
                    full_name,
                    user_id
                )
            )

        connection.commit()

        return cursor.rowcount > 0

    except Exception as e:

        connection.rollback()

        print(
            f"User profile update error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()