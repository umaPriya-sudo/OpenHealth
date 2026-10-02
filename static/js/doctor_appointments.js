document.addEventListener("DOMContentLoaded", () => {

    const appointmentsList =
        document.getElementById("appointmentsList");

    const appointmentsLoading =
        document.getElementById("appointmentsLoading");

    const appointmentsEmpty =
        document.getElementById("appointmentsEmpty");

    const appointmentCount =
        document.getElementById("appointmentCount");

    const appointmentSearch =
        document.getElementById("appointmentSearch");

    const statusFilter =
        document.getElementById("statusFilter");


    let appointments = [];


    // =====================================================
    // LOAD APPOINTMENTS
    // =====================================================

    async function loadAppointments() {

        try {

            const response = await fetch("/doctor/appointments");

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Unable to load appointments."
                );
            }

            appointments = data.appointments || [];

            renderAppointments();

        } catch (error) {

            console.error(
                "Appointment loading error:",
                error
            );

            appointmentsLoading.style.display = "none";
            appointmentsList.style.display = "none";
            appointmentsEmpty.style.display = "flex";

            appointmentsEmpty.querySelector("h3").textContent =
                "Unable to load appointments";

            appointmentsEmpty.querySelector("p").textContent =
                error.message;

        }
    }


    // =====================================================
    // RENDER APPOINTMENTS
    // =====================================================

    function renderAppointments() {

        const searchText =
            appointmentSearch.value
                .trim()
                .toLowerCase();

        const selectedStatus =
            statusFilter.value;


        const filteredAppointments =
            appointments.filter(appointment => {

                const patientName =
                    (appointment.patient_name || "")
                        .toLowerCase();

                const patientEmail =
                    (appointment.patient_email || "")
                        .toLowerCase();

                const appointmentId =
                    String(
                        appointment.appointment_id || ""
                    ).toLowerCase();

                const matchesSearch =
                    !searchText ||
                    patientName.includes(searchText) ||
                    patientEmail.includes(searchText) ||
                    appointmentId.includes(searchText);

                const matchesStatus =
                    selectedStatus === "all" ||
                    appointment.status === selectedStatus;

                return matchesSearch && matchesStatus;
            });


        appointmentCount.textContent =
            filteredAppointments.length;


        appointmentsLoading.style.display = "none";


        if (filteredAppointments.length === 0) {

            appointmentsList.style.display = "none";
            appointmentsEmpty.style.display = "flex";

            appointmentsEmpty.querySelector("h3").textContent =
                appointments.length === 0
                    ? "No appointments yet"
                    : "No appointments found";

            appointmentsEmpty.querySelector("p").textContent =
                appointments.length === 0
                    ? "Your scheduled patient appointments will appear here."
                    : "Try changing the search or status filter.";

            return;
        }


        appointmentsEmpty.style.display = "none";
        appointmentsList.style.display = "block";


        appointmentsList.innerHTML =
            filteredAppointments
                .map(createAppointmentCard)
                .join("");
    }


    // =====================================================
    // CREATE APPOINTMENT CARD
    // =====================================================

    function createAppointmentCard(appointment) {

        const status =
            appointment.status || "Confirmed";

        const statusClass =
            status.toLowerCase();


        const patientName =
            escapeHtml(
                appointment.patient_name || "Unknown Patient"
            );

        const patientEmail =
            escapeHtml(
                appointment.patient_email || "No email available"
            );

        const consultationType =
            escapeHtml(
                appointment.consultation_type || "Not specified"
            );

        const reason =
            escapeHtml(
                appointment.reason || "No reason provided"
            );

        const appointmentDate =
            formatDate(
                appointment.appointment_date
            );

        const appointmentTime =
            formatTime(
                appointment.appointment_time
            );


        return `
            <article class="appointment-item">

                <div class="appointment-main">

                    <div class="patient-avatar">
                        <i class="fas fa-user"></i>
                    </div>


                    <div class="patient-details">

                        <div class="patient-title-row">

                            <h3>
                                ${patientName}
                            </h3>

                            <span class="status-badge status-${statusClass}">
                                ${escapeHtml(status)}
                            </span>

                        </div>


                        <p class="patient-email">
                            <i class="fas fa-envelope"></i>
                            ${patientEmail}
                        </p>


                        <div class="appointment-meta">

                            <span>
                                <i class="fas fa-calendar"></i>
                                ${appointmentDate}
                            </span>

                            <span>
                                <i class="fas fa-clock"></i>
                                ${appointmentTime}
                            </span>

                            <span>
                                <i class="fas fa-video"></i>
                                ${consultationType}
                            </span>

                        </div>


                        <div class="appointment-reason">

                            <strong>
                                Reason:
                            </strong>

                            <span>
                                ${reason}
                            </span>

                        </div>

                    </div>

                </div>


                <div class="appointment-actions">

                    ${getActionButtons(appointment)}

                </div>

            </article>
        `;
    }


    // =====================================================
    // ACTION BUTTONS
    // =====================================================

    function getActionButtons(appointment) {

    const status =
        appointment.status || "Confirmed";

    // Completed or rejected appointments
    // should not have any action buttons.
    if (
        status === "Completed" ||
        status === "Rejected"
    ) {
        return "";
    }

    let buttons = "";

    if (status !== "Confirmed") {

        buttons += `
            <button
                class="appointment-action-btn confirm-btn"
                data-id="${appointment.id}"
                data-status="Confirmed">
                <i class="fas fa-check"></i>
                Confirm
            </button>
        `;
    }

    if (status !== "Rejected") {

        buttons += `
            <button
                class="appointment-action-btn reject-btn"
                data-id="${appointment.id}"
                data-status="Rejected">
                <i class="fas fa-xmark"></i>
                Reject
            </button>
        `;
    }

    if (status === "Confirmed") {

        buttons += `
            <button
                class="appointment-action-btn complete-btn"
                data-id="${appointment.id}"
                data-status="Completed">
                <i class="fas fa-check-double"></i>
                Complete
            </button>
        `;
    }

    return buttons;
}


    // =====================================================
    // UPDATE APPOINTMENT STATUS
    // =====================================================

    async function updateAppointmentStatus(
        appointmentId,
        newStatus
    ) {

        const confirmation =
            window.confirm(
                `Are you sure you want to mark this appointment as ${newStatus}?`
            );


        if (!confirmation) {
            return;
        }


        try {

            const response = await fetch(
                `/doctor/appointments/${appointmentId}/status`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        status: newStatus
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Unable to update appointment."
                );
            }


            const appointment =
                appointments.find(
                    item =>
                        String(item.id) ===
                        String(appointmentId)
                );


            if (appointment) {
                appointment.status = newStatus;
            }


            renderAppointments();


        } catch (error) {

            console.error(
                "Appointment update error:",
                error
            );

            alert(error.message);
        }
    }


    // =====================================================
    // BUTTON CLICK HANDLER
    // =====================================================

    appointmentsList.addEventListener(
        "click",
        event => {

            const button =
                event.target.closest(
                    ".appointment-action-btn"
                );


            if (!button) {
                return;
            }


            const appointmentId =
                button.dataset.id;

            const newStatus =
                button.dataset.status;


            updateAppointmentStatus(
                appointmentId,
                newStatus
            );
        }
    );


    // =====================================================
    // SEARCH + FILTER
    // =====================================================

    appointmentSearch.addEventListener(
        "input",
        renderAppointments
    );


    statusFilter.addEventListener(
        "change",
        renderAppointments
    );


    // =====================================================
    // FORMAT DATE
    // =====================================================

    function formatDate(dateValue) {

        if (!dateValue) {
            return "Date not available";
        }


        const date =
            new Date(dateValue);


        if (Number.isNaN(date.getTime())) {
            return dateValue;
        }


        return date.toLocaleDateString(
            "en-IN",
            {
                day: "2-digit",
                month: "short",
                year: "numeric"
            }
        );
    }


    // =====================================================
    // FORMAT TIME
    // =====================================================

    function formatTime(timeValue) {

    if (!timeValue) {
        return "Time not available";
    }

    const value = String(timeValue).trim();

    // Database already contains values such as:
    // "10:30 AM" or "02:30 PM"
    if (
        value.toUpperCase().includes("AM") ||
        value.toUpperCase().includes("PM")
    ) {
        return value;
    }

    const parts = value.split(":");

    if (parts.length < 2) {
        return value;
    }

    let hours = parseInt(parts[0], 10);

    const minutes = parts[1];

    const period =
        hours >= 12
            ? "PM"
            : "AM";

    hours =
        hours % 12 || 12;

    return `${hours}:${minutes} ${period}`;
}


    // =====================================================
    // BASIC HTML ESCAPE
    // =====================================================

    function escapeHtml(value) {

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    // =====================================================
    // INITIAL LOAD
    // =====================================================

    loadAppointments();

});