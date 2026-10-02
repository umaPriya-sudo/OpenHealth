document.addEventListener("DOMContentLoaded", () => {

    const dateInput = document.getElementById(
        "appointment_date"
    );

    if (dateInput) {

        // Prevent selecting a past date
        const today = new Date();

        const year = today.getFullYear();

        const month = String(
            today.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            today.getDate()
        ).padStart(2, "0");

        const todayString =
            `${year}-${month}-${day}`;

        dateInput.min = todayString;
    }

});


/* =========================================================
   Open Reschedule Form
   ========================================================= */

function openRescheduleForm() {

    const form =
        document.getElementById(
            "rescheduleForm"
        );

    if (!form) {
        return;
    }

    form.style.display = "block";

    form.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}


/* =========================================================
   Close Reschedule Form
   ========================================================= */

function closeRescheduleForm() {

    const form =
        document.getElementById(
            "rescheduleForm"
        );

    if (!form) {
        return;
    }

    form.style.display = "none";

}