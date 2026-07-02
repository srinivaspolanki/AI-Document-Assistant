# 🧠 AI Document Assistant

An AI-powered document analysis application built with **Python**, **Streamlit**, and **Ollama**. Analyze different document types locally using Large Language Models (LLMs) without sending your data to external cloud services.

---

## 📌 Features

- 📄 Analyze Meeting Notes
- 📚 Analyze Research Papers
- 📄 Analyze Resumes
- 🎓 Analyze Statements of Purpose (SOP)
- 📝 Analyze Assignments
- 📂 Analyze General Documents

### 📁 Supported File Types

- TXT
- PDF
- DOCX

### 🤖 AI Features

- Document Summarization
- Key Decision Extraction
- Action Item Detection
- Follow-up Email Generation
- AI Suggestions
- Resume Analysis
- Research Paper Analysis
- Dynamic Prompt Generation

### 📤 Export Options

- PDF
- Microsoft Word (.docx)
- Markdown (.md)

### 📊 Additional Features

- Local AI using Ollama
- Multiple LLM support
- Meeting History
- Dashboard Statistics
- Dynamic Document Parsing
- Offline Processing

---

# 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### AI

- Ollama
- Gemma 3
- Qwen
- Llama 2

### Document Processing

- PyPDF
- python-docx

### Export

- ReportLab
- python-docx

---

# 📂 Project Structure

```text
AI-Document-Assistant/
│
├── app.py
├── utils.py
├── pdf_export.py
├── doc_export.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── history/
│
├── sample_files/
│
├── screenshots/
│
└── venv/ (ignored)
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Document-Assistant.git
```

Go to the project

```bash
cd AI-Document-Assistant
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Download Ollama

https://ollama.com/

Install a model

```bash
ollama pull gemma3:4b
```

or

```bash
ollama pull qwen3.5:0.8b
```

Start Ollama

```bash
ollama serve
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---


# 📄 Sample Documents

Example documents are available inside

```
sample_files/
```

including

- Meeting Notes
- Resume
- Statement of Purpose

---

# 🎯 Future Improvements

- React + FastAPI Version
- Drag & Drop Upload
- Automatic Document Type Detection
- AI Chat with Uploaded Documents
- Multi-language Support
- Cloud Deployment
- OCR for Scanned PDFs
- RAG-based Document Question Answering

---
