# 💼 Resume Parser & ATS Evaluator using Gemini API

A full-stack web app to parse PDF resumes, extract structured sections, analyze content using **Google's Gemini API**, and compute an **ATS (Applicant Tracking System) score** — all with a sleek frontend and fast backend.

[![Vercel - Frontend](https://img.shields.io/badge/frontend-vercel-black?logo=vercel)](https://vercel.com)
[![Render - Backend](https://img.shields.io/badge/backend-render-blue?logo=render)](https://render.com)
[![Next.js](https://img.shields.io/badge/Built%20With-Next.js-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

🌐 **Live Project:** [https://resume-ats-zeta.vercel.app](https://resume-ats-zeta.vercel.app)

---

## ✨ Features

- 📄 Upload PDF resumes (only PDF allowed)
- 🧠 Uses **Google Gemini API** to analyze resume content by section
- ✅ Deterministic ATS scoring based on formatting and keyword matches
- 🧾 JSON output from backend, beautifully displayed on frontend
- 🌍 Fully deployed using **Vercel (frontend)** and **Render (backend)**


---

## 📁 Folder Structure

```
resumeATS/
├── client/   # Frontend - Next.js
└── server/   # Backend - FastAPI
```

---

## 🚀 Local Development

### 🖥️ Frontend (Next.js)

```bash
cd client
npm install

# Setup your environment
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8000" > .env.local

# Run the dev server
npm run dev
```

---

### 🧪 Backend (FastAPI + Gemini API)

```bash
cd server
pip install -r req.txt

# Setup your API key
echo "GEMINI_API_KEY=your-gemini-api-key" > .env

# Run backend
uvicorn main:app --reload --port 8000
```

---

## ⚙️ Deployment

### 🔵 Backend on Render

1. Create a new **Web Service**
2. Use your `server/` folder as repo root
3. Set Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. Add environment variable:

```
GEMINI_API_KEY=your-key
```

5. Deploy 🚀

---

### ⚫ Frontend on Vercel

1. Import your repo → Select `client/` as project root
2. Add environment variable:

```
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.onrender.com
```

3. Click **Deploy** ✅

---

## 🛠️ Tech Stack

- **Frontend**: Next.js, React, TailwindCSS
- **Backend**: FastAPI, Python
- **LLM Integration**: Google Gemini API
- **Deployment**: Vercel (client) + Render (server)

---

## 📌 Environment Variables

### Client (`.env.local`)

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Server (`.env`)

```
GEMINI_API_KEY=your-google-gemini-api-key
```

---

## 💡 Future Improvements

- 🔍 Smart keyword matching based on job description
- 📈 Resume improvement recommendations via AI
- 📊 ATS analytics dashboard for recruiters

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🤝 Connect

Made with ❤️ by **Arpit Aggarwal**
