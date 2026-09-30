<div align="center">

# 🔍 Reality Check

### AI Content Authenticity Analyzer

[![Live Site](https://img.shields.io/badge/Live%20Site-reality--check-00d4b4?style=for-the-badge&logo=render&logoColor=white)](https://reality-check-rxqu.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Upload any image. Know the truth in seconds.**

[Live Demo](https://reality-check-rxqu.onrender.com) · [Report a Bug](https://github.com/Aylin-Urumi/ai-content-detector/issues) · [Request a Feature](https://github.com/Aylin-Urumi/ai-content-detector/issues)

![Reality Check Screenshot](https://reality-check-rxqu.onrender.com)

</div>

---

## 🧠 What is Reality Check?

Reality Check is a web application that analyzes images and determines whether they are **AI-generated or real**, returning a confidence score and a plain-language explanation of the result.

As AI image generation becomes indistinguishable from real photography, tools like this matter. Reality Check was built to make authenticity detection fast, accessible, and free — no sign-up, no friction, just upload and know.

---

## ✨ Features

- 🖼️ **Instant image analysis** — results in seconds, not minutes
- 📊 **Confidence score** — clear percentage showing AI vs real likelihood
- 🧾 **Plain-language explanation** — no technical jargon, just the truth
- 🔒 **Privacy first** — uploaded images are deleted immediately after analysis
- ⚡ **Rate limiting** — 5 free analyses per day per visitor, with a live visual counter
- 🌙 **Dark UI** — clean, minimal design optimized for trust and readability
- 📈 **Global counter** — tracks total images analyzed across all users

---

## 🏗️ Architecture

```
User uploads image
       │
       ▼
Flask backend (app.py)
       │
       ├── Rate limiter checks IP (flask-limiter, 5/day)
       │
       ├── File validated (extension, size)
       │
       ├── Image sent to Sightengine AI API
       │        └── Returns ai_generated score (0.0 – 1.0)
       │
       ├── Score mapped to confidence % + explanation
       │
       ├── Global counter incremented (counter.txt)
       │
       └── Result rendered (result.html)
```

**Two-layer rate limiting:**
- **Frontend:** localStorage tracks daily usage per browser, shows a live countdown bar
- **Backend:** flask-limiter enforces hard 5/day limit per IP — cannot be bypassed by clearing browser data

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Detection Engine | [Sightengine AI API](https://sightengine.com) |
| Rate Limiting | flask-limiter (per IP) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Deployment | Render (free tier) |
| Uptime | UptimeRobot (keep-alive pings every 5 min) |
| Analytics | Google Analytics (GA4) |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.9+
- A free [Sightengine](https://sightengine.com) account (500 free checks/month)

### Setup

```bash
# Clone the repo
git clone https://github.com/Aylin-Urumi/ai-content-detector.git
cd ai-content-detector

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SIGHTENGINE_USER=your_user
export SIGHTENGINE_SECRET=your_secret

# Run
python3 app.py
```

Then visit `http://localhost:5000` in your browser.

### Environment Variables

| Variable | Where to find it |
|---|---|
| `SIGHTENGINE_USER` | [Sightengine dashboard](https://dashboard.sightengine.com) → API credentials |
| `SIGHTENGINE_SECRET` | [Sightengine dashboard](https://dashboard.sightengine.com) → API credentials |

---

## 📁 Project Structure

```
ai-content-detector/
├── app.py                  # Flask app, routes, rate limiting, API calls
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── counter.txt             # Persistent global analysis counter
├── templates/
│   ├── index.html          # Homepage with upload form + live usage counter
│   ├── result.html         # Image analysis result page
│   ├── about.html          # About page
│   └── error.html          # Error handling page
└── uploads/                # Temp folder — images deleted after analysis
```

---

## 🔐 Privacy & Security

- Uploaded images are **never stored** — they are deleted from the server immediately after analysis
- No user accounts, no cookies, no personal data collected
- Rate limiting protects against abuse and API quota exhaustion
- All environment variables (API keys) are stored securely via Render's environment config — never in code

---

## 🗺️ Roadmap

- [ ] Support for video analysis
- [ ] Drag and drop with image preview before submitting
- [ ] URL-based image submission (no upload needed)
- [ ] API endpoint for developers
- [ ] Upgrade to paid Sightengine plan for higher volume

---

## 👩‍💻 About the Author

Built by [Aylin](https://linkedin.com/in/aylin-urumi-5784b1387) — Software Engineering student at Fırat University, Turkey.

---

<div align="center">
  <sub>If you found this useful, consider giving it a ⭐ on GitHub!</sub>
</div>