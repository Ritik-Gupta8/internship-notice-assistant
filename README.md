# 🎓 Internship Notice Assistant

> **Turn messy placement notices into instant action plans — powered by Google Gemini AI**

![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-42b883?style=flat&logo=vuedotjs)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat&logo=google)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)

---

## ✨ What It Does

Paste any internship/job notice text **or upload a screenshot** of it, and the AI instantly generates:

| Output | Description |
|---|---|
| 📋 **Opportunity Snapshot** | Company, Role, Deadline, Stipend — in a clean table |
| ✅ **Eligibility Criteria** | Parsed and formatted, with key requirements bolded |
| 📁 **Documents Checklist** | Checkbox list of everything you need to apply |
| 📧 **Ready-to-Send Email** | A complete, professional application email draft |
| ⚡ **Smart Action Tips** | 4 specific tips to maximize your application chances |

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask |
| **Frontend** | Vue.js 3 (CDN), Vanilla CSS |
| **AI Engine** | Google Gemini 2.0 Flash (multimodal) |
| **Markdown** | Marked.js (CDN) |
| **Environment** | python-dotenv |

---

## 📁 Project Structure

```
internship-notice-assistant/
├── app.py               # Flask backend + Gemini API integration
├── requirements.txt     # Python dependencies
├── .env                 # API key 
├── README.md            # This file
├── templates/
│   └── index.html       # Vue.js frontend (single file)
└── venv/                # Python virtual environment
```

---

## ⚙️ Setup & Installation

### 1. Clone / navigate to project

```bash
cd internship-notice-assistant
```

### 2. Create & activate virtual environment

```bash
# Create
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Google API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free API key at: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Run the app

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🎯 Features

### 📝 Text Input
- Paste any internship/placement notice text directly
- Works with notices in any format (email, PDF copy, WhatsApp message, etc.)

### 📸 Screenshot Upload *(New Feature)*
- Upload a screenshot of the notice (JPG, PNG, WebP, GIF)
- Supports **drag-and-drop** or click-to-browse
- Gemini Vision extracts the text AND analyzes it — no manual copying needed

### 🤖 Prompt Engineering
The AI uses a carefully engineered system prompt that:
- Forces consistent, structured Markdown output
- Produces a formatted table for quick scanning
- Generates document checklists with actual checkboxes
- Creates personalized email drafts (not generic templates)
- Gives role-specific action tips (not generic career advice)

---

## 🔑 API Reference

### `POST /api/analyze`

**Request body (JSON):**
```json
{
  "notice_text": "optional text of the notice",
  "image_base64": "optional base64-encoded image string",
  "mime_type": "image/png"
}
```

**Response (success):**
```json
{
  "result": "## 📋 Opportunity Snapshot\n..."
}
```

**Response (error):**
```json
{
  "error": "Please paste a notice or upload a screenshot."
}
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `GOOGLE_API_KEY not set` | Create `.env` file with your key |
| `Module not found` | Run `pip install -r requirements.txt` in activated venv |
| `Port 5000 in use` | Change port in `app.py`: `app.run(port=5001)` |
| Image upload not working | Ensure the file is a valid image (JPG/PNG/WebP) |
| API quota exceeded | Wait a few minutes or use a different API key |

---

## 👤 Author

Built as part of an internship assistant project.  
Powered by **Google Gemini AI** and **Flask + Vue.js**.

---

## 📄 License

MIT License — free to use and modify.