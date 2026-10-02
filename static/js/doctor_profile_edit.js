document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("doctorProfileForm");

    const messageBox =
        document.getElementById("profileMessage");

    const saveButton =
        document.getElementById("saveProfileBtn");


    function showMessage(message, type = "success") {

        messageBox.textContent = message;

        messageBox.className =
            `profile-message ${type}`;

        messageBox.style.display = "block";

        setTimeout(() => {
            messageBox.style.display = "none";
        }, 3500);
    }


    form.addEventListener("submit", async (event) => {

        event.preventDefault();


        const qualification =
            document.getElementById("qualification").value.trim();

        const specialization =
            document.getElementById("specialization").value.trim();

        const experienceYears =
            document.getElementById("experienceYears").value;

        const bio =
            document.getElementById("bio").value.trim();

        const clinicName =
            document.getElementById("clinicName").value.trim();

        const clinicAddress =
            document.getElementById("clinicAddress").value.trim();

        const city =
            document.getElementById("city").value.trim();

        const consultationFee =
            document.getElementById("consultationFee").value;

        const consultationTypes =
            document.getElementById("consultationTypes").value;


        if (!qualification) {

            showMessage(
                "Qualification is required.",
                "error"
            );

            return;
        }


        if (!specialization) {

            showMessage(
                "Specialization is required.",
                "error"
            );

            return;
        }


        saveButton.disabled = true;

        saveButton.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            Saving...
        `;


        try {

            const response = await fetch(
                "/doctor/profile/api",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({

                        qualification:
                            qualification,

                        specialization:
                            specialization,

                        experience_years:
                            experienceYears,

                        bio:
                            bio,

                        clinic_name:
                            clinicName,

                        clinic_address:
                            clinicAddress,

                        city:
                            city,

                        consultation_fee:
                            consultationFee,

                        consultation_types:
                            consultationTypes

                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Unable to update profile."
                );
            }


            showMessage(
                "Professional profile updated successfully.",
                "success"
            );
            
            setTimeout(() => {
                window.location.href = "/doctor/dashboard";
            }, 800);


        } catch (error) {

            console.error(
                "Profile update error:",
                error
            );


            showMessage(
                error.message ||
                "Unable to update profile.",
                "error"
            );


        } finally {

            saveButton.disabled = false;

            saveButton.innerHTML = `
                <i class="fas fa-save"></i>
                Save Changes
            `;
        }

    });

});