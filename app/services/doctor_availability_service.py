from app.database.connection import get_db_connection


def get_doctor_availability(doctor_id):
    """
    Get active availability schedules for a doctor.
    """

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
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
              AND is_available = TRUE
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
            """,
            (doctor_id,)
        )

        return cursor.fetchall()

    except Exception as e:

        print(
            f"Get doctor availability error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()