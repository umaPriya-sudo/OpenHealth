document.addEventListener("DOMContentLoaded", () => {

    const confirmButton =
        document.getElementById("confirmAppointmentBtn");

    const backButton =
        document.getElementById("confirmationBackBtn");


    /* =====================================================
       BACK BUTTON
       ===================================================== */

    if (backButton) {

        backButton.addEventListener("click", () => {

            history.back();

        });

    }


    /* =====================================================
       CONFIRM APPOINTMENT
       ===================================================== */

    if (confirmButton) {

        confirmButton.addEventListener("click", () => {

            const confirmed =
                confirm(
                    "Are you sure you want to confirm this appointment?"
                );


            if (!confirmed) {
                return;
            }


            /*
             * Temporary confirmation.
             *
             * Database booking will be added
             * in the next step.
             */

            window.location.href =
                "/doctor-appointment/success";

        });

    }

});