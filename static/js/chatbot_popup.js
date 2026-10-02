// =========================================================
// OpenHealth - Floating Chatbot
// Step 2: Connect Popup With Chatbot Backend
// =========================================================


document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // Elements
    // =====================================================

    const chatbotToggle =
        document.getElementById("chatbot-toggle");

    const chatbotPanel =
        document.getElementById("chatbot-panel");

    const chatbotClose =
        document.getElementById("chatbot-close");

    const chatMessages =
        document.getElementById("chatbot-popup-messages");

    const chatInput =
        document.getElementById("chatbot-popup-input");

    const chatSend =
        document.getElementById("chatbot-popup-send");


    // =====================================================
    // Safety Check
    // =====================================================

    if (
        !chatbotToggle ||
        !chatbotPanel ||
        !chatbotClose ||
        !chatMessages ||
        !chatInput ||
        !chatSend
    ) {
        return;
    }


    // =====================================================
    // Open Chatbot
    // =====================================================

    chatbotToggle.addEventListener("click", function () {

        chatbotPanel.classList.add("active");

        chatbotPanel.setAttribute(
            "aria-hidden",
            "false"
        );

        setTimeout(function () {
            chatInput.focus();
        }, 250);

    });


    // =====================================================
    // Close Chatbot
    // =====================================================

    chatbotClose.addEventListener("click", function () {

        chatbotPanel.classList.remove("active");

        chatbotPanel.setAttribute(
            "aria-hidden",
            "true"
        );

    });


    // =====================================================
    // Format Bot Response
    // =====================================================

    function formatBotResponse(text) {

        const symptomCheckerButton =
            `<a href="/symptom-checker" class="chatbot-feature-action">
                <i class="fas fa-stethoscope"></i>
                Open Symptom Checker
                <i class="fas fa-arrow-right"></i>
            </a>`;

        const findDoctorButton =
            `<a href="/doctor-appointment" class="chatbot-feature-action">
                <i class="fas fa-user-doctor"></i>
                Find a Doctor
                <i class="fas fa-arrow-right"></i>
            </a>`;

        const medicineRecognitionButton =
            `<a href="/recognition" class="chatbot-feature-action">
                <i class="fas fa-pills"></i>
                Identify Medicine
                <i class="fas fa-arrow-right"></i>
            </a>`;

        const bookAppointmentButton =
            `<a href="/doctor-appointment" class="chatbot-feature-action">
                <i class="fas fa-calendar-check"></i>
                Book Appointment
                <i class="fas fa-arrow-right"></i>
            </a>`;

        const diseasePredictionButton =
            `<a href="/services" class="chatbot-feature-action">
                <i class="fas fa-heart-pulse"></i>
                Open Disease Prediction
                <i class="fas fa-arrow-right"></i>
            </a>`;

        const formattedText = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(
                /\[ACTION:SYMPTOM_CHECKER\]/g,
                symptomCheckerButton
            )
            .replace(
                /\[ACTION:FIND_DOCTOR\]/g,
                findDoctorButton
            )
            .replace(
                /\[ACTION:MEDICINE_RECOGNITION\]/g,
                medicineRecognitionButton
            )
            .replace(
                /\[ACTION:BOOK_APPOINTMENT\]/g,
                bookAppointmentButton
            )
            .replace(
                /\[ACTION:DISEASE_PREDICTION\]/g,
                diseasePredictionButton
            )
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(
                /^• (.*)$/gm,
                '<span class="chat-bullet">• $1</span>'
            )
            .replace(/\n/g, "<br>");

        return formattedText;
    }


    // =====================================================
    // Add User Message
    // =====================================================

    function addUserMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "chat-message user";

        const paragraph =
            document.createElement("p");

        paragraph.textContent = message;

        messageDiv.appendChild(paragraph);

        chatMessages.appendChild(messageDiv);

        scrollToBottom();
    }


    // =====================================================
    // Add Bot Message
    // =====================================================

    function addBotMessage(message) {

        const messageDiv =
            document.createElement("div");

        messageDiv.className =
            "chat-message bot";

        const paragraph =
            document.createElement("p");

        paragraph.innerHTML =
            formatBotResponse(message);

        messageDiv.appendChild(paragraph);

        chatMessages.appendChild(messageDiv);

        scrollToBottom();
    }


    // =====================================================
    // Loading Message
    // =====================================================

    function addLoadingMessage() {

        const loadingDiv =
            document.createElement("div");

        loadingDiv.className =
            "chat-message bot";

        loadingDiv.id =
            "popup-bot-loading";

        loadingDiv.innerHTML =
            `<p>🤔 <span class="typing">Thinking...</span></p>`;

        chatMessages.appendChild(loadingDiv);

        scrollToBottom();
    }


    // =====================================================
    // Remove Loading Message
    // =====================================================

    function removeLoadingMessage() {

        const loadingMessage =
            document.getElementById(
                "popup-bot-loading"
            );

        if (loadingMessage) {
            loadingMessage.remove();
        }
    }


    // =====================================================
    // Scroll To Bottom
    // =====================================================

    function scrollToBottom() {

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    }


    // =====================================================
    // Send Message
    // =====================================================

    function sendPopupMessage() {

        const message =
            chatInput.value.trim();

        if (!message) {
            return;
        }


        // Add user's message
        addUserMessage(message);


        // Clear input
        chatInput.value = "";


        // Disable while processing
        chatInput.disabled = true;
        chatSend.disabled = true;


        // Show loading
        addLoadingMessage();


        // Send to Flask backend
        fetch("/chatbot", {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            body:
                `message=${encodeURIComponent(message)}`
        })

        .then(function (response) {

            if (!response.ok) {
                throw new Error(
                    "Server returned an error."
                );
            }

            return response.json();

        })

        .then(function (data) {

            removeLoadingMessage();

            addBotMessage(
                data.response ||
                "Sorry, I couldn't generate a response."
            );

        })

        .catch(function (error) {

            console.error(
                "Chatbot error:",
                error
            );

            removeLoadingMessage();

            addBotMessage(
                "⚠️ Sorry, I'm having trouble connecting. Please try again."
            );

        })

        .finally(function () {

            chatInput.disabled = false;
            chatSend.disabled = false;

            chatInput.focus();

            scrollToBottom();

        });
    }


    // =====================================================
    // Send Button
    // =====================================================

    chatSend.addEventListener(
        "click",
        sendPopupMessage
    );


    // =====================================================
    // Enter Key
    // =====================================================

    chatInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendPopupMessage();

            }

        }
    );

});