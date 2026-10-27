"""Bersihkan JSON mentah Kalibrr -> tabel analitis + SQLite.

Output:
  data/processed/lowongan.csv     1 baris per lowongan
  data/processed/job_skill.csv    long format: id_lowongan x skill (1--n)
  database/jobmarket.db           kedua tabel di atas

Catatan metodologi (dokumentasikan di DATA_DICTIONARY):
- work_experience & education_level = kode enum Kalibrr -> dipetakan ke label
  (pemetaan terbaik-upaya, dicatat sebagai asumsi).
- Skill diekstrak dari teks deskripsi+kualifikasi via regex kata kunci —
  bukan NLP berat; trade-off sengaja: transparan & reproducible.
"""
import html
import json
import re
import sqlite3
from pathlib import Path

import pandas as pd

RAW = "data/raw/kalibrr_jobs_raw.json"
RAW_LI = "data/raw/linkedin_jobs_raw.json"

# Pemetaan lokasi LinkedIn ("Kota, Provinsi, Indonesia") -> (kota, provinsi)
LI_PROV = {
    "jakarta": ("Jakarta", "DKI Jakarta"),
    "jakarta metropolitan area": ("Jakarta", "DKI Jakarta"),
    "tangerang": ("Tangerang", "Banten"),
    "south tangerang": ("Tangerang Selatan", "Banten"),
    "bekasi": ("Bekasi", "Jawa Barat"),
    "bandung": ("Bandung", "Jawa Barat"),
    "west java": ("", "Jawa Barat"),
    "central java": ("", "Jawa Tengah"),
    "semarang": ("Semarang", "Jawa Tengah"),
    "east java": ("", "Jawa Timur"),
    "surabaya": ("Surabaya", "Jawa Timur"),
    "yogyakarta": ("Yogyakarta", "DI Yogyakarta"),
    "banten": ("", "Banten"),
    "bali": ("", "Bali"),
    "denpasar": ("Denpasar", "Bali"),
    "medan": ("Medan", "Sumatera Utara"),
    "north sumatra": ("Medan", "Sumatera Utara"),
    "makassar": ("Makassar", "Sulawesi Selatan"),
    "palembang": ("Palembang", "Sumatera Selatan"),
    "batam": ("Batam", "Kepulauan Riau"),
    "bandar lampung": ("Bandar Lampung", "Lampung"),
    "balikpapan": ("Balikpapan", "Kalimantan Timur"),
}
LI_TIPE = {"full-time": "Full time", "contract": "Contractual",
           "part-time": "Part time", "internship": "Internship",
           "temporary": "Contractual", "other": "Full time",
           "volunteer": "Freelance"}
LI_SEN = {"entry level": "Junior / Entry", "associate": "Junior / Entry",
          "mid-senior level": "Mid", "director": "Senior / Lead",
          "executive": "Senior / Lead", "internship": "Junior / Entry",
          "not applicable": "Mid"}

EXP_MAP = {100: "Fresh / <1 thn", 200: "1–3 thn", 300: "3–5 thn",
           400: "5–10 thn", 500: ">10 thn"}
EDU_MAP = {200: "SMA/SMK", 350: "D1–D3", 400: "D3", 450: "D3/D4",
           500: "S1", 550: "S1", 600: "S2", 650: "S2/S3"}

# Keluarga peran dari judul — urutan penting (pola spesifik dulu)
ROLE_RULES = [
    ("Data Scientist", r"data\s*scien|machine learning|\bml\b engineer"),
    ("Data Engineer", r"data\s*engineer|data platform|data pipeline|\betl\b developer|big data"),
    ("BI / Analytics", r"business intelligence|\bbi\b analyst|analytics engineer|data insight"),
    ("Data Analyst", r"data\s*analyst|analis\s*data|data quality|big data analyst|data officer|data governance|data protection|people analytics"),
    ("Business / System Analyst", r"business analyst|analis\s*bisnis|system analyst|it ba\b|\bit business\b|odoo analyst"),
    ("Risk & Credit Analyst", r"credit analyst|risk analyst|analis\s*(kredit|risiko)"),
    ("Ops & Domain Analyst", r"operations? analyst|claim analyst|pricing analyst|hr analyst|talent.*analyst|hc.*analyst|governance.*analyst|category.*analyst|business development.*analyst|procurement.*analyst|supply chain.*analyst|quality.*analyst|performance analyst"),
    ("MIS / Reporting", r"\bmis\b|management information|reporting|data admin|data management|data processing|kpi|performance reporting|data insight"),
    ("Product Analyst", r"product analyst"),
    ("Marketing Analyst", r"marketing analyst|marketing.*analyst|digital marketing|performance marketing"),
    ("Financial Analyst", r"financial analyst|financ.*analyst|accounting analyst|tax analyst"),
]
TITLE_RELEVANT = re.compile(
    r"analyst|analis|analytic|data|intelligence|scientist|\bbi\b|\betl\b|"
    r"\bmis\b|reporting|dashboard|kpi|analisa",
    re.I)
CORE_SKILLS = {"SQL", "Python", "R", "Excel", "Power BI", "Tableau",
               "Looker / Data Studio", "BigQuery", "Statistik",
               "Visualisasi Data", "Google Sheets", "ETL / Data Pipeline"}
SENIOR_RE = re.compile(r"senior|\bsr\b|lead|head|manager|supervisor|principal|chief", re.I)
JUNIOR_RE = re.compile(r"junior|\bjr\b|fresh|intern|magang|trainee|entry", re.I)

SKILLS = {
    "SQL": r"\bsql\b|mysql|postgresql|postgres|sqlite|t-sql|sql server",
    "Python": r"\bpython\b|pandas|numpy|scikit",
    "R": r"\br studio\b|\brlang\b|\bbahasa r\b|\br programming\b",
    "Excel": r"\bexcel\b|spreadsheet|vlookup|pivot table",
    "Google Sheets": r"google sheets|google workspace|gsheet",
    "Power BI": r"power\s*bi|powerbi",
    "Tableau": r"\btableau\b",
    "Looker / Data Studio": r"looker|data studio",
    "BigQuery": r"bigquery|big query",
    "Cloud (AWS/GCP/Azure)": r"\baws\b|google cloud|\bgcp\b|azure",
    "Spark / Hadoop": r"\bspark\b|hadoop|hive",
    "Airflow / Orchestrasi": r"airflow|orchestrat",
    "ETL / Data Pipeline": r"\betl\b|data pipeline|data integration",
    "Statistik": r"statistic|statistik|hipotesis|a/b testing|inferensia",
    "Machine Learning": r"machine learning|\bml\b|deep learning|modeling prediktif",
    "Visualisasi Data": r"visualisasi|data viz|dashboarding|dashboard",
    "Storytelling / Presentasi": r"storytell|presentasi|presentation skill|komunikasi",
    "dbt": r"\bdbt\b",
    "Git": r"\bgit\b|github|version control",
    "SPSS / SAS": r"\bspss\b|\bsas\b",
    "JIRA / Agile": r"\bjira\b|agile|scrum",
    "NoSQL / MongoDB": r"mongodb|nosql",
    "ERP / SAP": r"\berp\b|\bsap\b|odoo",
}


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", html.unescape(s))
    s = s.replace("�", "-")                    # karakter rusak encoding
    return re.sub(r"\s+", " ", s).strip()


def classify_role(title):
    t = title.lower()
    for fam, pat in ROLE_RULES:
        if re.search(pat, t):
            return fam
    return "Analyst Lainnya"


def classify_seniority(title, exp_code):
    if JUNIOR_RE.search(title):
        return "Junior / Entry"
    if SENIOR_RE.search(title):
        return "Senior / Lead"
    return {100: "Junior / Entry", 200: "Mid", 300: "Mid",
            400: "Senior / Lead", 500: "Senior / Lead"}.get(exp_code, "Mid")


def extract_skills(text):
    return [s for s, pat in SKILLS.items() if re.search(pat, text, re.I)]


def norm_prov(s):
    """'West Java (Jawa Barat)' -> 'Jawa Barat'; 'Daerah Khusus Ibukota
    Jakarta' -> 'DKI Jakarta'."""
    if not s or not isinstance(s, str):
        return s
    m = re.search(r"\(([^)]+)\)", s)
    s = m.group(1).strip() if m else s.strip()
    return {"Daerah Khusus Ibukota Jakarta": "DKI Jakarta",
            "Jakarta": "DKI Jakarta"}.get(s, s)


def parse_li_loc(loc):
    """'Jakarta, Jakarta, Indonesia' -> (kota, provinsi)."""
    if not loc:
        return None, None
    parts = [p.strip() for p in loc.split(",") if p.strip()]
    for p in parts:
        if p.lower() in LI_PROV:
            kota, prov = LI_PROV[p.lower()]
            return kota or (parts[0] if parts[0].lower() != "indonesia"
                            else None), prov
    if len(parts) >= 2 and parts[-1].lower() == "indonesia":
        return parts[0], parts[-2]
    return parts[0], None


def kalibrr_rows(jobs):
    rows, skill_rows = [], []
    for j in jobs:
        loc = (j.get("google_location") or {}).get("address_components") or {}
        teks = strip_html((j.get("description") or "") + " " +
                          (j.get("qualifications") or ""))
        title = j.get("name") or ""
        exp = j.get("work_experience")
        gaji_min, gaji_max = j.get("salary_lower"), j.get("maximum_salary")
        if j.get("salary_interval") not in ("month", None):
            gaji_min = gaji_max = None
        if (j.get("salary_currency") or "IDR") != "IDR":
            gaji_min = gaji_max = None
        skills = extract_skills(teks)
        judul_match = bool(TITLE_RELEVANT.search(title))
        n_core = len(CORE_SKILLS & set(skills))
        if not judul_match and n_core < 2:
            continue                     # buang lowongan tak relevan
        rows.append({
            "id_lowongan": f"kb_{j['id']}",
            "sumber": "kalibrr",
            "judul": strip_html(title),
            "peran_analyst": judul_match,
            "role_family": classify_role(title),
            "senioritas": classify_seniority(title, exp),
            "perusahaan": j.get("company_name") or
                (j.get("company") or {}).get("name"),
            "industri": (j.get("company") or {}).get("industry"),
            "fungsi": j.get("function"),
            "kota": loc.get("city"),
            "provinsi": norm_prov(loc.get("region")),
            "tipe": j.get("tenure"),
            "remote": bool(j.get("is_work_from_home")),
            "hybrid": bool(j.get("is_hybrid")),
            "fresh_grad_ok": bool(j.get("is_open_to_fresh_grads")),
            "pengalaman": EXP_MAP.get(exp, str(exp)),
            "pendidikan": EDU_MAP.get(j.get("education_level"), "Lainnya"),
            "gaji_min_jt": round(gaji_min / 1e6, 1) if gaji_min else None,
            "gaji_max_jt": round(gaji_max / 1e6, 1) if gaji_max else None,
            "tgl_posting": (j.get("activation_date") or "")[:10],
            "tgl_tutup": (j.get("application_end_date") or "")[:10],
            "teks": teks[:4000],
        })
        for s in skills:
            skill_rows.append({"id_lowongan": f"kb_{j['id']}", "skill": s})
    return rows, skill_rows


def linkedin_rows(jobs):
    rows, skill_rows = [], []
    for j in jobs:
        teks = strip_html(j.get("description_html") or "")
        title = j.get("name") or ""
        skills = extract_skills(teks)
        judul_match = bool(TITLE_RELEVANT.search(title))
        n_core = len(CORE_SKILLS & set(skills))
        if not judul_match and n_core < 2:
            continue
        kota, prov = parse_li_loc(j.get("location"))
        crit = j.get("criteria") or {}
        lid = f"li_{j['id']}"
        remote = bool(re.search(r"remote", j.get("location") or "", re.I))
        rows.append({
            "id_lowongan": lid,
            "sumber": "linkedin",
            "judul": strip_html(title),
            "peran_analyst": judul_match,
            "role_family": classify_role(title),
            "senioritas": LI_SEN.get(
                (crit.get("Seniority level") or "").lower(),
                classify_seniority(title, 200)),
            "perusahaan": j.get("company"),
            "industri": crit.get("Industries"),
            "fungsi": crit.get("Job function"),
            "kota": kota,
            "provinsi": norm_prov(prov),
            "tipe": LI_TIPE.get(
                (crit.get("Employment type") or "").lower(), "Full time"),
            "remote": remote,
            "hybrid": bool(re.search(r"hybrid", j.get("location") or "", re.I)),
            "fresh_grad_ok": "intern" in title.lower() or
                "fresh" in teks.lower(),
            "pengalaman": crit.get("Seniority level") or "—",
            "pendidikan": None,
            "gaji_min_jt": None,
            "gaji_max_jt": None,
            "tgl_posting": j.get("listed_date") or "",
            "tgl_tutup": "",
            "teks": teks[:4000],
        })
        for s in skills:
            skill_rows.append({"id_lowongan": lid, "skill": s})
    return rows, skill_rows


def main():
    jobs = json.load(open(RAW, encoding="utf-8"))
    rows, skill_rows = kalibrr_rows(jobs)
    if Path(RAW_LI).exists():
        li = json.load(open(RAW_LI, encoding="utf-8"))
        r2, s2 = linkedin_rows(li)
        rows += r2
        skill_rows += s2
    lv = pd.DataFrame(rows)
    sk = pd.DataFrame(skill_rows, columns=["id_lowongan", "skill"])
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("database").mkdir(exist_ok=True)
    lv.to_csv("data/processed/lowongan.csv", index=False)
    sk.to_csv("data/processed/job_skill.csv", index=False)

    con = sqlite3.connect("database/jobmarket.db")
    lv.drop(columns=["teks"]).to_sql("lowongan", con, if_exists="replace",
                                     index=False)
    sk.to_sql("job_skill", con, if_exists="replace", index=False)
    con.executescript("""
        CREATE INDEX IF NOT EXISTS ix_lv_role ON lowongan(role_family);
        CREATE INDEX IF NOT EXISTS ix_lv_prov ON lowongan(provinsi);
        CREATE INDEX IF NOT EXISTS ix_skill ON job_skill(skill);
    """)
    con.commit()
    con.close()
    print(f"lowongan: {len(lv)} | job_skill: {len(sk)} | "
          f"ada gaji: {lv.gaji_max_jt.notna().sum()}")
    print(lv.sumber.value_counts().to_dict())


if __name__ == "__main__":
    main()
