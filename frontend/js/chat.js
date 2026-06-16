const API_BASE =
    "http://127.0.0.1:8000";

let sessionId = null;

const chatToggle =
    document.getElementById(
        "chat-toggle"
    );

const chatWidget =
    document.getElementById(
        "chat-widget"
    );

const chatClose =
    document.getElementById(
        "chat-close"
    );

const messages =
    document.getElementById(
        "messages"
    );

const input =
    document.getElementById(
        "message-input"
    );

const sendButton =
    document.getElementById(
        "send-button"
    );


const clearChat =
    document.getElementById(
        "clear-chat"
    );

/* =====================================
   SESSION
===================================== */

async function createSession() {

    try {

        const response =
            await fetch(
                `${API_BASE}/api/session`,
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();

        sessionId =
            data.session_id;

        localStorage.setItem(
            "session_id",
            sessionId
        );

        addBotMessage(
            data.reply
        );

    } catch (error) {

        console.error(error);

        addBotMessage(
            "Unable to connect to server."
        );
    }
}

function loadSession() {

    const storedSessionId =
        localStorage.getItem(
            "session_id"
        );

    if (storedSessionId) {

        sessionId =
            parseInt(
                storedSessionId
            );
    }
}


/* =====================================
   MESSAGE RENDERING
===================================== */

function addUserMessage(
    text
) {

    messages.innerHTML += `
        <div class="user-message">
            <div class="user-bubble">
                ${escapeHtml(text)}
            </div>
        </div>
    `;

    scrollToBottom();
}

function addBotMessage(
    text,
    sources = []
) {

    let sourcesHtml = "";

    if (sources.length > 0) {

        sourcesHtml += `
            <div class="sources-container">
        `;

        for (
            const source
            of sources
        ) {

            sourcesHtml += `
                <a
                    href="${source.url}"
                    target="_blank"
                    class="source-card"
                >
                    📄 ${source.title}
                </a>
            `;
        }

        sourcesHtml += `
            </div>
        `;
    }

    messages.innerHTML += `
        <div class="bot-message">

            <div
                class="bot-avatar"
            >
                🤖
            </div>

            <div>

                <div
                    class="bot-bubble"
                >
                    ${escapeHtml(text)}
                </div>

                ${sourcesHtml}

            </div>

        </div>
    `;

    scrollToBottom();
}


/* =====================================
   TYPING
===================================== */

function showTyping() {

    messages.innerHTML += `
        <div
            id="typing"
            class="bot-message"
        >

            <div
                class="bot-avatar"
            >
                🤖
            </div>

            <div
                class="bot-bubble"
            >

                <div
                    class="typing-indicator"
                >
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>

            </div>

        </div>
    `;

    scrollToBottom();
}

function hideTyping() {

    const typing =
        document.getElementById(
            "typing"
        );

    if (typing) {

        typing.remove();
    }
}


/* =====================================
   CHAT API
===================================== */

async function sendMessage() {

    const text =
        input.value.trim();

    if (!text) {

        return;
    }

    if (!sessionId) {

        return;
    }

    addUserMessage(
        text
    );

    input.value = "";

    showTyping();

    try {

        const response =
            await fetch(
                `${API_BASE}/api/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            session_id:
                                sessionId,

                            message:
                                text
                        }
                    )
                }
            );

        const data =
            await response.json();

        hideTyping();

        addBotMessage(
            data.reply,
            data.sources || []
        );

    } catch (error) {

        hideTyping();

        console.error(
            error
        );

        addBotMessage(
            "Something went wrong."
        );
    }
}


async function loadMessages() {

    if (!sessionId) {

        return;
    }

    const response =
        await fetch(
            `${API_BASE}/api/session/${sessionId}/messages`
        );

    const data =
        await response.json();

    messages.innerHTML = "";

    for (
        const message
        of data
    ) {

        if (
            message.role === "user"
        ) {

            addUserMessage(
                message.content
            );
        }
        else {

            addBotMessage(
                message.content
            );
        }
    }
}

async function clearHistory() {

    if (!sessionId) {

        return;
    }

    const confirmed =
        confirm(
            "Clear chat history?"
        );

    if (!confirmed) {

        return;
    }

    await fetch(
        `${API_BASE}/api/session/${sessionId}/messages`,
        {
            method: "DELETE"
        }
    );

    localStorage.removeItem(
        "session_id"
    );

    location.reload();
}

/* =====================================
   HELPERS
===================================== */

function scrollToBottom() {

    messages.scrollTop =
        messages.scrollHeight;
}

function escapeHtml(
    unsafe
) {

    const div =
        document.createElement(
            "div"
        );

    div.innerText =
        unsafe;

    return div.innerHTML;
}


/* =====================================
   EVENTS
===================================== */

chatToggle.addEventListener(
    "click",
    async () => {

        chatWidget.classList.remove(
            "hidden"
        );

        chatToggle.classList.add(
            "hidden"
        );

        if (!sessionId) {

            await createSession();
        }
        else {

            await loadMessages();
        }
    }
);

clearChat.addEventListener(
    "click",
    clearHistory
);

chatClose.addEventListener(
    "click",
    () => {

        chatWidget.classList.add(
            "hidden"
        );

        chatToggle.classList.remove(
            "hidden"
        );
    }
);

sendButton.addEventListener(
    "click",
    sendMessage
);

input.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter"
        ) {

            sendMessage();
        }
    }
);


/* =====================================
   INIT
===================================== */

loadSession();