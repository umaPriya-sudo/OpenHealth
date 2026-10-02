import os

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    current_app
)

from werkzeug.utils import secure_filename

from app.services.profile_service import (
    get_user_profile,
    get_user_activity,
    update_user_profile
)


profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    user = get_user_profile(user_id)

    if not user:
        return redirect("/")

    activities = get_user_activity(user_id)

    return render_template(
        "profile.html",
        user=user,
        activities=activities
    )

@profile_bp.route(
    "/profile/update",
    methods=["POST"]
)
def update_profile():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    full_name = request.form.get(
        "full_name",
        ""
    ).strip()

    if not full_name:
        return redirect("/profile")


    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    profile_image = request.files.get(
        "profile_image"
    )

    profile_image_path = None


    if profile_image and profile_image.filename:

        allowed_extensions = {
            "png",
            "jpg",
            "jpeg"
        }

        original_filename = secure_filename(
            profile_image.filename
        )

        extension = (
            original_filename
            .rsplit(".", 1)[-1]
            .lower()
            if "." in original_filename
            else ""
        )


        if extension not in allowed_extensions:
            return redirect("/profile")


        # Create profile upload directory

        profile_folder = os.path.join(
            current_app.static_folder,
            "uploads",
            "profiles"
        )

        os.makedirs(
            profile_folder,
            exist_ok=True
        )


        # Use user ID to avoid filename conflicts

        filename = (
            f"user_{user_id}.{extension}"
        )

        file_path = os.path.join(
            profile_folder,
            filename
        )


        profile_image.save(
            file_path
        )


        profile_image_path = (
            f"/static/uploads/profiles/{filename}"
        )


    # =====================================================
    # UPDATE DATABASE
    # =====================================================

    updated = update_user_profile(
        user_id=user_id,
        full_name=full_name,
        profile_image=profile_image_path
    )


    if updated:

        session["full_name"] = full_name


    return redirect("/profile")

@profile_bp.route("/profile/remove-picture", methods=["POST"])
def remove_profile_picture():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    user = get_user_profile(user_id)

    if not user:
        return redirect("/profile")

    profile_image = user.get("profile_image")

    # Delete the image file from the server
    if profile_image:
        image_path = os.path.join(
            current_app.root_path,
            profile_image.lstrip("/")
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    # Remove image path from database
    updated = update_user_profile(
        user_id=user_id,
        full_name=user["full_name"],
        profile_image=""
    )

    return redirect("/profile")