from flask import Blueprint, render_template

from app.services.medicine_info_service import (
    get_medicine_information
)


medicine_info_bp = Blueprint(
    "medicine_info",
    __name__,
    url_prefix="/medicine-info"
)


@medicine_info_bp.route("/<medicine_name>")
def medicine_information(medicine_name):

    medicine_data = get_medicine_information(
        medicine_name
    )

    return render_template(
        "medicine/medicine_info.html",
        medicine=medicine_data
    )