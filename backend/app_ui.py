import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ResuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617 0%, #071827 55%, #0f172a 100%);
    color: white;
}

[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(148,163,184,0.18);
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.logo {
    font-size: 26px;
    font-weight: 900;
    color: #ffffff;
}

.plan {
    font-size: 12px;
    letter-spacing: 3px;
    color: #94a3b8;
    margin-bottom: 35px;
}

.hero {
    padding: 64px;
    border-radius: 28px;
    background: radial-gradient(circle at top, rgba(99,102,241,0.35), rgba(15,23,42,0.9));
    border: 1px solid rgba(148,163,184,0.18);
    text-align: center;
    margin-bottom: 34px;
}

.hero-title {
    font-size: 56px;
    font-weight: 950;
    color: white;
}

.hero-sub {
    font-size: 18px;
    color: #cbd5e1;
    max-width: 760px;
    margin: auto;
}

.section-title {
    font-size: 30px;
    font-weight: 850;
    margin: 28px 0 18px 0;
}

.card {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 22px;
    padding: 26px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.28);
    margin-bottom: 22px;
}

.metric-card {
    background: #0b1726;
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 22px;
    padding: 28px;
    min-height: 190px;
}

.metric-label {
    color: #cbd5e1;
    letter-spacing: 3px;
    font-size: 14px;
}

.metric-value {
    font-size: 54px;
    font-weight: 950;
    color: white;
    margin-top: 25px;
}

.feature-card {
    background: #071625;
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 20px;
    padding: 24px;
    min-height: 180px;
}

.feature-icon {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #6366f1, #22d3ee);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 18px;
    font-size: 22px;
}

.feature-title {
    font-size: 20px;
    font-weight: 800;
    color: white;
    margin-bottom: 8px;
}

.feature-text {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(99,102,241,0.18);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 14px;
}

.skill-pill {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.35);
    color: #86efac;
    border-radius: 999px;
    font-size: 14px;
}

.missing-pill {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    color: #fca5a5;
    border-radius: 999px;
    font-size: 14px;
}

.chat-user {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 12px 0;
}

.chat-bot {
    background: #0b1726;
    border: 1px solid rgba(148,163,184,0.18);
    color: white;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 12px 0;
}

.stButton button {
    background: linear-gradient(90deg, #818cf8, #6366f1);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 800;
    padding: 0.65rem 1.2rem;
}

.stTextArea textarea, .stTextInput input {
    background: #07111f !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(148,163,184,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "data" not in st.session_state:
    st.session_state.data = None

if "upload_type" not in st.session_state:
    st.session_state.upload_type = "Resume Analysis"

if "chat" not in st.session_state:
    st.session_state.chat = []

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = None


# Sidebar
st.sidebar.markdown("<div class='logo'>ResuMind AI</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='plan'>PREMIUM PLAN</div>", unsafe_allow_html=True)

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"
    st.rerun()

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.page = "dashboard"
    st.rerun()

if st.sidebar.button("💬 AI Chat", use_container_width=True):
    st.session_state.page = "chat"
    st.rerun()

if st.sidebar.button("🎯 Job Matcher", use_container_width=True):
    st.session_state.page = "job"
    st.rerun()

if st.sidebar.button("🧠 Blackbox AI", use_container_width=True):
    st.session_state.page = "blackbox"
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("⬆️ Upload New File", use_container_width=True):
    st.session_state.page = "dashboard"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("❔ Help Center")
st.sidebar.caption("↪ Logout")

# Home Page
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div class="badge">⚡ NEXT-GEN DOCUMENT INTELLIGENCE</div>
        <div class="hero-title">ResuMind AI</div>
        <br>
        <div class="hero-sub">
            AI-powered resume and document intelligence platform. Analyze resumes,
            extract insights from reports, match jobs, and chat with documents using local RAG.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Intelligent Capabilities</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Resume Intelligence</div>
            <div class="feature-text">
                Extract candidate details, skills, projects, education, score resumes,
                generate AI feedback, and match resumes with job descriptions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Document / Report Intelligence</div>
            <div class="feature-text">
                Upload PDFs, DOCX, or PPTX reports and extract text, headings, tables,
                key-value pairs, and searchable document chunks.
            </div>
        </div>
        """, unsafe_allow_html=True)

    c3, c4, c5 = st.columns(3)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Chat with Files</div>
            <div class="feature-text">
                Ask natural questions about uploaded resumes or documents and get grounded answers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Job Matching</div>
            <div class="feature-text">
                Compare resumes with job descriptions and identify matched and missing skills.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Semantic Search</div>
            <div class="feature-text">
                Search beyond keywords using embeddings, Qdrant vector database, and RAG retrieval.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Get Started Now", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()


# Dashboard Page
if st.session_state.page == "dashboard":
    st.markdown("<div class='section-title'>Dashboard Overview</div>", unsafe_allow_html=True)

    upload_type = st.radio(
        "Choose analysis mode",
        ["Resume Analysis", "Document / Report Analysis"],
        horizontal=True
    )

    if upload_type == "Resume Analysis":
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx", "pptx"],
            key="resume_upload"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload Document / Report",
            type=["pdf", "docx", "pptx"],
            key="document_upload"
        )

    if uploaded_file:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        progress = st.progress(0)
        status = st.empty()

        status.info("Step 1/4: Uploading file...")
        progress.progress(20)

        status.info("Step 2/4: Extracting text and structure...")
        progress.progress(45)

        status.info("Step 3/4: Creating embeddings and storing chunks...")
        progress.progress(70)

        res = requests.post(f"{API_URL}/upload", files=files)

        progress.progress(100)

        if res.status_code == 200:
            st.session_state.data = res.json()
            st.session_state.upload_type = upload_type
            st.session_state.ai_feedback = None
            st.session_state.chat = []
            status.success("Step 4/4: Processing complete ✅")
        else:
            status.error("Upload failed. Check FastAPI backend.")

    data = st.session_state.data
    current_type = st.session_state.get("upload_type", "Resume Analysis")

    if data:
        if current_type == "Resume Analysis":
            analysis = data.get("resume_analysis", {})
            intel = data.get("resume_intelligence", {})
            score = analysis.get("score", 0)

            m1, m2, m3 = st.columns(3)

            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RESUME SCORE</div>
                    <div class="metric-value">{score}<span style="font-size:24px;color:#94a3b8;"> /100</span></div>
                </div>
                """, unsafe_allow_html=True)

            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">TOTAL WORDS</div>
                    <div class="metric-value">{data.get("total_words", 0)}</div>
                    <p style="color:#94a3b8;">Ideal range: 450 - 600 words</p>
                </div>
                """, unsafe_allow_html=True)

            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">PAGE COUNT</div>
                    <div class="metric-value">{data.get("total_pages", 0)}</div>
                    <p style="color:#94a3b8;">Perfect for resume review</p>
                </div>
                """, unsafe_allow_html=True)

            st.progress(score / 100)

            left, right = st.columns([2, 1])

            with left:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                tabs = st.tabs(["Analysis", "AI Feedback", "Profile"])

                with tabs[0]:
                    st.subheader("Detailed Analysis")
                    st.write("Your resume has been analyzed for ATS readiness, technical density, and recruiter clarity.")

                    c1, c2 = st.columns(2)

                    with c1:
                        st.markdown("#### ✅ Top Strengths")
                        for s in analysis.get("strengths", []):
                            st.success(s)

                    with c2:
                        st.markdown("#### 📈 Growth Areas")
                        feedback = analysis.get("feedback", [])
                        if feedback:
                            for f in feedback:
                                st.warning(f)
                        else:
                            st.success("No major issues detected.")

                with tabs[1]:
                    st.subheader("AI Recruiter Feedback")

                    if st.button("⚡ Generate AI Feedback", use_container_width=True):
                        with st.spinner("Generating AI recruiter feedback..."):
                            feedback_res = requests.get(f"{API_URL}/ai-feedback")

                        if feedback_res.status_code == 200:
                            st.session_state.ai_feedback = feedback_res.json().get("feedback")
                        else:
                            st.error("Failed to generate AI feedback.")

                    if st.session_state.ai_feedback:
                        st.write(st.session_state.ai_feedback)
                    else:
                        st.info("Click the button to generate AI feedback.")

                with tabs[2]:
                    st.subheader("Candidate Profile")
                    st.write(f"**Name:** {intel.get('name', 'Not found')}")
                    st.write(f"**Location:** {intel.get('location', 'Not found')}")
                    st.write(f"**Email:** {intel.get('email', 'Not found')}")
                    st.write(f"**Phone:** {intel.get('phone', 'Not found')}")
                    st.write(f"**LinkedIn:** {intel.get('linkedin', 'Not found')}")

                st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("🛠 Skills")
                skills = intel.get("skills", [])
                if skills:
                    for s in skills:
                        st.markdown(f"<span class='skill-pill'>{s}</span>", unsafe_allow_html=True)
                else:
                    st.info("No skills found.")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("🚀 Projects")
                projects = intel.get("projects", [])
                if projects:
                    for p in projects:
                        st.write(f"• {p}")
                else:
                    st.info("No projects found.")
                st.markdown("</div>", unsafe_allow_html=True)

            report = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": data.get("filename"),
                "type": "resume",
                "resume_score": score,
                "candidate_profile": intel,
                "resume_analysis": analysis,
                "ai_feedback": st.session_state.ai_feedback or ""
            }

            st.download_button(
                "⬇️ Download Resume Report",
                data=json.dumps(report, indent=4),
                file_name="resume_analysis_report.json",
                mime="application/json"
            )

        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📄 Document Overview")

            c1, c2, c3 = st.columns(3)
            c1.metric("Words", data.get("total_words", 0))
            c2.metric("Pages", data.get("total_pages", 0))
            c3.metric("Vector Chunks", data.get("stored_chunks", 0))

            st.markdown("</div>", unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs([
                "Text Preview",
                "Headings",
                "Tables",
                "Key-Value Pairs"
            ])

            with tab1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📝 Extracted Text Preview")
                st.write(data.get("extracted_text_preview", "No preview available."))
                st.markdown("</div>", unsafe_allow_html=True)

            with tab2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📌 Headings")
                st.json(data.get("headings", []))
                st.markdown("</div>", unsafe_allow_html=True)

            with tab3:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📊 Tables")
                st.json(data.get("tables", []))
                st.markdown("</div>", unsafe_allow_html=True)

            with tab4:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("🔑 Key Value Pairs")
                st.json(data.get("key_value_pairs", {}))
                st.markdown("</div>", unsafe_allow_html=True)

            doc_report = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": data.get("filename"),
                "type": "document",
                "total_words": data.get("total_words"),
                "total_pages": data.get("total_pages"),
                "headings": data.get("headings", []),
                "tables": data.get("tables", []),
                "key_value_pairs": data.get("key_value_pairs", {}),
                "preview": data.get("extracted_text_preview", "")
            }

            st.download_button(
                "⬇️ Download Document Extraction Report",
                data=json.dumps(doc_report, indent=4),
                file_name="document_extraction_report.json",
                mime="application/json"
            )


# Chat Page
if st.session_state.page == "chat":
    st.markdown("<div class='section-title'>AI Chat</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    chat_label = "Ask your uploaded file anything"
    if st.session_state.get("upload_type") == "Resume Analysis":
        chat_label = "Ask your resume anything"
    elif st.session_state.get("upload_type") == "Document / Report Analysis":
        chat_label = "Ask your document/report anything"

    query = st.text_input(chat_label)

    if st.button("Send", use_container_width=True):
        if query.strip():
            with st.spinner("Thinking..."):
                res = requests.get(f"{API_URL}/search", params={"query": query})

            if res.status_code == 200:
                result = res.json()
                st.session_state.chat.append((
                    query,
                    result.get("answer", ""),
                    result.get("confidence", 0),
                    result.get("citations", [])
                ))
            else:
                st.error("Search failed.")
        else:
            st.warning("Enter a question first.")

    for q, a, conf, cites in reversed(st.session_state.chat):
        st.markdown(f"<div class='chat-user'>🧑 {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bot'>🤖 {a}</div>", unsafe_allow_html=True)
        st.caption(f"Confidence: {conf}")

        with st.expander("📚 Sources"):
            if cites:
                for c in cites:
                    st.write(f"📄 {c.get('source')} | Chunk {c.get('chunk')} | Score {c.get('score')}")
            else:
                st.write("No citations available.")

    st.markdown("</div>", unsafe_allow_html=True)


# Job Matcher Page
if st.session_state.page == "job":
    st.markdown("<div class='section-title'>Job Match Analysis</div>", unsafe_allow_html=True)

    if st.session_state.get("upload_type") != "Resume Analysis":
        st.warning("Job Matcher works best after uploading a resume in Resume Analysis mode.")

    st.write("Paste a job description below to see how well your resume aligns with the role requirements.")

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        jd = st.text_area(
            "JOB DESCRIPTION CONTENT",
            height=340,
            placeholder="Paste the full job description here..."
        )

        if st.button("⚡ Analyze Match", use_container_width=True):
            if jd.strip():
                with st.spinner("Matching resume with job description..."):
                    res = requests.post(f"{API_URL}/match-job", params={"job_description": jd})

                if res.status_code == 200:
                    st.session_state.job_match = res.json()
                else:
                    st.error("Job match failed.")
            else:
                st.warning("Paste a job description first.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        match = st.session_state.get("job_match")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if match:
            score = match.get("match_score", 0)
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="font-size:54px;font-weight:950;color:white;">{score}%</div>
                <div style="color:#67e8f9;font-weight:800;">MATCH SCORE</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score / 100)
        else:
            st.markdown("""
            <div style="text-align:center;">
                <div style="font-size:54px;font-weight:950;color:white;">--%</div>
                <div style="color:#94a3b8;">Upload resume and analyze job description</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if match:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("⚠️ Missing Skills")
            for s in match.get("missing_skills", []):
                st.markdown(f"<span class='missing-pill'>{s}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ✅ OUTSIDE (correct placement)
# -------------------------------
# Blackbox AI Page
if st.session_state.page == "blackbox":
    st.markdown("<div class='section-title'>🧠 Blackbox AI</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Ask general questions using your local AI model.")

    user_input = st.text_area(
        "Ask anything...",
        height=180,
        placeholder="Example: Explain RAG in simple words"
    )

    if st.button("Generate Answer", use_container_width=True):
        if user_input.strip():
            with st.spinner("Blackbox AI is thinking..."):
                res = requests.post(
                    f"{API_URL}/blackbox-ai",
                    params={"prompt": user_input}
                )

            if res.status_code == 200:
                answer = res.json().get("answer", "")
                st.markdown(f"<div class='chat-bot'>🤖 {answer}</div>", unsafe_allow_html=True)
            else:
                st.error("Blackbox AI failed. Check backend.")
        else:
            st.warning("Enter a prompt first.")

    st.markdown("</div>", unsafe_allow_html=True)