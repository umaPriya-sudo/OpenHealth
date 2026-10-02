document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       ELEMENTS
    ====================================================== */

    const selectionCard =
        document.getElementById("symptomSelection");

    const searchInput =
        document.getElementById("symptomSearch");

    const symptomGrid =
        document.getElementById("symptomGrid");

    const symptomTotal =
        document.getElementById("symptomTotal");

    const selectedSymptomsContainer =
        document.getElementById("selectedSymptoms");

    const selectedCount =
        document.getElementById("selectedCount");

    const clearButton =
        document.getElementById("clearSymptomsBtn");

    const predictButton =
        document.getElementById("predictSymptomBtn");

    const errorBox =
        document.getElementById("symptomError");

    const loading =
        document.getElementById("symptomLoading");

    const result =
        document.getElementById("symptomResult");

    const resultDisease =
        document.getElementById("resultDisease");

    const resultSymptoms =
        document.getElementById("resultSymptoms");

    const resultSymptomCount =
        document.getElementById("resultSymptomCount");

    const checkAgainButton =
        document.getElementById("checkAgainBtn");

    const viewDetailsButton =
        document.getElementById("viewDetailsBtn");

    const diseaseDetails =
        document.getElementById("diseaseDetails");

    const detailsDisease =
        document.getElementById("detailsDisease");


    /* =====================================================
       STATE
    ====================================================== */

    let allSymptoms = [];

    let selectedSymptoms = new Set();

    let currentCategory = "all";


    /* =====================================================
       HELPERS
    ====================================================== */

    function normalizeSymptom(symptom) {

        return symptom
            .replaceAll("_", " ")
            .replace(/\s+/g, " ")
            .trim();

    }


    function showError(message) {

        errorBox.textContent = message;

        errorBox.classList.add("show");

    }


    function clearError() {

        errorBox.textContent = "";

        errorBox.classList.remove("show");

    }


    /* =====================================================
       CATEGORY FILTER
    ====================================================== */

    function matchesCategory(symptom) {

        if (currentCategory === "all") {
            return true;
        }


        const value =
            symptom.toLowerCase();


        const categories = {

            general: [
                "fever",
                "fatigue",
                "weakness",
                "chills",
                "sweating",
                "weight",
                "appetite",
                "malaise"
            ],

            skin: [
                "skin",
                "rash",
                "itching",
                "eruption",
                "acne",
                "blister",
                "nail",
                "hair",
                "pigment",
                "redness",
                "ulcer",
                "pus"
            ],

            gastro: [
                "stomach",
                "abdominal",
                "vomit",
                "nausea",
                "diarr",
                "constipation",
                "acidity",
                "indigestion",
                "liver",
                "jaundice",
                "ulcer"
            ],

            respiratory: [
                "cough",
                "breath",
                "throat",
                "nose",
                "sneeze",
                "phlegm",
                "congestion",
                "sinus"
            ],

            musculoskeletal: [
                "joint",
                "muscle",
                "bone",
                "back",
                "neck",
                "stiff",
                "pain"
            ],

            neurological: [
                "headache",
                "dizziness",
                "vertigo",
                "memory",
                "speech",
                "seizure",
                "tingling",
                "numbness"
            ],

            cardiovascular: [
                "chest",
                "heart",
                "pulse",
                "pressure",
                "swelling"
            ],

            other: []

        };


        if (
            currentCategory === "other"
        ) {

            const allKeywords =
                Object.values(categories)
                    .flat();

            return !allKeywords.some(
                keyword =>
                    value.includes(keyword)
            );
        }


        return categories[
            currentCategory
        ].some(
            keyword =>
                value.includes(keyword)
        );

    }


    /* =====================================================
       RENDER SYMPTOMS
    ====================================================== */

    function renderSymptoms() {

        const searchTerm =
            searchInput.value
                .trim()
                .toLowerCase();


        const filtered =
            allSymptoms.filter(symptom => {

                const normalized =
                    normalizeSymptom(
                        symptom
                    ).toLowerCase();


                const matchesSearch =
                    !searchTerm ||
                    normalized.includes(
                        searchTerm
                    );


                return (
                    matchesSearch &&
                    matchesCategory(symptom)
                );

            });


        symptomGrid.innerHTML = "";


        if (filtered.length === 0) {

            symptomGrid.innerHTML = `
                <div
                    style="
                        grid-column: 1 / -1;
                        padding: 25px;
                        text-align: center;
                        color: #8295aa;
                        font-size: 10px;
                    "
                >
                    No symptoms found.
                </div>
            `;

            return;
        }


        filtered.forEach(
            (symptom, index) => {

                const id =
                    `symptom-${index}-${symptom
                        .replace(
                            /[^a-zA-Z0-9]/g,
                            "-"
                        )}`;


                const wrapper =
                    document.createElement(
                        "div"
                    );

                wrapper.className =
                    "symptom-option";


                const input =
                    document.createElement(
                        "input"
                    );

                input.type = "checkbox";

                input.id = id;

                input.value = symptom;

                input.checked =
                    selectedSymptoms.has(
                        symptom
                    );


                const label =
                    document.createElement(
                        "label"
                    );

                label.htmlFor = id;


                const check =
                    document.createElement(
                        "span"
                    );

                check.className =
                    "symptom-check";

                check.innerHTML =
                    '<i class="fas fa-check"></i>';


                const text =
                    document.createElement(
                        "span"
                    );

                text.textContent =
                    normalizeSymptom(
                        symptom
                    );


                label.appendChild(check);

                label.appendChild(text);

                wrapper.appendChild(input);

                wrapper.appendChild(label);

                symptomGrid.appendChild(
                    wrapper
                );


                input.addEventListener(
                    "change",
                    () => {

                        if (
                            input.checked
                        ) {

                            selectedSymptoms.add(
                                symptom
                            );

                        } else {

                            selectedSymptoms.delete(
                                symptom
                            );

                        }


                        updateSelectedUI();

                    }
                );

            }
        );

    }


    /* =====================================================
       SELECTED SYMPTOMS UI
    ====================================================== */

    function updateSelectedUI() {

        const selected =
            Array.from(
                selectedSymptoms
            );


        selectedCount.textContent =
            selected.length;


        predictButton.disabled =
            selected.length === 0;


        if (
            selected.length === 0
        ) {

            selectedSymptomsContainer.innerHTML = `
                <span class="selected-placeholder">
                    Select symptoms above to add them here.
                </span>
            `;

            return;
        }


        selectedSymptomsContainer.innerHTML =
            "";


        selected.forEach(
            symptom => {

                const chip =
                    document.createElement(
                        "span"
                    );

                chip.className =
                    "selected-chip";


                chip.innerHTML = `
                    <span>
                        ${normalizeSymptom(symptom)}
                    </span>

                    <button
                        type="button"
                        aria-label="Remove symptom"
                    >
                        <i class="fas fa-times"></i>
                    </button>
                `;


                chip
                    .querySelector("button")
                    .addEventListener(
                        "click",
                        () => {

                            selectedSymptoms.delete(
                                symptom
                            );

                            renderSymptoms();

                            updateSelectedUI();

                        }
                    );


                selectedSymptomsContainer
                    .appendChild(chip);

            }
        );

    }


    /* =====================================================
       LOAD SYMPTOMS
    ====================================================== */

    async function loadSymptoms() {

        try {

            const response =
                await fetch(
                    "/api/symptoms"
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.message ||
                    "Unable to load symptoms."
                );

            }


            allSymptoms =
                data.symptoms || [];


            symptomTotal.textContent =
                allSymptoms.length;


            const allCount =
                document.getElementById(
                    "allCount"
                );


            if (allCount) {

                allCount.textContent =
                    allSymptoms.length;

            }


            renderSymptoms();

            updateSelectedUI();


        } catch (error) {

            console.error(
                "Symptom loading error:",
                error
            );


            showError(
                "Unable to load symptoms. Please refresh the page."
            );

        }

    }


    /* =====================================================
       SEARCH
    ====================================================== */

    searchInput.addEventListener(
        "input",
        renderSymptoms
    );


    /* =====================================================
       CLEAR ALL
    ====================================================== */

    clearButton.addEventListener(
        "click",
        () => {

            selectedSymptoms.clear();

            clearError();

            renderSymptoms();

            updateSelectedUI();

        }
    );


    /* =====================================================
       CATEGORY BUTTONS
    ====================================================== */

    document
        .querySelectorAll(
            ".category-item"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    document
                        .querySelectorAll(
                            ".category-item"
                        )
                        .forEach(item => {

                            item.classList.remove(
                                "active"
                            );

                        });


                    button.classList.add(
                        "active"
                    );


                    currentCategory =
                        button.dataset.category;


                    renderSymptoms();

                }
            );

        });


    /* =====================================================
       PREDICT DISEASE
    ====================================================== */

    predictButton.addEventListener(
        "click",
        async () => {

            clearError();


            const symptoms =
                Array.from(
                    selectedSymptoms
                );


            if (
                symptoms.length === 0
            ) {

                showError(
                    "Please select at least one symptom."
                );

                return;

            }


            selectionCard.style.display =
                "none";


            result.classList.remove(
                "show"
            );


            loading.classList.add(
                "show"
            );


            try {

                const response =
                    await fetch(
                        "/api/symptoms/predict",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            credentials:
                                "same-origin",

                            body:
                                JSON.stringify({
                                    symptoms:
                                        symptoms
                                })
                        }
                    );


                const data =
                    await response.json();


                if (
                    response.status === 401 ||
                    data.requires_login
                ) {

                    loading.classList.remove(
                        "show"
                    );


                    selectionCard.style.display =
                        "block";


                    if (
                        typeof window.openAuthModal ===
                        "function"
                    ) {

                        window.openAuthModal(
                            "signin"
                        );

                    }

                    return;

                }


                if (
                    !response.ok ||
                    !data.success
                ) {

                    throw new Error(
                        data.message ||
                        "Prediction failed."
                    );

                }


                const prediction =
                    data.result;


                resultDisease.textContent =
                    prediction.disease;

                renderAssociatedMedicines(prediction.associated_medicines);

                detailsDisease.textContent =
                    prediction.disease;


                resultSymptomCount.textContent =
                    symptoms.length;


                resultSymptoms.innerHTML =
                    "";

                


                symptoms.forEach(
                    symptom => {

                        const chip =
                            document.createElement(
                                "span"
                            );

                        chip.className =
                            "result-chip";

                        chip.textContent =
                            normalizeSymptom(
                                symptom
                            );


                        resultSymptoms
                            .appendChild(chip);

                    }
                );


                loading.classList.remove(
                    "show"
                );


                result.classList.add(
                    "show"
                );


                window.scrollTo({
                    top: 0,
                    behavior: "smooth"
                });


            } catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );


                loading.classList.remove(
                    "show"
                );


                selectionCard.style.display =
                    "block";


                showError(
                    error.message ||
                    "Unable to predict the disease."
                );

            }

        }
    );


    /* =====================================================
       CHECK AGAIN
    ====================================================== */

    checkAgainButton.addEventListener(
        "click",
        () => {

            result.classList.remove(
                "show"
            );


            diseaseDetails.classList.remove(
                "show"
            );


            selectionCard.style.display =
                "block";


            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }
    );


    /* =====================================================
       VIEW DETAILS
    ====================================================== */

    viewDetailsButton.addEventListener(
        "click",
        () => {

            diseaseDetails.classList.add(
                "show"
            );

            diseaseDetails.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }
    );

    /* =====================================================
           DISEASE DETAIL TABS
        ===================================================== */

    const detailTabs =
        document.querySelectorAll(".details-tab");
    
    const detailTabContents = {
        overview: document.getElementById("detailsOverview"),
        symptoms: document.getElementById("detailsSymptoms"),
        causes: document.getElementById("detailsCauses"),
        precautions: document.getElementById("detailsPrecautions"),
        medicines: document.getElementById("detailsMedicines")
    };
    
    
    function showDetailTab(tabName) {
    
        /* Remove active state from all tabs */
    
        detailTabs.forEach(tab => {
        
            tab.classList.remove("active");
        
        });
    
    
        /* Hide all content */
    
        Object.values(detailTabContents)
            .forEach(content => {
            
                if (content) {
                
                    content.classList.remove("active");
                
                }
            
            });
        
        
        /* Activate selected tab */
        
        const selectedTab =
            document.querySelector(
                `.details-tab[data-tab="${tabName}"]`
            );
        
        
        if (selectedTab) {
        
            selectedTab.classList.add("active");
        
        }
    
    
        /* Show selected content */
    
        if (
            detailTabContents[tabName]
        ) {
        
            detailTabContents[tabName]
                .classList.add("active");
        
        }
    
    
        /* Update selected symptoms */
    
        if (
            tabName === "symptoms"
        ) {
        
            renderDetailsSymptoms();
        
        }
    
    }
    
    
    /* =====================================================
       DETAIL TAB CLICK
    ===================================================== */
    
    detailTabs.forEach(tab => {
    
        tab.addEventListener(
            "click",
            () => {
            
                const tabName =
                    tab.dataset.tab;
            
                showDetailTab(tabName);
            
            }
        );
    
    });
    
    
    /* =====================================================
       RENDER SELECTED SYMPTOMS
    ===================================================== */
    
    function renderDetailsSymptoms() {
    
        const container =
            document.getElementById(
                "detailsSymptomsList"
            );
        
        
        if (!container) {
            return;
        }
    
    
        container.innerHTML = "";
    
    
        const symptoms =
            Array.from(
                selectedSymptoms
            );
        
        
        if (symptoms.length === 0) {
        
            container.innerHTML = `
                <p>
                    No symptoms were selected.
                </p>
            `;
        
            return;
        
        }
    
    
        symptoms.forEach(symptom => {
        
            const chip =
                document.createElement("span");
        
            chip.className =
                "details-symptom-chip";
        
            chip.textContent =
                normalizeSymptom(symptom);
        
            container.appendChild(chip);
        
        });
    
    }

    /* =====================================================
       RENDER ASSOCIATED MEDICINES
    ===================================================== */

    function renderAssociatedMedicines(medicines) {

        const container =
            document.getElementById("associatedMedicinesList");

        const diseaseName =
            document.getElementById("medicinesDiseaseName");

        if (!container) {
            return;
        }

        container.innerHTML = "";

        if (diseaseName) {
            diseaseName.textContent =
                detailsDisease.textContent || "this condition";
        }

        if (!medicines || medicines.length === 0) {

            container.innerHTML = `
                <div class="details-info-box">
                    <i class="fas fa-circle-info"></i>

                    <span>
                        No commonly associated medicine information
                        is currently available for this condition.
                    </span>
                </div>
            `;

            return;
        }

        medicines.forEach(medicine => {

            const card =
                document.createElement("div");

            card.className =
                "associated-medicine-card";

            card.innerHTML = `
                <div class="medicine-card-header">

                    <div class="medicine-card-icon">
                        <i class="fas fa-capsules"></i>
                    </div>

                    <div>
                        <h4 class="medicine-card-name">
                            ${medicine.name}
                        </h4>

                        <p class="medicine-card-type">
                            ${medicine.type}
                        </p>
                    </div>

                </div>

                <p class="medicine-card-description">
                    ${medicine.description}
                </p>

                <a
                    href="/medicine-info/${encodeURIComponent(medicine.name)}"
                    class="medicine-card-details"
                >
                    View Details
                    <i class="fas fa-arrow-right"></i>
                </a>
            `;

            container.appendChild(card);
        });
    }

    /* =====================================================
        INITIALIZATION
    ====================================================== */

    loadSymptoms();

});