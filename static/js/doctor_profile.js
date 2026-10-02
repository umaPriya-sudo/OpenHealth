document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       DATE SELECTION
       ===================================================== */

    const dateCards = document.querySelectorAll(".date-card");

    dateCards.forEach(card => {

        card.addEventListener("click", () => {

            dateCards.forEach(item => {
                item.classList.remove("active");
            });

            card.classList.add("active");
        });

    });


    /* =====================================================
       TIME SLOT SELECTION
       ===================================================== */

    const timeSlots = document.querySelectorAll(".time-slot");

    timeSlots.forEach(slot => {

        slot.addEventListener("click", () => {

            timeSlots.forEach(item => {
                item.classList.remove("active");
            });

            slot.classList.add("active");
        });

    });


    /* =====================================================
       CONSULTATION TYPE
       ===================================================== */

    const consultationChoices =
        document.querySelectorAll(".consultation-choice");

    consultationChoices.forEach(choice => {

        choice.addEventListener("click", () => {

            consultationChoices.forEach(item => {
                item.classList.remove("active");
            });

            choice.classList.add("active");

            const radio =
                choice.querySelector('input[type="radio"]');

            if (radio) {
                radio.checked = true;
            }

        });

    });


    /* =====================================================
   CONTINUE TO APPOINTMENT DETAILS
   ===================================================== */

    /* =====================================================
   CONTINUE BUTTON
   ===================================================== */

const continueButton =
    document.getElementById("continueBookingBtn");

if (continueButton) {

    continueButton.addEventListener("click", () => {

        const selectedDate =
            document.querySelector(".date-card.active");

        const selectedTime =
            document.querySelector(".time-slot.active");

        const selectedConsultation =
            document.querySelector(
                '.consultation-choice input[type="radio"]:checked'
            );


        if (!selectedDate) {
            alert("Please select an appointment date.");
            return;
        }


        if (!selectedTime) {
            alert("Please select an appointment time.");
            return;
        }


        if (!selectedConsultation) {
            alert("Please select a consultation type.");
            return;
        }


        const date =
            selectedDate.dataset.date;

        const time =
            selectedTime.dataset.time;

        const consultation =
            selectedConsultation.value;

        const doctorId =
            continueButton.dataset.doctorId;


        const form =
            document.createElement("form");

        form.method = "POST";
        form.action =
            "/doctor-appointment/details";


        const doctorInput =
            document.createElement("input");

        doctorInput.type = "hidden";
        doctorInput.name = "doctor_id";
        doctorInput.value = doctorId;


        const dateInput =
            document.createElement("input");

        dateInput.type = "hidden";
        dateInput.name = "appointment_date";
        dateInput.value = date;


        const timeInput =
            document.createElement("input");

        timeInput.type = "hidden";
        timeInput.name = "appointment_time";
        timeInput.value = time;


        const consultationInput =
            document.createElement("input");

        consultationInput.type = "hidden";
        consultationInput.name = "consultation_type";
        consultationInput.value = consultation;


        form.appendChild(doctorInput);
        form.appendChild(dateInput);
        form.appendChild(timeInput);
        form.appendChild(consultationInput);


        document.body.appendChild(form);

        form.submit();

    });

}

});