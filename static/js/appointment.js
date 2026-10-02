document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       ELEMENTS
       ===================================================== */

    const searchInput =
        document.getElementById("doctorSearch");

    const searchButton =
        document.getElementById("searchDoctorBtn");

    const specialtyCards =
        document.querySelectorAll(".specialty-card");

    const viewAllButton =
        document.getElementById("viewAllSpecialties");


    /* =====================================================
       SEARCH
       ===================================================== */

    function searchDoctors() {

        if (!searchInput) {
            return;
        }

        const searchValue =
            searchInput.value.trim();

        if (!searchValue) {
            searchInput.focus();
            return;
        }


        /*
         * Search is handled by the doctor listing route.
         * We pass the entered value as a query parameter.
         */

        window.location.href =
            "/doctor-appointment/doctors?search=" +
            encodeURIComponent(searchValue);

    }


    /* =====================================================
       SEARCH BUTTON
       ===================================================== */

    if (searchButton) {

        searchButton.addEventListener(
            "click",
            searchDoctors
        );

    }


    /* =====================================================
       ENTER KEY SEARCH
       ===================================================== */

    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            (event) => {

                if (event.key === "Enter") {

                    event.preventDefault();

                    searchDoctors();

                }

            }
        );

    }


    /* =====================================================
       SPECIALTY CARDS
       ===================================================== */

    specialtyCards.forEach(card => {

        card.addEventListener("click", () => {

            const specialty =
                card.dataset.specialty;

            if (!specialty) {
                return;
            }


            window.location.href =
                "/doctor-appointment/doctors?specialty=" +
                encodeURIComponent(specialty);

        });

    });


    /* =====================================================
       VIEW ALL SPECIALTIES
       ===================================================== */

    if (viewAllButton) {

        viewAllButton.addEventListener(
            "click",
            () => {

                const firstSpecialty =
                    document.querySelector(
                        ".specialty-card"
                    );

                if (firstSpecialty) {

                    firstSpecialty.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }

            }
        );

    }

});