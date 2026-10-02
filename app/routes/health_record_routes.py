import json
from flask import Blueprint, render_template, session, redirect

from app.services.health_record_service import (
    get_user_prediction_records,
    get_prediction_record_by_id,
    delete_prediction_record
)


health_record_bp = Blueprint(
    "health_record",
    __name__
)


@health_record_bp.route(
    "/my-health-records"
)
def my_health_records():

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to view your health records.", 401


    # -----------------------------------------------------
    # Get logged-in user's records
    # -----------------------------------------------------

    records = get_user_prediction_records(
        session["user_id"]
    )
    
    
    for record in records:
    
        try:
        
            record["prediction_result"] = json.loads(
                record["prediction_result"]
            ) if record["prediction_result"] else None
    
        except Exception:
        
            pass
        
        
    return render_template(
        "my_health_records.html",
        records=records
    )

@health_record_bp.route(
    "/my-health-records/<record_id>"
)
def health_record_details(record_id):

    # -----------------------------------------------------
    # Require login
    # -----------------------------------------------------

    if "user_id" not in session:

        return "Please sign in to view this health record.", 401


    # -----------------------------------------------------
    # Get record belonging to logged-in user
    # -----------------------------------------------------

    record = get_prediction_record_by_id(
        record_id,
        session["user_id"]
    )


    # -----------------------------------------------------
    # Record not found
    # -----------------------------------------------------

    if not record:

        return "Health record not found.", 404


    # -----------------------------------------------------
    # Convert stored JSON strings into Python dictionaries
    # -----------------------------------------------------

    try:

        record["input_data"] = json.loads(
            record["input_data"]
        ) if record["input_data"] else {}

    except Exception:

        record["input_data"] = {}

    try:

        record["prediction_result"] = json.loads(
            record["prediction_result"]
        ) if record["prediction_result"] else None
    
    except Exception:
    
        record["prediction_result"] = record["prediction_result"]


    try:

        record["result_details"] = json.loads(
            record["result_details"]
        ) if record["result_details"] else {}

    except Exception:

        record["result_details"] = {}


    return render_template(
        "health_record_details.html",
        record=record
    )

@health_record_bp.route(
    "/my-health-records/delete/<record_id>",
    methods=["POST"]
)
def delete_health_record(record_id):

    if "user_id" not in session:
        return "Please sign in to delete this health record.", 401

    deleted = delete_prediction_record(
        record_id,
        session["user_id"]
    )

    if not deleted:
        return "Health record not found or could not be deleted.", 404

    return redirect("/my-health-records")