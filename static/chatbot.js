const chatBody = document.getElementById("chatBody");

const userInput = document.getElementById("userInput");

const sendButton = document.getElementById("sendButton");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.className =
        sender === "user"
            ? "message user-message"
            : "message bot-message";

    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.innerHTML =
        sender === "user"
            ? '<i class="fas fa-user"></i>'
            : '<i class="fas fa-robot"></i>';

    const content = document.createElement("div");

    content.className = "message-content";

    // Use textContent to safely display chatbot responses
    content.textContent = message;

    messageDiv.appendChild(avatar);

    messageDiv.appendChild(content);

    chatBody.appendChild(messageDiv);

    chatBody.scrollTop = chatBody.scrollHeight;
}


function showTyping() {

    const typing = document.createElement("div");

    typing.id = "typing";

    typing.className = "typing";

    typing.textContent = "AI Assistant is typing...";

    chatBody.appendChild(typing);

    chatBody.scrollTop = chatBody.scrollHeight;
}


function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


async function sendMessage() {

    const message = userInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

    sendButton.disabled = true;

    showTyping();

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        removeTyping();

        if (!response.ok) {
            throw new Error(data.error || "Unable to process message.");
        }

        addMessage(data.response, "bot");

    }

    catch (error) {

        removeTyping();

        addMessage(
            "Sorry, something went wrong. " + error.message,
            "bot"
        );

    }

    finally {

        sendButton.disabled = false;

        userInput.focus();

    }

}


function sendSuggestion(question) {

    userInput.value = question;

    sendMessage();

}


// Send message using Enter key

userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();

    }

});