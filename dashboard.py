import streamlit as st
import pandas as pd
from pathlib import Path
from job_agent.database import init_db, list_jobs, set_job_status, record_application, application_history
from job_agent.agent import discover_and_analyse
from job_agent.sources import portal_search_links
from job_agent.config import load_profile, OLLAMA_CHAT_MODEL, OLLAMA_EMBED_MODEL
from job_agent.llm import ollama_available
from job_agent.resume import ingest_resume
from job_agent.rag import collection_count
from job_agent.matching import generate_cover_letter
from job_agent.sources import load_sample_jobs

st.set_page_config(page_title="RAG Job Agent", page_icon="💼", layout="wide")
init_db()
st.title("💼 RAG + LLM Job Application Agent")
st.caption("Senior Java Developer · India · Local models · Human approval required")

profile = load_profile()
with st.sidebar:
    st.header("Local AI status")
    ok = ollama_available()
    if ok:
       st.success("Ollama connected")
    else:
       st.error("Ollama not detected")
    st.caption(f"Chat model: {OLLAMA_CHAT_MODEL}")
    st.caption(f"Embedding model: {OLLAMA_EMBED_MODEL}")
    st.metric("Indexed vector chunks", collection_count())
    st.divider()
    links = portal_search_links(profile.get("current_role", "Senior Java Developer"),
                                profile.get("preferred_location", "India"))
    st.subheader("Job portal search")
    for label, url in links.items():
        st.markdown(f"[Open {label}]({url})")

tab1, tab2, tab3 = st.tabs(["Discover & match", "Resume RAG", "Application tracker"])

with tab1:
    st.subheader("Discover sample jobs and analyse with RAG + LLM")
    st.caption("Sample job listings are demonstrations, not live vacancies.")
    if st.button("Run RAG + LLM analysis", type="primary", disabled=not ok):
        with st.spinner("Retrieving resume evidence and analysing jobs..."):
            try:
                results = discover_and_analyse()
                st.session_state["latest_results"] = [
                    {"job": j.model_dump(), "analysis": a} for j, a in results
                ]
                st.success(f"Analysed {len(results)} sample jobs.")
            except Exception as e:
                st.error(str(e))
    for item in st.session_state.get("latest_results", []):
        j, a = item["job"], item["analysis"]
        with st.expander(f"{a.get('score', 0)}% · {j['company']} · {j['title']}"):
            st.write(f"**Location:** {j['location']} | **Source:** {j['source']}")
            st.write(f"**Recommendation:** {a.get('recommendation', '')}")
            st.write(f"**Matching skills:** {', '.join(a.get('matching_skills', []))}")
            st.write(f"**Missing/unproven:** {', '.join(a.get('missing_or_unproven_skills', []))}")
            st.write(f"**Experience fit:** {a.get('experience_fit', '')}")
            st.write("**Evidence retrieved from resume:**")
            for ev in a.get("retrieved_evidence", []):
                st.markdown(f"- {ev}")
            if j.get("url"):
                st.markdown(f"[Open job portal]({j['url']})")

with tab2:
    st.subheader("Index your PDF resume into the vector database")
    uploaded = st.file_uploader("Upload resume PDF", type=["pdf"])
    if uploaded and st.button("Index resume with RAG"):
        temp = Path("output") / uploaded.name
        temp.parent.mkdir(exist_ok=True)
        temp.write_bytes(uploaded.getvalue())
        try:
            text, count = ingest_resume(str(temp))
            st.success(f"Indexed {count} chunks from {len(text)} extracted characters.")
            st.info("Resume text is stored in your local Chroma vector database.")
        except Exception as e:
            st.error(str(e))
    st.caption("Scanned PDFs require OCR; this version extracts selectable PDF text.")

with tab3:
    st.subheader("Approval and application tracker")
    jobs = list_jobs()
    if jobs:
        for j in jobs:
            with st.expander(f"{j['match_score']}% · {j['company']} · {j['title']} · {j['status']}"):
                st.write(j["location"])
                if j["url"]:
                    st.markdown(f"[Open listing]({j['url']})")
                if st.button("Approve document preparation", key=f"approve_{j['id']}"):
                    record_application(j["id"], "APPROVED_FOR_PREPARATION",
                                       "User approved preparation; not submitted.")
                    st.rerun()
                if st.button("Skip", key=f"skip_{j['id']}"):
                    set_job_status(j["id"], "SKIPPED")
                    st.rerun()
                if st.button("Generate cover letter draft", key=f"letter_{j['id']}", disabled=not ok):
                    sample = next((x for x in load_sample_jobs() if x.id == j["id"]), None)
                    if sample:
                        with st.spinner("Generating a grounded draft..."):
                            draft = generate_cover_letter(sample, profile)
                        st.text_area("Review and edit before use", draft, height=250,
                                     key=f"draft_{j['id']}")
    else:
        st.info("No analysed jobs yet. Run analysis in the first tab.")
    st.markdown("**Approval history**")
    hist = application_history()
    if hist:
        st.dataframe(pd.DataFrame(hist), use_container_width=True)
    else:
        st.caption("No approvals yet.")

st.warning("This tool does not submit applications, log in to job portals, or bypass platform protections. Every application must be reviewed and submitted by you.")
