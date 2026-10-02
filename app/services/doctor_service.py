DOCTORS = [
    {
        "id": "DOC001",
        "name": "Dr. Rahul Sharma",
        "specialty": "Cardiology",
        "qualification": "MBBS, MD Cardiology",
        "experience": "10+ Years",
        "clinic": "City Heart Clinic",
        "location": "Dehradun",
        "rating": 4.8,
        "consultation": ["In-person", "Online"],
        "image": "doctor-male.svg"
    },
    {
        "id": "DOC002",
        "name": "Dr. Ananya Verma",
        "specialty": "Cardiology",
        "qualification": "MBBS, MD",
        "experience": "8+ Years",
        "clinic": "OpenHealth Medical Center",
        "location": "Dehradun",
        "rating": 4.7,
        "consultation": ["In-person", "Online"],
        "image": "doctor-female.svg"
    },
    {
        "id": "DOC003",
        "name": "Dr. Arjun Mehta",
        "specialty": "Neurology",
        "qualification": "MBBS, DM Neurology",
        "experience": "12+ Years",
        "clinic": "NeuroCare Clinic",
        "location": "Dehradun",
        "rating": 4.9,
        "consultation": ["In-person", "Online"],
        "image": "doctor-male.svg"
    },
    {
        "id": "DOC004",
        "name": "Dr. Priya Kapoor",
        "specialty": "Neurology",
        "qualification": "MBBS, MD, DM",
        "experience": "9+ Years",
        "clinic": "Brain & Nerve Center",
        "location": "Dehradun",
        "rating": 4.8,
        "consultation": ["In-person"],
        "image": "doctor-female.svg"
    },
    {
        "id": "DOC005",
        "name": "Dr. Vikram Joshi",
        "specialty": "Orthopedics",
        "qualification": "MBBS, MS Orthopedics",
        "experience": "11+ Years",
        "clinic": "OrthoCare Hospital",
        "location": "Dehradun",
        "rating": 4.7,
        "consultation": ["In-person"],
        "image": "doctor-male.svg"
    },
    {
        "id": "DOC006",
        "name": "Dr. Neha Singh",
        "specialty": "Dermatology",
        "qualification": "MBBS, MD Dermatology",
        "experience": "7+ Years",
        "clinic": "SkinCare Clinic",
        "location": "Dehradun",
        "rating": 4.8,
        "consultation": ["In-person", "Online"],
        "image": "doctor-female.svg"
    },
    {
        "id": "DOC007",
        "name": "Dr. Amit Rawat",
        "specialty": "General Medicine",
        "qualification": "MBBS, MD Medicine",
        "experience": "13+ Years",
        "clinic": "OpenHealth Medical Center",
        "location": "Dehradun",
        "rating": 4.9,
        "consultation": ["In-person", "Online"],
        "image": "doctor-male.svg"
    },
    {
        "id": "DOC008",
        "name": "Dr. Sneha Gupta",
        "specialty": "Gynecology",
        "qualification": "MBBS, MD Gynecology",
        "experience": "9+ Years",
        "clinic": "Women's Health Center",
        "location": "Dehradun",
        "rating": 4.8,
        "consultation": ["In-person", "Online"],
        "image": "doctor-female.svg"
    },
    {
        "id": "DOC009",
        "availability_id": "AHT 0001",
        "name": "Dr. Riya Malhotra",
        "specialty": "Pediatrics",
        "qualification": "MBBS, MD Pediatrics",
        "experience": "8+ Years",
        "clinic": "Little Hearts Children's Clinic",
        "location": "Dehradun",
        "rating": 4.8,
        "consultation": ["In-person", "Online"],
        "image": "doctor-female.svg"
    },

    {
        "id": "DOC010",
        "name": "Dr. Karan Negi",
        "specialty": "ENT",
        "qualification": "MBBS, MS ENT",
        "experience": "10+ Years",
        "clinic": "ENT Care Center",
        "location": "Dehradun",
        "rating": 4.7,
        "consultation": ["In-person", "Online"],
        "image": "doctor-male.svg"
    },
]


def get_all_doctors():
    return DOCTORS


def get_doctors_by_specialty(specialty):

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE d.specialization = %s
              AND u.role = 'doctor'
            ORDER BY d.id
            """,
            (specialty,)
        )

        doctors = cursor.fetchall()

        for doctor in doctors:

            doctor["experience"] = (
                f'{doctor["experience_years"]} Years'
            )

            doctor["consultation"] = parse_consultation_types(
                doctor["consultation_types"]
            )

        return doctors

    except Exception as e:

        print(
            f"Get doctors by specialty error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()


def get_doctor_by_id(doctor_id):

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE
                (d.id = %s OR d.registration_number = %s)
                AND u.role = 'doctor'
            """,
            (doctor_id, doctor_id)
        )

        doctor = cursor.fetchone()

        if not doctor:
            return None

        doctor["experience"] = (
            f'{doctor["experience_years"]} Years'
        )

        doctor["consultation"] = parse_consultation_types(
            doctor["consultation_types"]
        )

        return doctor

    except Exception as e:

        print(
            f"Get doctor by ID error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()



def search_doctors(search_term):

    search_term = search_term.strip()

    if not search_term:
        return []

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        search_pattern = f"%{search_term}%"

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE u.role = 'doctor'
              AND (
                    u.full_name LIKE %s
                    OR d.specialization LIKE %s
                    OR d.qualification LIKE %s
                    OR d.clinic_name LIKE %s
                    OR d.city LIKE %s
                  )
            ORDER BY d.id
            """,
            (
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern
            )
        )

        doctors = cursor.fetchall()

        for doctor in doctors:

            doctor["experience"] = (
                f'{doctor["experience_years"]} Years'
            )

            doctor["consultation"] = parse_consultation_types(
                doctor["consultation_types"]
            )

        return doctors

    except Exception as e:

        print(
            f"Search doctors error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()


from app.database.connection import get_db_connection

def parse_consultation_types(consultation_types):
    if not consultation_types:
        return []

    consultation_types = consultation_types.strip()

    if consultation_types.lower() == "both":
        return ["In-person", "Online"]

    return [
        item.strip()
        for item in consultation_types.split(",")
        if item.strip()
    ]

def get_doctor_by_user_id(user_id):

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE d.user_id = %s
            """,
            (user_id,)
        )

        doctor = cursor.fetchone()

        if not doctor:
            return None

        doctor["experience"] = (
            f'{doctor["experience_years"]} Years'
        )

        doctor["consultation"] = parse_consultation_types(
            doctor["consultation_types"]
        )

        return doctor

    except Exception as e:

        print(
            f"Get doctor by user ID error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()


def get_all_doctors_from_db():

    connection = get_db_connection()

    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE u.role = 'doctor'
            ORDER BY d.id
            """
        )

        doctors = cursor.fetchall()

        for doctor in doctors:

            doctor["experience"] = (
                f'{doctor["experience_years"]} Years'
            )

            doctor["consultation"] = parse_consultation_types(
                doctor["consultation_types"]
            )

        return doctors

    except Exception as e:

        print(
            f"Get all doctors from database error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()

def get_doctor_from_db_by_id(doctor_id):

    connection = get_db_connection()

    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                d.id,
                d.user_id,
                d.registration_number,
                u.full_name AS name,
                u.email,
                d.specialization AS specialty,
                d.qualification,
                d.experience_years,
                d.clinic_name AS clinic,
                d.city AS location,
                d.consultation_types,
                d.verification_status
            FROM doctors d
            JOIN users u
                ON d.user_id = u.id
            WHERE d.id = %s
              AND u.role = 'doctor'
            """,
            (doctor_id,)
        )

        doctor = cursor.fetchone()

        if not doctor:
            return None

        doctor["experience"] = (
            f'{doctor["experience_years"]} Years'
        )

        doctor["consultation"] = []

        doctor["consultation"] = parse_consultation_types(
            doctor["consultation_types"]
        )

        return doctor

    except Exception as e:

        print(
            f"Get doctor from database by ID error: {e}"
        )

        return None

    finally:

        cursor.close()
        connection.close()