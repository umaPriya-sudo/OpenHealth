import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_verification_email(
    recipient_email,
    otp
):
    """
    Send email verification OTP.
    """

    mail_server = os.getenv("MAIL_SERVER")
    mail_port = int(
        os.getenv("MAIL_PORT", 587)
    )
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_use_tls = (
        os.getenv(
            "MAIL_USE_TLS",
            "true"
        ).lower() == "true"
    )

    if not mail_server:
        print("MAIL_SERVER is not configured.")
        return False

    if not mail_username:
        print("MAIL_USERNAME is not configured.")
        return False

    if not mail_password:
        print("MAIL_PASSWORD is not configured.")
        return False

    message = EmailMessage()

    message["Subject"] = (
        "OpenHealth - Verify Your Email"
    )

    message["From"] = mail_username
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

Welcome to OpenHealth.

Your email verification code is:

{otp}

This code will expire in 10 minutes.

If you did not create an OpenHealth account,
you can safely ignore this email.

Regards,
OpenHealth Team
"""
    )

    try:

        with smtplib.SMTP(
            mail_server,
            mail_port
        ) as server:

            if mail_use_tls:
                server.starttls()

            server.login(
                mail_username,
                mail_password
            )

            server.send_message(message)

        print(
            f"Verification email sent to {recipient_email}"
        )

        return True

    except Exception as e:

        print(
            f"Email sending error: {e}"
        )

        return False