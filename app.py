
import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Cloudflare configuration
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
MODEL_NAME = os.getenv(
    "CLOUDFLARE_MODEL",
    "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
)

API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL_NAME}"
    if ACCOUNT_ID else None
)

SYSTEM_INSTRUCTION = """
You are CampusMate, a friendly and reliable AI Student Assistant.

Help students understand:
- Academic subjects
- Programming and coding
- College projects
- Examination preparation
- Study planning
- General learning questions

Use simple English and explain concepts step by step.

For programming questions:
- Provide readable code.
- Explain important lines.
- Give examples when useful.

If a question is unclear, ask one short clarification.

Do not invent facts, citations, college policies, marks, or deadlines.

Encourage students to learn rather than submit work
they do not understand.

Keep answers organized and student-friendly.
"""


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/status")
def status():
    configured = bool(API_TOKEN and ACCOUNT_ID)

    return jsonify({
        "configured": configured,
        "model": MODEL_NAME if configured else None
    })


@app.post("/api/chat")
def chat():

    if not API_TOKEN or not ACCOUNT_ID:
        return jsonify({
            "error": "Cloudflare API token or Account ID is missing. Check your .env file."
        }), 503

    data = request.get_json(silent=True) or {}

    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({
            "error": "Please enter a message."
        }), 400

    if len(message) > 5000:
        return jsonify({
            "error": "Message is too long. Keep it under 5,000 characters."
        }), 400

    messages = [
        {
            "role": "system",
            "content": SYSTEM_INSTRUCTION
        }
    ]

    for item in history[-10:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role in ("user", "model") and isinstance(content, str) and content.strip():
            cloudflare_role = "user" if role == "user" else "assistant"

            messages.append({
                "role": cloudflare_role,
                "content": content[:5000]
            })

    messages.append({
        "role": "user",
        "content": message
    })

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1200
            },
            timeout=90
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("success", True):
            raise RuntimeError(str(result.get("errors", "Cloudflare API request failed")))

        answer = result.get("result", {}).get("response", "")
        answer = answer.strip() if isinstance(answer, str) else ""

        if not answer:
            answer = "I couldn't generate a response. Please try again."

        return jsonify({
            "answer": answer
        })

    except requests.exceptions.Timeout:
        app.logger.exception("Cloudflare API timeout")
        return jsonify({
            "error": "The AI request timed out. Please try again."
        }), 504

    except requests.exceptions.RequestException:
        app.logger.exception("Cloudflare API request failed")
        return jsonify({
            "error": "Unable to connect to Cloudflare AI. Check your API settings and try again."
        }), 502

    except Exception:
        app.logger.exception("Cloudflare AI response error")
        return jsonify({
            "error": "Cloudflare AI could not generate a response. Check the server logs."
        }), 502


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
