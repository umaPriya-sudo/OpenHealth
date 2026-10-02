document.addEventListener("DOMContentLoaded", () => {

    const continueButton =
        document.getElementById("continueDetailsBtn");

    if (!continueButton) {
        return;
    }

    let pendingAppointmentForm = null;


    // =========================================================
    // CREATE APPOINTMENT FORM
    // =========================================================

    function createAppointmentForm() {

        const reasonField =
            document.getElementById("reasonForVisit");

        const reason =
            reasonField
                ? reasonField.value.trim()
                : "";


        const appointmentDate =
            document.querySelector(
                ".appointment-summary-item:nth-child(1) strong"
            );

        const appointmentTime =
            document.querySelector(
                ".appointment-summary-item:nth-child(2) strong"
            );

        const consultationType =
            document.querySelector(
                ".appointment-summary-item:nth-child(3) strong"
            );


        if (
            !appointmentDate ||
            !appointmentTime ||
            !consultationType
        ) {

            alert("Unable to read appointment details.");

            return null;
        }


        const date =
            appointmentDate.textContent.trim();

        const time =
            appointmentTime.textContent.trim();

        const consultation =
            consultationType.textContent.trim();


        const doctorCard =
            document.querySelector(
                ".doctor-summary-card"
            );

        const doctorId =
            doctorCard
                ? doctorCard.dataset.doctorId
                : "";


        const form =
            document.createElement("form");

        form.method = "POST";

        form.action =
            "/doctor-appointment/confirmation";


        const fields = {
            doctor_id: doctorId,
            appointment_date: date,
            appointment_time: time,
            consultation_type: consultation,
            reason: reason
        };


        Object.entries(fields).forEach(
            ([name, value]) => {

                const input =
                    document.createElement("input");

                input.type = "hidden";
                input.name = name;
                input.value = value;

                form.appendChild(input);
            }
        );


        return form;
    }


    // =========================================================
    // CONTINUE BUTTON
    // =========================================================

    continueButton.addEventListener("click", async () => {

        const form = createAppointmentForm();

        if (!form) {
            return;
        }


        try {

            const response = await fetch(
                "/api/auth/status",
                {
                    method: "GET",
                    credentials: "same-origin"
                }
            );


            const data = await response.json();


            // =================================================
            // LOGGED IN
            // =================================================

            if (data.authenticated) {

                document.body.appendChild(form);

                form.submit();

                return;
            }


            // =================================================
            // LOGGED OUT
            // =================================================

            pendingAppointmentForm = form;

            if (typeof openAuthModal === "function") {

                openAuthModal("signin");

            } else {

                console.error(
                    "openAuthModal is not available."
                );

                alert(
                    "Sign in form could not be opened."
                );
            }


        } catch (error) {

            console.error(
                "Authentication check failed:",
                error
            );

            if (typeof openAuthModal === "function") {
                openAuthModal("signin");
            }

        }

    });


    // =========================================================
    // AFTER SUCCESSFUL LOGIN
    // =========================================================

    window.addEventListener(
        "openhealth:login",
        () => {

            if (!pendingAppointmentForm) {
                return;
            }


            document.body.appendChild(
                pendingAppointmentForm
            );

            pendingAppointmentForm.submit();

            pendingAppointmentForm = null;

        }
    );

});