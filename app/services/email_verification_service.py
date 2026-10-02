import hashlib
import secrets
from datetime import datetime, timedelta

from app.database.connection import get_db_connection
from app.services.mail_service import send_verification_email


OTP_EXPIRY_MINUTES = 10


def generate_otp():
    """
    Generate a secure 6-digit OTP.
    """

    return f"{secrets.randbelow(1000000):06d}"


def hash_otp(otp):
    """
    Hash OTP before storing it in the database.
    """

    return hashlib.sha256(
        otp.encode("utf-8")
    ).hexdigest()


def create_and_send_verification_code(
    user_id,
    email
):
    """
    Generate an OTP, store its hash,
    and send the OTP to the user's email.
    """

    otp = generate_otp()
    otp_hash = hash_otp(otp)

    expires_at = (
        datetime.now()
        + timedelta(
            minutes=OTP_EXPIRY_MINUTES
        )
    )

    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO email_verification_codes
            (
                user_id,
                otp_hash,
                expires_at,
                attempts
            )
            VALUES
            (
                %s,
                %s,
                %s,
                0
            )
            ON DUPLICATE KEY UPDATE
                otp_hash = VALUES(otp_hash),
                expires_at = VALUES(expires_at),
                attempts = 0
            """,
            (
                user_id,
                otp_hash,
                expires_at
            )
        )

        connection.commit()

    except Exception as e:

        connection.rollback()

        print(
            f"OTP database error: {e}"
        )

        cursor.close()
        connection.close()

        return False, "Unable to create verification code."


    cursor.close()
    connection.close()


    # Send the actual OTP email

    email_sent = send_verification_email(
        email,
        otp
    )


    if not email_sent:

        return False, "Unable to send verification email."


    return True, "Verification code sent successfully."

def verify_email_code(
    user_id,
    otp
):
    """
    Verify the email OTP for a user.
    """

    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed."

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                id,
                otp_hash,
                expires_at,
                attempts
            FROM email_verification_codes
            WHERE user_id = %s
            LIMIT 1
            """,
            (user_id,)
        )

        verification = cursor.fetchone()

        if not verification:
            return False, "No verification code found."


        # Check expiry

        if datetime.now() > verification["expires_at"]:

            return False, (
                "Verification code has expired. "
                "Please request a new code."
            )


        # Check maximum attempts

        if verification["attempts"] >= 5:

            return False, (
                "Too many incorrect attempts. "
                "Please request a new verification code."
            )


        # Compare OTP

        submitted_hash = hash_otp(otp)

        if submitted_hash != verification["otp_hash"]:

            cursor.execute(
                """
                UPDATE email_verification_codes
                SET attempts = attempts + 1
                WHERE id = %s
                """,
                (verification["id"],)
            )

            connection.commit()

            return False, "Invalid verification code."


        # Mark email as verified

        cursor.execute(
            """
            UPDATE users
            SET email_verified = TRUE
            WHERE id = %s
            """,
            (user_id,)
        )


        # Remove used verification code

        cursor.execute(
            """
            DELETE FROM email_verification_codes
            WHERE id = %s
            """,
            (verification["id"],)
        )

        connection.commit()

        return True, "Email verified successfully."


    except Exception as e:

        connection.rollback()

        print(
            f"Email verification error: {e}"
        )

        return False, (
            "Unable to verify email."
        )


    finally:

        cursor.close()
        connection.close()


def resend_verification_code(
    user_id,
    email
):
    """
    Generate and send a new verification code
    for an existing unverified user.
    """

    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed."

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                id,
                email,
                email_verified,
                is_active
            FROM users
            WHERE id = %s
            LIMIT 1
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            return False, "User account not found."

        if not user["is_active"]:
            return False, "This account is inactive."

        if user["email_verified"]:
            return False, "This email is already verified."

        if user["email"].lower() != email.lower():
            return False, "Email verification request is invalid."

    finally:
        cursor.close()
        connection.close()


    # Generate and send a fresh OTP.
    # This also replaces the previous expired OTP.

    return create_and_send_verification_code(
        user_id=user_id,
        email=email
    )