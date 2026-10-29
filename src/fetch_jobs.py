"""Ambil data lowongan riil dari public API Kalibrr (Indonesia).

Endpoint job board publik — tanpa auth. Diambil untuk beberapa kata kunci
terkait data/analytics, dipaginasi, lalu di-dedup berdasarkan id lowongan.

Output: data/raw/kalibrr_jobs_raw.json
"""
import json
import time
from pathlib import Path

import requests

BASE = "https://www.kalibrr.com/kjs/job_board/search"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-research)"}

QUERIES = [
    "data analyst", "business analyst", "data scientist",
    "business intelligence", "data engineer", "analytics",
    "data quality", "product analyst", "marketing analyst",
    "financial analyst", "analyst", "analis", "reporting analyst",
    "operations analyst", "risk analyst", "research analyst",
    "credit analyst", "system analyst", "sql", "tableau",
    "power bi", "excel analyst", "supply chain analyst",
    "hr analyst", "procurement analyst", "pricing analyst",
    "mis analyst", "mis staff", "mis officer",
    "management information", "reporting", "dashboard",
    "data administrator", "data admin", "staff data",
    "analisa data", "kpi", "performance reporting",
    "big data", "data processing", "data management",
    "junior analyst", "senior analyst", "market research",
    "insight analyst", "digital analyst", "growth analyst",
    "people analytics", "web analyst", "finance analyst",
    "data support", "staf data", "report analyst",
    "quality assurance analyst", "revenue analyst",
    "data officer", "data specialist", "analytics manager",
    "bi developer", "bi engineer", "reporting specialist",
    "insight", "database analyst", "quantitative analyst",
    "strategy analyst", "business data", "data analyst intern",
    "bi analyst", "analytics", "big data analyst",
    # --- segmen IT umum ---
    "software engineer", "web developer", "frontend developer",
    "backend developer", "fullstack developer", "mobile developer",
    "android developer", "ios developer", "flutter",
    "devops", "site reliability", "system administrator",
    "network engineer", "it support", "helpdesk",
    "qa engineer", "quality assurance", "software tester",
    "security engineer", "cyber security", "ui ux",
    "it project manager", "erp consultant", "sap consultant",
    "sistem informasi", "it auditor", "database administrator",
    "cloud engineer", "infrastructure engineer", "it consultant",
    "solution architect", "technical support", "it officer",
    "programmer", "software developer", "golang", "python developer",
]
PER_PAGE, MAX_PAGES = 50, 20          # maks 1000 lowongan per kata kunci


def fetch(query, offset):
    r = requests.get(BASE, headers=HEADERS, timeout=30, params={
        "text": query, "country": "Indonesia",
        "limit": PER_PAGE, "offset": offset})
    r.raise_for_status()
    return r.json()


def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    all_jobs, seen = {}, set()
    raw_path = "data/raw/kalibrr_jobs_raw.json"
    if Path(raw_path).exists():          # append: pertahankan hasil fetch lama
        for j in json.load(open(raw_path, encoding="utf-8")):
            seen.add(j["id"])
            all_jobs[j["id"]] = j
    for q in QUERIES:
        got = 0
        for page in range(MAX_PAGES):
            try:
                d = fetch(q, page * PER_PAGE)
            except Exception as e:
                print(f"{q} page {page}: gagal ({e})")
                break
            jobs = d.get("jobs", [])
            if not jobs:
                break
            for j in jobs:
                jid = j.get("id")
                if jid and jid not in seen:
                    seen.add(jid)
                    j["_query"] = q
                    all_jobs[jid] = j
                    got += 1
            time.sleep(0.6)             # sopan: jangan spam endpoint
        print(f"{q}: +{got} lowongan baru")
    out = "data/raw/kalibrr_jobs_raw.json"
    json.dump(list(all_jobs.values()), open(out, "w", encoding="utf-8"),
              ensure_ascii=False)
    print(f"TOTAL unik: {len(all_jobs)} -> {out}")


if __name__ == "__main__":
    main()
