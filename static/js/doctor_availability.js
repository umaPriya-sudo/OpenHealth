document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("availabilityForm");
    const dayInput = document.getElementById("dayOfWeek");
    const startTimeInput = document.getElementById("startTime");
    const endTimeInput = document.getElementById("endTime");
    const consultationTypeInput = document.getElementById("consultationType");

    const messageBox = document.getElementById("availabilityMessage");
    const loadingState = document.getElementById("availabilityLoading");
    const emptyState = document.getElementById("availabilityEmpty");
    const listContainer = document.getElementById("availabilityList");

    function showMessage(message, type = "success") {
        messageBox.textContent = message;
        messageBox.className = `availability-message ${type}`;
        messageBox.style.display = "block";

        setTimeout(() => {
            messageBox.style.display = "none";
        }, 3000);
    }

    function formatTime(time) {
        if (!time) return "";

        // If already formatted like 10:30 AM
        if (/[AP]M/i.test(time)) {
            return time;
        }

        return time;
    }

    function renderAvailability(availability) {
    listContainer.innerHTML = "";

    const countElement = document.getElementById("availabilityCount");

    const totalSlots = availability ? availability.length : 0;

    if (countElement) {
        countElement.textContent = totalSlots;
    }

    if (!availability || availability.length === 0) {
        emptyState.style.display = "block";
        listContainer.style.display = "none";
        return;
    }

    emptyState.style.display = "none";
    listContainer.style.display = "block";

    availability.forEach(item => {
        const card = document.createElement("div");

        card.className = "availability-item";

        card.innerHTML = `
            <div class="availability-info">

                <div class="availability-day">
                    <i class="fas fa-calendar-day"></i>
                    <strong>${escapeHtml(item.day_of_week)}</strong>
                </div>

                <div class="availability-time">
                    <i class="fas fa-clock"></i>
                    ${escapeHtml(formatTime(item.start_time))}
                    -
                    ${escapeHtml(formatTime(item.end_time))}
                </div>

                <div class="availability-type">
                    <i class="fas fa-stethoscope"></i>
                    ${escapeHtml(item.consultation_type)}
                </div>

            </div>

            <button
                type="button"
                class="delete-availability-btn"
                data-id="${item.id}"
            >
                <i class="fas fa-trash"></i>
            </button>
        `;

        listContainer.appendChild(card);
    });

    document.querySelectorAll(".delete-availability-btn").forEach(button => {
        button.addEventListener("click", () => {
            deleteAvailability(button.dataset.id);
        });
    });
}

    async function loadAvailability() {
        loadingState.style.display = "block";
        emptyState.style.display = "none";
        listContainer.innerHTML = "";

        try {
            const response = await fetch("/doctor/availability/api");
            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.message || "Unable to load availability.");
            }

            renderAvailability(data.availability);
        } catch (error) {
            console.error("Availability loading error:", error);
            showMessage(
                error.message || "Unable to load availability.",
                "error"
            );
        } finally {
            loadingState.style.display = "none";
        }
    }

    async function addAvailability(event) {
        event.preventDefault();

        const dayOfWeek = dayInput.value.trim();
        const startTime = startTimeInput.value.trim();
        const endTime = endTimeInput.value.trim();
        const consultationType = consultationTypeInput.value;

        if (!dayOfWeek) {
            showMessage("Please select a day.", "error");
            return;
        }

        if (!startTime || !endTime) {
            showMessage(
                "Please provide both start and end time.",
                "error"
            );
            return;
        }

        try {
            const response = await fetch("/doctor/availability/api", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    day_of_week: dayOfWeek,
                    start_time: startTime,
                    end_time: endTime,
                    consultation_type: consultationType
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Unable to add availability."
                );
            }

            showMessage(
                "Availability added successfully.",
                "success"
            );

            form.reset();

            await loadAvailability();

        } catch (error) {
            console.error("Availability add error:", error);

            showMessage(
                error.message || "Unable to add availability.",
                "error"
            );
        }
    }

    async function deleteAvailability(id) {
        const confirmed = confirm(
            "Are you sure you want to remove this availability?"
        );

        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch(
                `/doctor/availability/api/${id}`,
                {
                    method: "DELETE"
                }
            );

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(
                    data.message || "Unable to remove availability."
                );
            }

            showMessage(
                "Availability removed successfully.",
                "success"
            );

            await loadAvailability();

        } catch (error) {
            console.error("Availability delete error:", error);

            showMessage(
                error.message || "Unable to remove availability.",
                "error"
            );
        }
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    form.addEventListener("submit", addAvailability);

    loadAvailability();
});