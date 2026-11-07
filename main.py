import argparse
from pathlib import Path
from job_agent.database import init_db, list_jobs, record_application, set_job_status, application_history
from job_agent.agent import discover_and_analyse
from job_agent.sources import portal_search_links, load_sample_jobs
from job_agent.config import load_profile
from job_agent.rag import index_document, collection_count
from job_agent.resume import ingest_resume
from job_agent.matching import generate_cover_letter
from job_agent.llm import ollama_available

def main():
    parser = argparse.ArgumentParser(description="Local RAG + LLM Job Application Agent")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("init")
    sub.add_parser("links")
    resume = sub.add_parser("index-resume")
    resume.add_argument("pdf_path")
    job = sub.add_parser("index-job")
    job.add_argument("job_id", help="ID from data/sample_jobs.json")
    sub.add_parser("discover")
    sub.add_parser("list")
    sub.add_parser("review")
    letter = sub.add_parser("cover-letter")
    letter.add_argument("job_id")
    sub.add_parser("history")
    args = parser.parse_args()

    if args.command == "init":
        init_db()
        print("Database initialized.")
    elif args.command == "links":
        p = load_profile()
        for k, v in portal_search_links(p["current_role"], p["preferred_location"]).items():
            print(f"{k}: {v}")
    elif args.command == "index-resume":
        text, chunks = ingest_resume(args.pdf_path)
        print(f"Indexed resume: {len(text)} characters, {chunks} chunks.")
        print(f"Total chunks in vector DB: {collection_count()}")
    elif args.command == "index-job":
        jobs = load_sample_jobs()
        selected = next((j for j in jobs if j.id == args.job_id), None)
        if not selected:
            raise SystemExit("Job ID not found in sample_jobs.json")
        count = index_document(selected.description, f"job-{selected.id}", "job_description",
                               {"job_id": selected.id, "company": selected.company})
        print(f"Indexed {count} job-description chunks.")
    elif args.command == "discover":
        if not ollama_available():
            raise SystemExit("Ollama is not running. Start Ollama and pull the models; see README.")
        for job, analysis in discover_and_analyse():
            print(f"\n{analysis.get('score')}% | {job.company} | {job.title}")
            print(analysis.get("recommendation"))
            print("Matching:", ", ".join(analysis.get("matching_skills", [])))
            print("Gaps:", ", ".join(analysis.get("missing_or_unproven_skills", [])))
    elif args.command == "list":
        for j in list_jobs():
            print(f"{j['id']} | {j['match_score']}% | {j['status']} | {j['company']} | {j['title']}")
    elif args.command == "review":
        for j in list_jobs():
            if j["status"] not in ("NEW", "REVIEW"):
                continue
            print(f"\n{j['company']} | {j['title']} | {j['match_score']}%")
            print(j["url"])
            choice = input("Approve preparation (a), skip (s), quit (q): ").strip().lower()
            if choice == "q": break
            if choice == "a":
                record_application(j["id"], "APPROVED_FOR_PREPARATION",
                                   "User approved preparation; not submitted.")
                print("Approved for document preparation only; not submitted.")
            elif choice == "s":
                set_job_status(j["id"], "SKIPPED")
    elif args.command == "cover-letter":
        jobs = load_sample_jobs()
        selected = next((j for j in jobs if j.id == args.job_id), None)
        if not selected:
            raise SystemExit("Job ID not found in sample_jobs.json")
        output = generate_cover_letter(selected, load_profile())
        Path("output").mkdir(exist_ok=True)
        path = Path("output") / f"cover_letter_{selected.id}.md"
        path.write_text(output, encoding="utf-8")
        print(f"Saved draft to {path}\n\n{output}")
    elif args.command == "history":
        for item in application_history():
            print(item)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
