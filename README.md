# 📄 Resume Parser Service

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000?logo=flask)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT_4.1-412991?logo=openai)](https://platform.openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

**A lightweight Flask microservice** that parses resumes, extracts structured insights, and powers AI‑driven candidate filtering for the [Career Navigator](https://github.com/Yaso-Moha/ai-career-navigator) platform.

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📥 **Multi‑file Upload** | Accepts single PDF/DOCX files or bulk ZIP uploads of resumes |
| 📖 **Text Extraction** | Extracts raw text from PDFs using `pdfminer.six` & `PyPDF2`, and from DOCX using `mammoth` |
| 🔍 **AI Filtering** | Natural‑language query filtering — describe what you're looking for and get matching filenames (powered by OpenAI GPT‑4.1‑mini) |
| 🧠 **Smart Parsing** | Cleans, normalizes, and structures extracted text for downstream processing |
| 📎 **File Serving** | Serves uploaded resume files for preview/download |
| 🌐 **CORS Enabled** | Ready to accept requests from any frontend origin |

---

## 🏗️ Architecture

```
POST /upload-resumes         →  Upload PDFs or ZIP, returns { parsed_resumes: [...] }
POST /filter-parsed-resumes  →  AI filtering of parsed resumes by query
POST /extract-cv-text        →  Extract text from a single PDF or DOCX file
GET  /resume-file/<filename> →  Serve an uploaded resume file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- An **OpenAI API key** ([get one here](https://platform.openai.com/api-keys))

### 1. Clone the repository

```bash
git clone https://github.com/Yaso-Moha/resume_parser_service.git
cd resume_parser_service
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
# Or create a .env file:
echo 'OPENAI_API_KEY=sk-...' > .env
```

### 4. Run the service

```bash
python3 resume_parser_service.py
```

The API will be available at **http://localhost:5001**

> ⚠️ This service is designed to work alongside the [Career Navigator frontend](https://github.com/Yaso-Moha/ai-career-navigator). Make sure both are running for the full experience.

---

## 📡 API Endpoints

### `POST /upload-resumes`

Upload one or more PDF files (or a ZIP containing PDFs) for text extraction.

```bash
curl -X POST -F "files=@resume.pdf" http://localhost:5001/upload-resumes
```

**Response:**
```json
{
  "parsed_resumes": [
    {
      "filename": "resume.pdf",
      "full_text": "John Doe\nSoftware Engineer...",
      "snippet": "John Doe\nSoftware Engineer..."
    }
  ]
}
```

---

### `POST /filter-parsed-resumes`

Filter a batch of parsed resumes using a natural‑language query. The AI matches candidates against all constraints in the query.

```bash
curl -X POST http://localhost:5001/filter-parsed-resumes \
  -H "Content-Type: application/json" \
  -d '{
    "filter_query": "has 3+ years of Python experience and speaks Arabic",
    "parsed_resumes": [ ... ]
  }'
```

**Response:**
```json
{
  "matches": ["candidate_1.pdf", "candidate_5.pdf"]
}
```

---

### `POST /extract-cv-text`

Extract plain text from a single PDF or DOCX file. Useful for quick parsing without batch processing.

```bash
curl -X POST -F "file=@cv.pdf" http://localhost:5001/extract-cv-text
```

**Response:**
```json
{
  "text": "Extracted text content..."
}
```

---

### `GET /resume-file/<filename>`

Serve an uploaded resume file for viewing or download.

```bash
curl http://localhost:5001/resume-file/resume.pdf
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Flask 3.0 |
| **CORS** | Flask‑CORS |
| **PDF Parsing** | pdfminer.six, PyPDF2 |
| **DOCX Parsing** | mammoth |
| **AI / Filtering** | OpenAI SDK (GPT‑4.1‑mini) |
| **File Handling** | python‑multipart, tempfile |
| **Config** | python‑dotenv (`.env` support) |

---

## 📦 Dependencies

```
Flask>=2.0
python-multipart
openai>=0.27.0
pdfminer.six>=20201018
python-dateutil>=2.8.1
```

Install with: `pip install -r requirements.txt`

---

## 🔗 Frontend

This service is the backend for the **Career Navigator** web application:

👉 [**github.com/Yaso-Moha/ai-career-navigator**](https://github.com/Yaso-Moha/ai-career-navigator)

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/Yaso-Moha">Yaso-Moha</a>
</div>