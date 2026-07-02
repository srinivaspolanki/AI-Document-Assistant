import streamlit as st
import ollama
import time
from pypdf import PdfReader
import os
from datetime import datetime
from doc_export import create_docx
from pdf_export import create_pdf
from docx import Document

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Documents Analyzer",
    page_icon="https://img.icons8.com/color/96/artificial-intelligence.png",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    max-width:1200px;
}

/* ---------- Title ---------- */

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#2563eb;
}

.sub-title{
    text-align:center;
    color:#6b7280;
    font-size:18px;
    margin-bottom:30px;
}

/* ---------- Metrics ---------- */

div[data-testid="stMetric"]{
    background:#ffffff;
    border-radius:15px;
    padding:18px;
    border:1px solid #d1d5db;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

/* ---------- Metric Labels ---------- */

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] p,
div[data-testid="stMetric"] div:first-child {
    color: #1f2937 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* ---------- Metric Values ---------- */

div[data-testid="stMetric"] div[data-testid="stMetricValue"]{
    color:#111827 !important;
    font-size:28px !important;
    font-weight:700 !important;
}

/* ---------- Buttons ---------- */

div.stButton > button{
    width:100%;
    height:55px;
    font-size:18px;
    font-weight:bold;
    border-radius:12px;
}

/* ---------- Expander ---------- */

div[data-testid="stExpander"]{
    border-radius:12px;
    border:1px solid #d1d5db;
    margin-bottom:12px;
}

/* ---------- Text Area ---------- */

textarea{
    font-size:16px !important;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    border-right:1px solid #e5e7eb;
}

/* ---------- Success ---------- */

div[data-testid="stAlert"]{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://img.icons8.com/color/96/artificial-intelligence.png",
    width=80
)

st.sidebar.title("Settings")

document_type = st.sidebar.selectbox(
    "📂 Document Type",
    [
        "Meeting Notes",
        "Research Paper",
        "Resume",
        "Statement of Purpose",
        "Assignment",
        "General Document",
        "Custom"
    ]
)

model = st.sidebar.selectbox(
    "AI Model",
    [
        "gemma3:4b",
        "llama2:latest",
        "qwen3.5:0.8b"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("📂 Meeting History")

history_files = []
if os.path.exists("history"):
    history_files = sorted(os.listdir("history"), reverse=True)

for file in history_files[:10]:
    st.sidebar.caption(file)

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.3, 0.1)

# ---------------- TITLE ----------------
col1,col2,col3,col4=st.columns(4)

col1.info("📄 PDF")
col2.info("📘 DOCX")
col3.info("📝 TXT")
col4.info("🤖 Local AI")
st.markdown("""
<div class="main-title">
AI Document Assistant
</div>

<div class="sub-title">
Analyze PDFs, Word Documents, Meeting Notes, Research Papers and Resumes using Local AI (Ollama)
</div>
""", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📂 Upload Document",
    type=["txt", "pdf", "docx"],
    help="Supported formats: TXT, PDF, DOCX"
)

meeting_notes = ""

if uploaded_file is not None:

    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):

        meeting_notes = uploaded_file.read().decode("utf-8")

        st.success("✅ TXT loaded successfully!")

    elif filename.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        meeting_notes = text

        st.success("✅ PDF loaded successfully!")

    elif filename.endswith(".docx"):

        document = Document(uploaded_file)

        meeting_notes = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        st.success("✅ Word document loaded successfully!")

else:

    meeting_notes = st.text_area(
        "Or Paste Document",
        height=250
    )

# ---------------- STATS ----------------

if meeting_notes:
    words = len(meeting_notes.split())
    chars = len(meeting_notes)
    lines = len(meeting_notes.splitlines())

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Words", words)
    c2.metric("Characters", chars)
    c3.metric("Lines", lines)
    c4.metric("Reading", f"{max(1, words // 200)} min")
    c5.metric("Speaking", f"{max(1, words // 130)} min")


def get_prompt(document_type, content):

    prompts = {

        "Meeting Notes": f"""
You are an expert meeting assistant.

Analyze these meeting notes.

Return exactly:

## Meeting Overview
## Summary
## Key Decisions
## Action Items
## Follow-up Email
## AI Suggestions

Meeting Notes:

{content}
""",

        "Research Paper": f"""
You are an AI research assistant.

Analyze this research paper.

Return exactly:

## Summary
## Research Problem
## Methodology
## Key Findings
## Limitations
## Future Work

Paper:

{content}
""",

        "Resume": f"""
You are an HR recruiter.

Analyze this resume.

Return exactly:

## Professional Summary
## Strengths
## Weaknesses
## Missing Skills
## Resume Score
## Suggestions

Resume:

{content}
""",

        "Statement of Purpose": f"""
You are an admissions committee member.

Analyze this Statement of Purpose.

Return exactly:

## Summary
## Strengths
## Weaknesses
## Grammar Issues
## Suggestions

Statement:

{content}
""",

        "Assignment": f"""
Analyze this assignment.

Return exactly:

## Summary
## Important Concepts
## Key Points
## Suggestions

Assignment:

{content}
""",

        "General Document": f"""
Analyze this document.

Return exactly:

## Summary
## Important Points
## Keywords
## Recommendations

Document:

{content}
""",

        "Custom": f"""
Analyze this document.

Return a professional structured response.

Document:

{content}
"""
    }

    return prompts[document_type]


def parse_sections(result_text):
    """Split the model's markdown output into {heading: content} sections."""
    sections = {}
    current_heading = None

    for line in result_text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("##"):
            current_heading = line.replace("##", "").strip()
            sections[current_heading] = ""
            continue

        if current_heading:
            sections[current_heading] += line + "\n"

    return sections


ICONS = {
    "Meeting Overview": "📋",
    "Summary": "📄",
    "Key Decisions": "✅",
    "Action Items": "📌",
    "Follow-up Email": "📧",
    "AI Suggestions": "💡",
    "Research Problem": "🔬",
    "Methodology": "⚙️",
    "Key Findings": "📊",
    "Limitations": "⚠️",
    "Future Work": "🚀",
    "Professional Summary": "👨‍💼",
    "Strengths": "💪",
    "Weaknesses": "❌",
    "Missing Skills": "🎯",
    "Resume Score": "🏆",
    "Grammar Issues": "✍️",
    "Important Concepts": "📘",
    "Important Points": "📌",
    "Keywords": "🏷️",
    "Recommendations": "⭐"
}

# ---------------- SESSION STATE ----------------

if "sections" not in st.session_state:
    st.session_state.sections = None
if "report" not in st.session_state:
    st.session_state.report = None
if "history_saved" not in st.session_state:
    st.session_state.history_saved = False

# ---------------- GENERATE BUTTON ----------------

if st.button("🚀 Analyze Document", use_container_width=True):

    if meeting_notes.strip() == "":
        st.warning("Please enter meeting notes.")
        st.stop()

    prompt = get_prompt(document_type, meeting_notes)

    start = time.time()

    with st.spinner("🤖 AI is generating your meeting report..."):
        try:
            response = ollama.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": temperature,
                    "num_predict": 700
                }
            )

            message = response["message"]
            result = message.get("content", "")

            if not result:
                result = message.get("thinking", "")

        except Exception as e:
            st.error("""
## ❌ AI Generation Failed

Possible reasons:

- Ollama is not running.
- The selected model is not installed.
- GPU memory is full.
- The model crashed.

Please check your Ollama installation and try again.
""")

            with st.expander("Technical Details"):
                st.code(str(e))

            st.stop()

    end = time.time()
    st.success(
        f"✅ Analysis completed successfully in {end-start:.2f} seconds"
    )
    st.balloons()

    # Parse into sections and build the report
    sections = parse_sections(result)

    if not sections:
        # Model didn't follow the "##" format — fall back to raw output
        sections = {"Result": result}

    report = ""
    for heading, content in sections.items():
        report += f"# {heading}\n\n{content}\n\n"

    # Persist across reruns (e.g. when download buttons are clicked)
    st.session_state.sections = sections
    st.session_state.report = report
    st.session_state.history_saved = False  # allow saving this new result

# ---------------- DISPLAY SECTIONS + DOWNLOADS ----------------
# Runs on every rerun as long as we have a generated report in session_state,
# so download buttons keep working after the initial click.

if st.session_state.sections:

    st.divider()

    for heading, content in st.session_state.sections.items():
        icon = ICONS.get(heading, "📄")
        with st.expander(f"{icon} {heading}", expanded=True):
            st.markdown(content)

    # ---------------- SAVE HISTORY (once per generated result) ----------------

    if not st.session_state.history_saved:
        os.makedirs("history", exist_ok=True)
        filename = datetime.now().strftime("history/meeting_%Y-%m-%d_%H-%M-%S.md")

        with open(filename, "w", encoding="utf-8") as file:
            file.write(st.session_state.report)

        st.session_state.history_saved = True

    # ---------------- DOWNLOADS ----------------

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📄 Download Markdown",
            data=st.session_state.report,
            file_name="meeting_notes.md",
            mime="text/markdown"
        )

    with col2:
        pdf = create_pdf(st.session_state.report)
        st.download_button(
            label="📕 Download PDF",
            data=pdf,
            file_name="meeting_notes.pdf",
            mime="application/pdf"
        )

    with col3:
        word = create_docx(st.session_state.report)
        st.download_button(
            label="📘 Download Word",
            data=word,
            file_name="meeting_notes.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
st.divider()

st.caption(
    "Built with ❤️ using Python • Streamlit • Ollama • Local LLMs"
)