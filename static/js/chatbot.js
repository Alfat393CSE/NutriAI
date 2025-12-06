// Chatbot JavaScript

let sessionId = null;
let isTyping = false;

document.addEventListener('DOMContentLoaded', () => {
    sessionId = localStorage.getItem('chatSessionId') || null;
});

document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isTyping) return;
    
    // Clear input
    input.value = '';
    
    // Display user message
    appendMessage(message, 'user');
    
    // Show typing indicator
    showTyping();
    
    try {
        const response = await window.nutriAI.apiRequest('/api/chatbot/message', 'POST', {
            message,
            session_id: sessionId
        });
        
        // Save session ID
        if (!sessionId) {
            sessionId = response.session_id;
            localStorage.setItem('chatSessionId', sessionId);
        }
        
        hideTyping();
        appendMessage(response.response, 'bot');
        
    } catch (error) {
        hideTyping();
        appendMessage('Sorry, I encountered an error. Please try again.', 'bot');
    }
});

function appendMessage(text, role) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message animate-fade-in`;
    
    if (role === 'bot') {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                ${formatMessage(text)}
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                ${formatMessage(text)}
            </div>
            <div class="message-avatar user-avatar">
                <i class="fas fa-user"></i>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(text) {
    // Convert newlines to <br> and preserve formatting
    return text.replace(/\n/g, '<br>');
}

function showTyping() {
    isTyping = true;
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTyping() {
    isTyping = false;
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function sendQuickQuestion(question) {
    document.getElementById('messageInput').value = question;
    document.getElementById('chatForm').dispatchEvent(new Event('submit'));
}

// Add CSS for chat
const chatbotStyles = document.createElement('style');
chatbotStyles.textContent = `
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        background: white;
        border-radius: var(--border-radius-xl);
        box-shadow: var(--shadow-xl);
        overflow: hidden;
        height: calc(100vh - 120px);
        display: flex;
        flex-direction: column;
    }
    .chat-header {
        padding: 32px;
        background: linear-gradient(135deg, var(--primary), var(--purple));
        color: white;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .chat-avatar {
        width: 64px;
        height: 64px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    .chat-header h2 {
        color: white;
        margin-bottom: 4px;
    }
    .chat-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 32px;
        background: var(--bg-secondary);
    }
    .message {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }
    .message.user-message {
        flex-direction: row-reverse;
    }
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .message.user-message .message-avatar {
        background: var(--gray-600);
    }
    .message-content {
        max-width: 70%;
        padding: 16px 20px;
        border-radius: 16px;
        background: white;
        box-shadow: var(--shadow-sm);
    }
    .message.user-message .message-content {
        background: var(--primary);
        color: white;
    }
    .message-content p {
        margin-bottom: 12px;
        color: inherit;
    }
    .message-content ul {
        padding-left: 24px;
    }
    .message-content li {
        margin-bottom: 8px;
    }
    .typing-indicator {
        display: flex;
        gap: 6px;
        padding: 8px 0;
    }
    .typing-indicator span {
        width: 8px;
        height: 8px;
        background: var(--primary);
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    .chat-input-form {
        padding: 24px;
        background: white;
        border-top: 1px solid var(--gray-200);
    }
    .chat-input {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
    }
    .chat-input input {
        flex: 1;
        padding: 14px 20px;
        border: 2px solid var(--gray-200);
        border-radius: 24px;
        font-size: 1rem;
    }
    .chat-input input:focus {
        outline: none;
        border-color: var(--primary);
    }
    .chat-input button {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .quick-questions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .quick-q {
        padding: 8px 16px;
        background: var(--bg-secondary);
        border: 1px solid var(--gray-200);
        border-radius: 20px;
        font-size: 0.875rem;
        cursor: pointer;
        transition: var(--transition);
    }
    .quick-q:hover {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
    }
`;
document.head.appendChild(chatbotStyles);
