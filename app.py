
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

client = Groq(api_key=API_KEY) if API_KEY else None

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
    return jsonify({
        "configured": bool(client),
        "model": MODEL_NAME if client else None
    })


@app.post("/api/chat")
def chat():

    if not client:
        return jsonify({
            "error": "Groq API key is missing. Add GROQ_API_KEY to your .env file."
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

        role = item.get("role")
        content = item.get("content")

        if role in ("user", "model") and isinstance(content, str) and content.strip():

            
            groq_role = "user" if role == "user" else "assistant"

            messages.append({
                "role": groq_role,
                "content": content[:5000]
            })

    
    messages.append({
        "role": "user",
        "content": message
    })

    try:

        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1200
        )

        answer = response.choices[0].message.content or ""

        answer = answer.strip()

        if not answer:
            answer = "I couldn't generate a response. Please try again."

        return jsonify({
            "answer": answer
        })

    except Exception:
      app.logger.exception("Groq API request failed")

    return jsonify({
        "error": f"{type(e).__name__}: {str(e)}"
    }), 502
      


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
