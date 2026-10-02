document.addEventListener("DOMContentLoaded", () => {

    const filterButtons =
        document.querySelectorAll(".appointment-filter");

    const appointmentCards =
        document.querySelectorAll(".appointment-card");


    filterButtons.forEach(button => {

        button.addEventListener("click", () => {

            const filter =
                button.dataset.filter;


            // -------------------------------------------------
            // Active tab
            // -------------------------------------------------

            filterButtons.forEach(item => {
                item.classList.remove("active");
            });

            button.classList.add("active");


            // -------------------------------------------------
            // Filter appointment cards
            // -------------------------------------------------

            appointmentCards.forEach(card => {

                const status =
                    card.dataset.status;

                if (filter === "all") {

                    card.style.display = "";

                }
                else if (filter === "confirmed") {

                    card.style.display =
                        status === "confirmed"
                            ? ""
                            : "none";

                }
                else if (filter === "completed") {

                    card.style.display =
                        status === "completed"
                            ? ""
                            : "none";

                }
                else if (filter === "cancelled") {

                    card.style.display =
                        status === "cancelled"
                            ? ""
                            : "none";

                }

            });

        });

    });

});