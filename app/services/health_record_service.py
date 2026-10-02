import uuid
import json

from app.database.connection import get_db_connection


def generate_health_record_id():
    unique_part = uuid.uuid4().hex[:8].upper()

    return f"OH-HR-{unique_part}"


def save_prediction_record(
    user_id,
    disease_name,
    prediction_result,
    confidence=None,
    prediction_type="Disease Prediction",
    input_data=None,
    result_details=None
):
    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor()

    try:

        record_id = generate_health_record_id()

        query = """
            INSERT INTO health_prediction_records (
                record_id,
                user_id,
                disease_name,
                prediction_result,
                confidence,
                prediction_type,
                input_data,
                result_details
            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        values = (
            record_id,
            user_id,
            disease_name,
            json.dumps(prediction_result) if prediction_result is not None else None,
            confidence,
            prediction_type,
            json.dumps(input_data) if input_data is not None else None,
            json.dumps(result_details) if result_details is not None else None
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        return {
            "record_id": record_id,
            "user_id": user_id,
            "disease_name": disease_name,
            "prediction_result": prediction_result,
            "confidence": confidence,
            "prediction_type": prediction_type
        }

    except Exception as e:

        connection.rollback()

        print(
            f"Health record save error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()


def get_user_prediction_records(user_id):

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                record_id,
                user_id,
                disease_name,
                prediction_result,
                confidence,
                prediction_type,
                input_data,
                result_details,
                created_at
            FROM health_prediction_records
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        records = cursor.fetchall()

        return records

    except Exception as e:

        print(
            f"Health records retrieval error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()

def get_prediction_record_by_id(
    record_id,
    user_id
):

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                record_id,
                user_id,
                disease_name,
                prediction_result,
                confidence,
                prediction_type,
                input_data,
                result_details,
                created_at
            FROM health_prediction_records
            WHERE
                record_id = %s
                AND user_id = %s
            LIMIT 1
            """,
            (
                record_id,
                user_id
            )
        )

        record = cursor.fetchone()

        return record

    except Exception as e:

        print(
            f"Health record detail retrieval error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()

def delete_prediction_record(record_id, user_id):
    connection = get_db_connection()

    if not connection:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM health_prediction_records
            WHERE record_id = %s
              AND user_id = %s
            """,
            (record_id, user_id)
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception as e:

        connection.rollback()

        print(
            f"Health record deletion error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()