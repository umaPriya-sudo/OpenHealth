document.addEventListener("DOMContentLoaded", () => {

    const inputContainer =
        document.getElementById("inputDataContainer");

    const resultContainer =
        document.getElementById("resultDetailsContainer");

    let inputData = {};
    let resultDetails = {};

    const inputDataElement =
        document.getElementById("recordInputData");

    const resultDetailsElement =
        document.getElementById("recordResultDetails");


    try {

        if (inputDataElement) {

            inputData = JSON.parse(
                inputDataElement.textContent
            );

        }

    } catch (error) {

        console.error(
            "Unable to parse input data:",
            error
        );

    }


    try {

        if (resultDetailsElement) {

            resultDetails = JSON.parse(
                resultDetailsElement.textContent
            );

        }

    } catch (error) {

        console.error(
            "Unable to parse result details:",
            error
        );

    }

    /* =====================================================
       Convert JSON data safely
       ===================================================== */


    try {
        if (typeof inputData === "string") {
            inputData = JSON.parse(inputData);
        }
    } catch (error) {
        console.error(
            "Unable to parse input data:",
            error
        );

        inputData = {};
    }


    try {
        if (typeof resultDetails === "string") {
            resultDetails = JSON.parse(resultDetails);
        }
    } catch (error) {
        console.error(
            "Unable to parse result details:",
            error
        );

        resultDetails = {};
    }


    /* =====================================================
       Format field names
       ===================================================== */

    function formatLabel(key) {

        return key
            .replace(/_/g, " ")
            .replace(/([a-z])([A-Z])/g, "$1 $2")
            .replace(/\b\w/g, letter =>
                letter.toUpperCase()
            );
    }


    /* =====================================================
       Format values
       ===================================================== */

    function formatValue(value) {
        
        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            return "—";
        }
    
        if (typeof value === "object") {
        
            if (!Array.isArray(value)) {
            
                return Object.entries(value)
                    .map(([key, val]) => {
                    
                        let displayValue = val;
                    
                        if (
                            typeof val === "number" &&
                            val >= 0 &&
                            val <= 1
                        ) {
                            displayValue =
                                `${(val * 100).toFixed(2)}%`;
                        }
                    
                        return `${formatLabel(key)}: ${displayValue}`;
                    
                    })
                    .join("<br>");
            }
        
            return value.join(", ");
        }
    
        return String(value);
    }
    

    /* =====================================================
       Render Input Information
       ===================================================== */

    function renderInputData() {

        if (!inputContainer) {
            return;
        }

        inputContainer.innerHTML = "";

        const entries =
            Object.entries(inputData || {});


        if (entries.length === 0) {

            inputContainer.innerHTML = `
                <div class="record-data-item">
                    <span class="record-data-label">
                        Information
                    </span>

                    <span class="record-data-value">
                        Not available
                    </span>
                </div>
            `;

            return;
        }


        entries.forEach(([key, value]) => {

            const item =
                document.createElement("div");

            item.className =
                "record-data-item";

            item.innerHTML = `
                <span class="record-data-label">
                    ${formatLabel(key)}
                </span>

                <span class="record-data-value">
                    ${formatValue(value)}
                </span>
            `;

            inputContainer.appendChild(item);

        });

    }


    /* =====================================================
       Render Result Details
       ===================================================== */

    function renderResultDetails() {

        if (!resultContainer) {
            return;
        }

        resultContainer.innerHTML = "";

        const entries =
            Object.entries(resultDetails || {});


        if (entries.length === 0) {

            resultContainer.innerHTML = `
                <div class="record-data-item">
                    <span class="record-data-label">
                        Information
                    </span>

                    <span class="record-data-value">
                        Not available
                    </span>
                </div>
            `;

            return;
        }


        entries.forEach(([key, value]) => {

            const item =
                document.createElement("div");

            item.className =
                "record-data-item";

            item.innerHTML = `
                <span class="record-data-label">
                    ${formatLabel(key)}
                </span>

                <span class="record-data-value">
                    ${formatValue(value)}
                </span>
            `;

            resultContainer.appendChild(item);

        });

    }


    renderInputData();
    renderResultDetails();

});