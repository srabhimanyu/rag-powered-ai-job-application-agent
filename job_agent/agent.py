from .config import load_profile
from .database import init_db, upsert_job
from .sources import load_sample_jobs
from .matching import rag_job_analysis

def discover_and_analyse():
    init_db()
    profile = load_profile()
    jobs = load_sample_jobs()
    results = []
    for job in jobs:
        analysis = rag_job_analysis(job, profile)
        upsert_job(job, analysis.get("score", 0), str(analysis))
        results.append((job, analysis))
    return sorted(results, key=lambda x: x[1].get("score", 0), reverse=True)
