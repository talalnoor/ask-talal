// IMPORTANT: Replace this with your deployed backend URL once you deploy to Railway.
// Example: "https://ask-talal-backend-production.up.railway.app"
const BACKEND_URL = "http://localhost:8000";

const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

let history = [];

function addMessage(text, role) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return div;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = chatInput.value.trim();
  if (!userMessage) return;

  addMessage(userMessage, "user");
  history.push({ role: "user", content: userMessage });
  chatInput.value = "";
  sendBtn.disabled = true;

  const loadingEl = addMessage("Thinking...", "agent loading");

  try {
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage, history }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `Server responded ${response.status}`);
    }

    loadingEl.remove();
    addMessage(data.reply, "agent");
    history.push({ role: "assistant", content: data.reply });
  } catch (err) {
    loadingEl.remove();
    addMessage(
      "ERROR (send this to Claude): " + err.message,
      "agent"
    );
    console.error("Chat error:", err);
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
});