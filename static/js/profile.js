document.addEventListener("DOMContentLoaded", () => {

    const profileModal =
        document.getElementById("profileModal");

    const editProfileBtn =
        document.getElementById("editProfileBtn");

    const closeProfileModal =
        document.getElementById("closeProfileModal");

    const cancelProfileEdit =
        document.getElementById("cancelProfileEdit");

    const profileImageInput =
        document.getElementById("profileImage");

    const profilePicturePreview =
        document.getElementById("profilePicturePreview");

    const profilePicturePlaceholder =
        document.getElementById(
            "profilePicturePlaceholder"
        );


    if (!profileModal || !editProfileBtn) {
        return;
    }


    // =====================================================
    // OPEN MODAL
    // =====================================================

    editProfileBtn.addEventListener(
        "click",
        () => {

            profileModal.classList.add(
                "active"
            );

            document.body.classList.add(
                "profile-modal-open"
            );

        }
    );


    // =====================================================
    // PROFILE PICTURE PREVIEW
    // =====================================================

    if (profileImageInput) {

        profileImageInput.addEventListener(
            "change",
            (event) => {

                const file =
                    event.target.files[0];

                if (!file) {
                    return;
                }


                // Check file type

                if (
                    ![
                        "image/jpeg",
                        "image/jpg",
                        "image/png"
                    ].includes(file.type)
                ) {

                    alert(
                        "Please select a JPG or PNG image."
                    );

                    profileImageInput.value = "";

                    return;
                }


                // Check file size

                const maxSize =
                    2 * 1024 * 1024;

                if (file.size > maxSize) {

                    alert(
                        "Profile picture must be smaller than 2 MB."
                    );

                    profileImageInput.value = "";

                    return;
                }


                // Create temporary preview

                const reader =
                    new FileReader();

                reader.onload = (e) => {

                    if (profilePicturePreview) {

                        profilePicturePreview.src =
                            e.target.result;

                        profilePicturePreview.style.display =
                            "block";

                    }


                    if (profilePicturePlaceholder) {

                        profilePicturePlaceholder.style.display =
                            "none";

                    }

                };

                reader.readAsDataURL(file);

            }
        );

    }

    // =====================================================
    // CLOSE MODAL
    // =====================================================

    function closeModal() {

        profileModal.classList.remove(
            "active"
        );

        document.body.classList.remove(
            "profile-modal-open"
        );

    }


    if (closeProfileModal) {

        closeProfileModal.addEventListener(
            "click",
            closeModal
        );

    }


    if (cancelProfileEdit) {

        cancelProfileEdit.addEventListener(
            "click",
            closeModal
        );

    }


    // =====================================================
    // CLOSE WHEN CLICKING OUTSIDE
    // =====================================================

    profileModal.addEventListener(
        "click",
        (event) => {

            if (
                event.target ===
                profileModal
            ) {

                closeModal();

            }

        }
    );


    // =====================================================
    // CLOSE WITH ESCAPE
    // =====================================================

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape" &&
                profileModal.classList.contains("active")
            ) {

                closeModal();

            }

        }
    );

});

const removeProfilePictureBtn =
    document.getElementById("removeProfilePictureBtn");

if (removeProfilePictureBtn) {
    removeProfilePictureBtn.addEventListener(
        "click",
        async () => {

            const confirmed = confirm(
                "Are you sure you want to remove your profile picture?"
            );

            if (!confirmed) {
                return;
            }

            try {
                const response = await fetch(
                    "/profile/remove-picture",
                    {
                        method: "POST"
                    }
                );

                if (response.ok) {
                    window.location.reload();
                } else {
                    alert(
                        "Unable to remove profile picture. Please try again."
                    );
                }

            } catch (error) {
                console.error(
                    "Remove profile picture error:",
                    error
                );

                alert(
                    "Something went wrong. Please try again."
                );
            }
        }
    );
}