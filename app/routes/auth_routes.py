import os

from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    redirect,
    url_for
)
from authlib.integrations.flask_client import OAuth

from app.services.auth_service import (
    create_user,
    create_doctor,
    authenticate_user,
    get_or_create_google_user
)

from app.services.email_verification_service import (
    create_and_send_verification_code,
    verify_email_code,
    resend_verification_code
)

oauth = OAuth()

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    account_type = data.get("account_type", "").strip().lower()

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # -----------------------------------------
    # Common validation
    # -----------------------------------------

    if account_type not in ["patient", "doctor"]:
        return jsonify({
            "success": False,
            "message": "Please select an account type."
        }), 400

    if not full_name:
        return jsonify({
            "success": False,
            "message": "Full name is required."
        }), 400

    if not email:
        return jsonify({
            "success": False,
            "message": "Email address is required."
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400

    # -----------------------------------------
    # DOCTOR SIGNUP
    # -----------------------------------------

    if account_type == "doctor":

        registration_number = data.get(
            "registration_number",
            ""
        ).strip()

        qualification = data.get(
            "qualification",
            ""
        ).strip()

        specialization = data.get(
            "specialization",
            ""
        ).strip()

        experience_years = data.get(
            "experience_years",
            ""
        )

        bio = data.get(
            "bio",
            ""
        ).strip()

        clinic_name = data.get(
            "clinic_name",
            ""
        ).strip()

        clinic_address = data.get(
            "clinic_address",
            ""
        ).strip()

        city = data.get(
            "city",
            ""
        ).strip()

        consultation_fee = data.get(
            "consultation_fee",
            ""
        )

        consultation_types = data.get(
            "consultation_type",
            []
        )

        # Doctor required fields
        if not registration_number:
            return jsonify({
                "success": False,
                "message": "Medical registration number is required."
            }), 400

        if not qualification:
            return jsonify({
                "success": False,
                "message": "Qualification is required."
            }), 400

        if not specialization:
            return jsonify({
                "success": False,
                "message": "Specialization is required."
            }), 400

        if experience_years in ["", None]:
            return jsonify({
                "success": False,
                "message": "Years of experience is required."
            }), 400

        if not clinic_name:
            return jsonify({
                "success": False,
                "message": "Clinic or hospital name is required."
            }), 400

        if not clinic_address:
            return jsonify({
                "success": False,
                "message": "Clinic address is required."
            }), 400

        if not city:
            return jsonify({
                "success": False,
                "message": "City is required."
            }), 400

        if not consultation_types:
            return jsonify({
                "success": False,
                "message": "Please select at least one consultation type."
            }), 400

        # Convert experience to integer
        try:
            experience_years = int(experience_years)
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Years of experience must be a valid number."
            }), 400

        if experience_years < 0 or experience_years > 70:
            return jsonify({
                "success": False,
                "message": "Please enter a valid experience value."
            }), 400

        # Convert consultation types to a single string
        if isinstance(consultation_types, list):
            consultation_type = ", ".join(
                consultation_types
            )
        else:
            consultation_type = str(
                consultation_types
            )

        # Optional consultation fee
        if consultation_fee in ["", None]:
            consultation_fee = None
        else:
            try:
                consultation_fee = float(
                    consultation_fee
                )
            except (TypeError, ValueError):
                return jsonify({
                    "success": False,
                    "message": "Consultation fee must be a valid number."
                }), 400

            if consultation_fee < 0:
                return jsonify({
                    "success": False,
                    "message": "Consultation fee cannot be negative."
                }), 400

        success, message, user_id = create_doctor(
            full_name=full_name,
            email=email,
            password=password,
            registration_number=registration_number,
            qualification=qualification,
            specialization=specialization,
            experience_years=experience_years,
            bio=bio,
            clinic_name=clinic_name,
            clinic_address=clinic_address,
            city=city,
            consultation_fee=consultation_fee,
            consultation_type=consultation_type
        )

        if not success:
            return jsonify({
                "success": False,
                "message": message
            }), 400


        otp_sent, otp_message = (
            create_and_send_verification_code(
                user_id=user_id,
                email=email
            )
        )

        if not otp_sent:

            return jsonify({
                "success": False,
                "message": (
                    "Doctor account was created, "
                    "but we could not send the "
                    "verification email. Please try again."
                )
            }), 500


        return jsonify({
            "success": True,
            "message": (
                "Doctor registration submitted successfully. "
                "Please check your email for the verification code."
            ),
            "account_type": "doctor",
            "verification_required": True,
            "verification_status": "Pending",
            "user_id": user_id
        }), 201

    # -----------------------------------------
    # PATIENT SIGNUP
    # -----------------------------------------

    success, message, user_id = create_user(
        full_name,
        email,
        password
    )

    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 400


    otp_sent, otp_message = (
        create_and_send_verification_code(
            user_id=user_id,
            email=email
        )
    )

    if not otp_sent:

        return jsonify({
            "success": False,
            "message": (
                "Account was created, "
                "but we could not send the "
                "verification email. Please try again."
            )
        }), 500


    return jsonify({
        "success": True,
        "message": (
            "Account created successfully. "
            "Please check your email for "
            "the verification code."
        ),
        "account_type": "patient",
        "verification_required": True,
        "user_id": user_id
    }), 201


@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    otp = str(
        data.get("otp", "")
    ).strip()


    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required."
        }), 400


    if not otp:
        return jsonify({
            "success": False,
            "message": "Verification code is required."
        }), 400


    if not otp.isdigit() or len(otp) != 6:
        return jsonify({
            "success": False,
            "message": "Please enter a valid 6-digit verification code."
        }), 400


    success, message = verify_email_code(
        user_id=user_id,
        otp=otp
    )


    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 400


    return jsonify({
        "success": True,
        "message": "Email verified successfully."
    }), 200

@auth_bp.route("/resend-verification", methods=["POST"])
def resend_verification():

    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    email = data.get("email", "").strip().lower()


    if not user_id:
        return jsonify({
            "success": False,
            "message": "User ID is required."
        }), 400


    if not email:
        return jsonify({
            "success": False,
            "message": "Email address is required."
        }), 400


    success, message = resend_verification_code(
        user_id=user_id,
        email=email
    )


    if not success:
        return jsonify({
            "success": False,
            "message": message
        }), 400


    return jsonify({
        "success": True,
        "message": (
            "A new verification code has been sent "
            "to your email."
        )
    }), 200

@auth_bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    user = authenticate_user(email, password)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session.clear()

    session["user_id"] = user["id"]
    session["full_name"] = user["full_name"]
    session["email"] = user["email"]
    session["role"] = user["role"]

    return jsonify({
        "success": True,
        "message": "Signed in successfully.",
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200


@auth_bp.route("/status", methods=["GET"])
def auth_status():
    if "user_id" not in session:
        return jsonify({
            "authenticated": False
        }), 200

    return jsonify({
        "authenticated": True,
        "user": {
            "id": session.get("user_id"),
            "full_name": session.get("full_name"),
            "email": session.get("email"),
            "role": session.get("role")
        }
    })

@auth_bp.route("/google", methods=["GET"])
def google_login():

    redirect_uri = url_for(
        "auth.google_callback",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )

@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():

    try:
        token = oauth.google.authorize_access_token()

        user_info = token.get("userinfo")

        if not user_info:
            return redirect("/?google_error=missing_user_info")

        email = user_info.get("email")
        full_name = user_info.get("name") or "OpenHealth User"
        google_id = user_info.get("sub")
        profile_image = user_info.get("picture")
        email_verified = user_info.get("email_verified", False)

        if not email:
            return redirect("/?google_error=missing_email")

        if not email_verified:
            return redirect("/?google_error=email_not_verified")

        user = get_or_create_google_user(
            google_id=google_id,
            full_name=full_name,
            email=email.lower(),
            profile_image=profile_image
        )

        if not user:
            return redirect("/?google_error=account_error")

        session.clear()

        session["user_id"] = user["id"]
        session["full_name"] = user["full_name"]
        session["email"] = user["email"]
        session["role"] = user["role"]

        return redirect("/")

    except Exception as e:

        print(f"Google OAuth error: {e}")

        return redirect("/?google_error=google_login_failed")