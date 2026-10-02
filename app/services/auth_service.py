from werkzeug.security import generate_password_hash, check_password_hash
from app.database.connection import get_db_connection


def create_user(full_name, email, password):
    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed.", None

    cursor = connection.cursor()

    try:
        # Check whether email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return False, "An account with this email already exists.", None

        # Hash password before storing it
        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password_hash,
                auth_provider,
                email_verified,
                terms_accepted_at
            )
            VALUES (%s, %s, %s, 'local', FALSE, NOW())
            """,
            (
                full_name,
                email,
                password_hash
            )
        )

        connection.commit()
        user_id = cursor.lastrowid
        return True, "Account created successfully.", user_id

    except Exception as e:
        connection.rollback()
        print(f"Create user error: {e}")
        return False, "Unable to create account.", None

    finally:
        cursor.close()
        connection.close()


def authenticate_user(email, password):
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
                role,
                password_hash,
                auth_provider,
                profile_image,
                email_verified,
                is_active
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:
            return None

        if not user["is_active"]:
            return None

        # Google accounts don't have a local password
        if not user["password_hash"]:
            return None

        if not check_password_hash(
            user["password_hash"],
            password
        ):
            return None

        # Update last login time
        cursor.execute(
            """
            UPDATE users
            SET last_login_at = NOW()
            WHERE id = %s
            """,
            (user["id"],)
        )

        connection.commit()

        return user

    except Exception as e:
        connection.rollback()
        print(f"Authentication error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()


def get_or_create_google_user(
    google_id,
    full_name,
    email,
    profile_image=None
):
    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        # Check whether this Google email already exists
        cursor.execute(
            """
            SELECT
                id,
                full_name,
                email,
                password_hash,
                auth_provider,
                profile_image,
                email_verified,
                is_active
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        # Existing account
        if user:

            if not user["is_active"]:
                return None

            # Update Google account information
            cursor.execute(
                """
                UPDATE users
                SET
                    full_name = %s,
                    profile_image = %s,
                    auth_provider = 'google',
                    email_verified = TRUE,
                    last_login_at = NOW()
                WHERE id = %s
                """,
                (
                    full_name,
                    profile_image,
                    user["id"]
                )
            )

            connection.commit()

            cursor.execute(
                """
                SELECT
                    id,
                    full_name,
                    email,
                    password_hash,
                    auth_provider,
                    profile_image,
                    email_verified,
                    is_active
                FROM users
                WHERE id = %s
                """,
                (user["id"],)
            )

            return cursor.fetchone()

        # New Google account
        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password_hash,
                auth_provider,
                profile_image,
                email_verified,
                terms_accepted_at,
                last_login_at
            )
            VALUES
            (
                %s,
                %s,
                NULL,
                'google',
                %s,
                TRUE,
                NOW(),
                NOW()
            )
            """,
            (
                full_name,
                email,
                profile_image
            )
        )

        connection.commit()

        new_user_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT
                id,
                full_name,
                email,
                password_hash,
                auth_provider,
                profile_image,
                email_verified,
                is_active
            FROM users
            WHERE id = %s
            """,
            (new_user_id,)
        )

        return cursor.fetchone()

    except Exception as e:
        connection.rollback()
        print(f"Google authentication error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def create_doctor(
    full_name,
    email,
    password,
    registration_number,
    qualification,
    specialization,
    experience_years,
    bio,
    clinic_name,
    clinic_address,
    city,
    consultation_fee,
    consultation_type
):
    connection = get_db_connection()

    if not connection:
        return False, "Database connection failed."

    cursor = connection.cursor()

    try:
        # Check whether email already exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return False, "An account with this email already exists."

        # Check whether medical registration number already exists
        cursor.execute(
            """
            SELECT id
            FROM doctors
            WHERE registration_number = %s
            """,
            (registration_number,)
        )

        existing_registration = cursor.fetchone()

        if existing_registration:
            return False, "This medical registration number is already registered."

        # Hash password
        password_hash = generate_password_hash(password)

        # Create doctor account in users table
        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                password_hash,
                auth_provider,
                role,
                email_verified,
                terms_accepted_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                'local',
                'doctor',
                FALSE,
                NOW()
            )
            """,
            (
                full_name,
                email,
                password_hash
            )
        )

        user_id = cursor.lastrowid

        # Create doctor professional profile
        cursor.execute(
            """
            INSERT INTO doctors
            (
                user_id,
                registration_number,
                qualification,
                specialization,
                experience_years,
                bio,
                clinic_name,
                clinic_address,
                city,
                consultation_fee,
                consultation_types,
                verification_status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'Pending'
            )
            """,
            (
                user_id,
                registration_number,
                qualification,
                specialization,
                experience_years,
                bio,
                clinic_name,
                clinic_address,
                city,
                consultation_fee,
                consultation_type
            )
        )

        connection.commit()

        return (
            True,
            "Doctor registration submitted successfully.",
            user_id
        )

    except Exception as e:
        connection.rollback()
        print(f"Doctor registration error: {e}")
        return False, "Unable to create doctor account."

    finally:
        cursor.close()
        connection.close()