// =========================================================
// OpenHealth - Chatbot JavaScript
// =========================================================

function formatBotResponse(text) {
    return text
        // Escape HTML characters for safety
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')

        // Bold: **text**
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

        // Bullet points: • text
        .replace(/^• (.*)$/gm, '<span class="chat-bullet">• $1</span>')

        // New lines
        .replace(/\n/g, '<br>');
}

function sendMessage() {

    const input = document.getElementById('user-message');
    const message = input.value.trim();

    if (!message) return;

    const messagesContainer =
        document.getElementById('chat-messages');

    // Add user message safely
    const userDiv = document.createElement('div');

    userDiv.className = 'chat-message user';

    const userText = document.createElement('p');
    userText.textContent = message;

    userDiv.appendChild(userText);
    messagesContainer.appendChild(userDiv);

    // Clear input
    input.value = '';

    // Add loading message
    const botDiv = document.createElement('div');

    botDiv.className = 'chat-message bot';
    botDiv.id = 'bot-loading';

    botDiv.innerHTML =
        `<p>🤔 <span class="typing">Thinking...</span></p>`;

    messagesContainer.appendChild(botDiv);

    messagesContainer.scrollTop =
        messagesContainer.scrollHeight;

    // Send message to Flask backend
    fetch('/chatbot', {
        method: 'POST',

        headers: {
            'Content-Type':
                'application/x-www-form-urlencoded'
        },

        body:
            `message=${encodeURIComponent(message)}`
    })

    .then(response => response.json())

    .then(data => {

        const loadingMessage =
            document.getElementById('bot-loading');

        if (loadingMessage) {
            loadingMessage.remove();
        }

        const botResponse =
            document.createElement('div');

        botResponse.className =
            'chat-message bot';

        botResponse.innerHTML =
            `<p>${formatBotResponse(data.response)}</p>`;

        messagesContainer.appendChild(botResponse);

        messagesContainer.scrollTop =
            messagesContainer.scrollHeight;
    })

    .catch(error => {

        const loadingMessage =
            document.getElementById('bot-loading');

        if (loadingMessage) {
            loadingMessage.remove();
        }

        const errorDiv =
            document.createElement('div');

        errorDiv.className =
            'chat-message bot';

        errorDiv.innerHTML =
            `<p>⚠️ Sorry, I'm having trouble connecting. Please try again.</p>`;

        messagesContainer.appendChild(errorDiv);

        messagesContainer.scrollTop =
            messagesContainer.scrollHeight;
    });
}

