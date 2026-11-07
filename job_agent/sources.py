"""
Job source adapters.

Naukri and LinkedIn do not offer unrestricted public job-search APIs.
This starter uses search links, manually imported listings, and optional sample data.
Do not scrape logged-in pages or bypass CAPTCHA / access controls.
"""
import csv
import json
import urllib.parse
from pathlib import Path
from .models import Job
from .config import ROOT

def portal_search_links(role="Senior Java Developer", location="India"):
    q = urllib.parse.quote_plus(role)
    loc = urllib.parse.quote_plus(location)
    return {
        "Naukri": f"https://www.naukri.com/{q.replace('+', '-')}-jobs-in-{loc.replace('+', '-')}",
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}"
    }

def load_sample_jobs():
    with (ROOT / "data" / "sample_jobs.json").open("r", encoding="utf-8") as f:
        return [Job(**x) for x in json.load(f)]

def import_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("jobs", [])
    return [Job(**item) for item in data]

def import_csv(path):
    jobs = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["skills"] = [x.strip() for x in row.get("skills", "").split("|") if x.strip()]
            for field in ("experience_min", "experience_max"):
                row[field] = int(row[field]) if row.get(field, "").strip() else None
            jobs.append(Job(**row))
    return jobs
