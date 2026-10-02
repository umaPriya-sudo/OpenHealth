// =========================================================
// OpenHealth - Medicine Recognition JavaScript
// =========================================================

// Preview selected medicine image
function previewMedicineImage(event) {

    const fileInput = event.target;
    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    // Check file type
    const allowedTypes = [
        "image/jpeg",
        "image/png"
    ];

    if (!allowedTypes.includes(file.type)) {
        alert("Please select a JPG, JPEG, or PNG image.");
        fileInput.value = "";
        return;
    }

    // Find the selected-name area
    const selectedName = document.getElementById(
        "medicine-selected-name"
    );

    if (selectedName) {
        selectedName.textContent = `Selected: ${file.name}`;
    }
}