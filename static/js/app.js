const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const messagesEl = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const statusText = document.getElementById("connectionStatus");
const statusDot = document.querySelector(".status-dot");

let history = [];
let busy = false;

async function checkStatus() {
  try {
    const response = await fetch("/api/status");
    const data = await response.json();
    statusText.textContent = data.configured ? "AI service connected" : "API key not configured";
    statusDot.classList.toggle("online", data.configured);
  } catch {
    statusText.textContent = "Server connection unavailable";
  }
}

function addMessage(role, content) {
  welcome.hidden = true;
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "Y" : "✦";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  // textContent prevents model output from being interpreted as HTML.
  bubble.textContent = content;
  wrapper.append(avatar, bubble);
  messagesEl.appendChild(wrapper);
  wrapper.scrollIntoView({ behavior: "smooth", block: "end" });
  return bubble;
}

function setBusy(value) {
  busy = value;
  sendBtn.disabled = value;
  input.disabled = value;
}

async function sendMessage(message) {
  const clean = message.trim();
  if (!clean || busy) return;

  addMessage("user", clean);
  const previousHistory = [...history];
  history.push({ role: "user", content: clean });
  input.value = "";
  input.style.height = "auto";
  setBusy(true);
  const pending = addMessage("model", "CampusMate is thinking…");
  pending.classList.add("typing");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: clean, history: previousHistory })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    pending.classList.remove("typing");
    pending.textContent = data.answer;
    history.push({ role: "model", content: data.answer });
  } catch (error) {
    pending.classList.remove("typing");
    pending.textContent = `Sorry, ${error.message}`;
    // Do not keep a failed user turn in the conversation context.
    history = previousHistory;
  } finally {
    setBusy(false);
    input.focus();
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  sendMessage(input.value);
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 150)}px`;
});
input.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

document.querySelectorAll("[data-prompt]").forEach(button => {
  button.addEventListener("click", () => {
    const prompt = button.dataset.prompt;
    input.value = prompt;
    input.focus();
    if (prompt.endsWith(": ")) return;
    sendMessage(prompt);
  });
});

document.getElementById("newChatBtn").addEventListener("click", () => {
  history = [];
  messagesEl.replaceChildren();
  welcome.hidden = false;
  input.value = "";
  input.focus();
});

checkStatus();
