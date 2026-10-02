document.addEventListener("DOMContentLoaded", () => {

    const readMoreButtons =
        document.querySelectorAll(".medicine-read-more");


    readMoreButtons.forEach(button => {

        button.addEventListener("click", () => {

            const content =
                button.previousElementSibling;

            if (!content) {
                return;
            }


            const isExpanded =
                content.classList.contains("expanded");


            if (isExpanded) {

                content.classList.remove("expanded");

                button.classList.remove("expanded");

                button.innerHTML = `
                    Read More
                    <i class="fas fa-chevron-down"></i>
                `;

            } else {

                content.classList.add("expanded");

                button.classList.add("expanded");

                button.innerHTML = `
                    Show Less
                    <i class="fas fa-chevron-up"></i>
                `;
            }

        });

    });

});