import os
import base64
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ─── Setup ────────────────────────────────────────────────────────────────────
load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in .env file")

client = genai.Client(api_key=GOOGLE_API_KEY)

# ─── Engineered System Prompt ─────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an elite university career placement counselor and application coach with 15+ years of experience helping students land competitive internships at top companies.

A student has shared an internship or job posting notice with you (either as text or an image screenshot). Your job is to analyze it thoroughly and produce a detailed, structured student-friendly action plan.

STRICT OUTPUT FORMAT (use exactly these Markdown headers):

## 📋 Opportunity Snapshot
Create a table with the following fields (fill in "Not mentioned" if info is missing):
| Field | Details |
|---|---|
| 🏢 Company / Organization | ... |
| 💼 Role / Position | ... |
| 📍 Location / Mode | ... |
| 🗓️ Application Deadline | ... |
| 💰 Stipend / Salary | ... |
| ⏳ Duration | ... |

## ✅ Eligibility Criteria
List all eligibility conditions as bullet points. If years/CGPA/skills are mentioned, bold them. If none stated, write "Open to all — verify with the company."

## 📁 Required Documents Checklist
List each document as a checkbox item:
- [ ] Resume / CV
- [ ] ... (add others from the notice)

## 📧 Ready-to-Send Application Email
Write a complete, professional email. Include:
- A compelling subject line
- Formal greeting
- A strong opening hook (1 sentence about why you want THIS specific role)
- 2-3 sentences showing relevant skills/experience
- Mention of attached documents
- Professional closing

Format it exactly like this:
**Subject:** [Subject line here]

**Body:**
[Full email body here]

## ⚡ Smart Action Tips
Give exactly 4 personalized, specific tips for THIS role/company to maximize the student's chances. Make them actionable and specific — not generic advice.

---
IMPORTANT RULES:
- If given an image, extract ALL text from it first, then analyze
- Use the EXACT Markdown headers above — do not change them
- Be specific and practical — avoid generic filler advice
- If the notice is in another language, respond in English
"""


def analyze_with_gemini(notice_text: str = None, image_base64: str = None, mime_type: str = None):
    """Call Gemini with text and/or image input using the new google.genai SDK."""

    contents = []

    if image_base64:
        # Inline image part
        image_bytes = base64.b64decode(image_base64)
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type or "image/png"
            )
        )
        contents.append(
            types.Part.from_text(
                text="Please extract all text from this notice image and then analyze it as described in your instructions."
            )
        )

    if notice_text and notice_text.strip():
        contents.append(
            types.Part.from_text(
                text=f"Here is the internship/job notice text to analyze:\n\n{notice_text.strip()}"
            )
        )

    if not contents:
        raise ValueError("No input provided — please paste text or upload a screenshot.")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.4,
            max_output_tokens=2048,
        )
    )

    return response.text


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts JSON body:
      { "notice_text": "...", "image_base64": "...", "mime_type": "image/png" }
    Returns:
      { "result": "... markdown string ..." }
    """
    try:
        data = request.get_json(force=True)
        notice_text  = data.get("notice_text", "").strip()
        image_base64 = data.get("image_base64", None)
        mime_type    = data.get("mime_type", "image/png")

        if not notice_text and not image_base64:
            return jsonify({"error": "Please paste a notice or upload a screenshot."}), 400

        result = analyze_with_gemini(
            notice_text=notice_text if notice_text else None,
            image_base64=image_base64 if image_base64 else None,
            mime_type=mime_type
        )
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)