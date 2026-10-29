"""Ambil lowongan riil dari LinkedIn guest API (publik, tanpa auth).

Dua tahap:
1. Search list -> id, judul, perusahaan, lokasi, tanggal posting
2. Job detail -> deskripsi, seniority, employment type, industri, fungsi

Output: data/raw/linkedin_jobs_raw.json
Sopan: delay antar request; stop kalau di-throttle.
"""
import json
import re
import time
from pathlib import Path

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"}
SEARCH = ("https://www.linkedin.com/jobs-guest/jobs/api/"
          "seeMoreJobPostings/search")
DETAIL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}"
QUERIES = ["data analyst", "business analyst", "data scientist",
           "business intelligence", "data engineer", "analytics",
           "MIS analyst", "system analyst", "reporting analyst",
           "software engineer", "web developer", "frontend",
           "backend", "fullstack", "mobile developer",
           "devops", "qa engineer", "it support", "ui ux",
           "security engineer", "erp consultant", "it project manager",
           "network engineer", "system administrator", "database administrator"]
PER_PAGE, MAX_PAGES = 10, 10            # s.d. 100 per kata kunci

TITLE_RE = re.compile(r'base-search-card__title[^>]*>\s*([^<]+)')
COMP_RE = re.compile(r'base-search-card__subtitle[^>]*>.*?<a[^>]*>([^<]+)', re.S)
LOC_RE = re.compile(r'job-search-card__location[^>]*>\s*([^<]+)')
ID_RE = re.compile(r'data-entity-urn="urn:li:jobPosting:(\d+)"')
DATE_RE = re.compile(r'datetime="([^"]+)"')


def get(url, **kw):
    r = requests.get(url, headers=UA, timeout=30, **kw)
    if r.status_code == 429:
        raise RuntimeError("rate-limited 429")
    r.raise_for_status()
    return r.text


def parse_detail(jid):
    h = get(DETAIL.format(jid))
    desc = re.search(r'description__text[^>]*>(.*?)</div>', h, re.S)
    crit = dict(re.findall(
        r'criteria[^>]*>.*?<span[^>]*>([^<]+)</span>.*?<span[^>]*>([^<]+)</span>',
        h, re.S))
    return {"description_html": desc.group(1) if desc else "",
            "criteria": crit}


def main():
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    out = "data/raw/linkedin_jobs_raw.json"
    jobs, seen = {}, set()
    if Path(out).exists():
        for j in json.load(open(out, encoding="utf-8")):
            seen.add(j["id"]); jobs[j["id"]] = j

    for q in QUERIES:
        got = 0
        for p in range(MAX_PAGES):
            try:
                h = get(SEARCH, params={"keywords": q,
                                        "location": "Indonesia",
                                        "start": p * PER_PAGE})
            except Exception as e:
                print(f"{q} p{p}: stop ({e})"); break
            ids = ID_RE.findall(h)
            if not ids:
                break
            titles = TITLE_RE.findall(h)
            comps = COMP_RE.findall(h)
            locs = LOC_RE.findall(h)
            dates = DATE_RE.findall(h)
            for i, jid in enumerate(ids):
                if jid in seen:
                    continue
                seen.add(jid)
                jobs[jid] = {
                    "id": jid, "_query": q,
                    "name": titles[i].strip() if i < len(titles) else "",
                    "company": re.sub(r"\s+", " ",
                        comps[i]).strip() if i < len(comps) else "",
                    "location": locs[i].strip() if i < len(locs) else "",
                    "listed_date": dates[i] if i < len(dates) else "",
                    "detail_fetched": False}
                got += 1
            time.sleep(0.8)
        print(f"{q}: +{got} lowongan baru (total {len(jobs)})")
    json.dump(list(jobs.values()), open(out, "w", encoding="utf-8"),
              ensure_ascii=False)

    # --- tahap 2: detail ---
    pending = [j for j in jobs.values() if not j.get("detail_fetched")]
    print(f"fetch detail: {len(pending)} lowongan")
    ok = 0
    for j in pending:
        try:
            j.update(parse_detail(j["id"]))
            j["detail_fetched"] = True
            ok += 1
        except Exception as e:
            print(f"detail {j['id']}: {e} — stop tahap detail")
            break
        if ok % 50 == 0:
            print(f"  {ok}/{len(pending)}")
            json.dump(list(jobs.values()), open(out, "w", encoding="utf-8"),
                      ensure_ascii=False)   # checkpoint
        time.sleep(0.7)
    json.dump(list(jobs.values()), open(out, "w", encoding="utf-8"),
              ensure_ascii=False)
    print(f"detail OK: {ok}, total unik: {len(jobs)} -> {out}")


if __name__ == "__main__":
    main()
