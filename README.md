# Indonesia IT & Analytics Job Market — Analisis Pasar Kerja Digital

![Python](https://img.shields.io/badge/Python-3.12-7C3AED)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![pandas](https://img.shields.io/badge/pandas-EDA-150458)
![Data](https://img.shields.io/badge/Data-RIIL%20Bukan%20Sintetis-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Portofolio Data Analyst: analisis **pasar kerja IT & data Indonesia** dari
**data riil** — ~3.500 lowongan diambil dari API publik Kalibrr + LinkedIn
guest API, disaring menjadi **1.630 lowongan relevan** yang mencakup
seluruh ekosistem IT: data/analytics, software engineering, infra/DevOps,
security, QA, IT support, UI/UX, ERP/konsultasi, hingga peran
transformasi/change digital.

> **Bedanya dengan 2 project lain di portfolio ini:** data di sini **bukan
> sintetis** — semua baris adalah lowongan nyata yang diposting perusahaan
> Indonesia. Ini mendemonstrasikan skill yang tidak bisa ditunjukkan data
> buatan: data acquisition, deduplikasi, pembersihan teks tidak rapi,
> normalisasi kategori, dan dokumentasi keterbatasan data secara jujur.

## Pertanyaan bisnis yang dijawab

1. Domain IT mana yang paling besar permintaannya — dan **skill signature**
   apa yang membedakan tiap domain?
2. Skill apa yang **paling sering diminta** — dan kombinasi apa yang sering
   muncul bersamaan?
3. Berapa gaji yang ditawarkan (yang berani menampilkannya), per peran?
4. Di mana lowongan terkonsentrasi — dan seberapa terbuka pasar untuk
   fresh graduate / remote?
5. Industri dan perusahaan mana yang paling aktif merekrut talenta digital?

## Temuan kunci (dihitung via `src/key_metrics.py`)

- **1.630 lowongan relevan** dari ~3.500 hasil fetch dua platform —
  filtering adalah bagian terbesar pekerjaan nyata karena pencarian
  job board itu noisy.
- **Delapan domain pasar:** Software Engineering (29%) terbesar, diikuti
  Data & Analytics (24%), IT Mgmt & Consulting (12%), Infra & Network
  (8%), Security, IT Support, dan UI/UX.
- **Skill teratas:** SQL (36%), Networking (30%), Python (26%),
  API/Integrasi (25%), Excel & Cloud (19%), JIRA & JavaScript (18%).
- **Dua platform = dua segmen pasar berbeda.** LinkedIn membawa ~76%
  lowongan (segmen enterprise/multinasional); Kalibrr ~25% (UMKM/lokal,
  banyak peran MIS/reporting). Komposisi domain per platform berbeda
  signifikan (lihat `outputs/sql_results/14_*`).
- **69% lowongan di DKI Jakarta** → pasar digital Indonesia sangat
  terpusat di ibu kota.
- **Hanya 3% lowongan menampilkan gaji** (median max Rp10 jt/bln) →
  transparansi gaji rendah; analisis gaji bias ke perusahaan transparan.
- **Remote murni ~1%**, hybrid ~3% → masih on-site centric; hanya ~11%
  yang eksplisit fresh-grad friendly; 71% lowongan menargetkan level Mid.

## Struktur

```
├── data/
│   ├── raw/                 JSON mentah hasil fetch API (apa adanya)
│   └── processed/           lowongan.csv + job_skill.csv (bersih)
├── database/
│   ├── jobmarket.db         SQLite — lowongan 1—n job_skill
│   └── queries.sql          14 query analisis
├── dashboard/app.py         Streamlit 5 tab interaktif + filter domain
├── src/
│   ├── fetch_jobs.py        scraper API publik Kalibrr (paginasi+dedup)
│   ├── fetch_linkedin.py    scraper LinkedIn guest API (list + detail)
│   ├── drip_details.py      resume fetch detail LinkedIn (pelan+retry)
│   ├── build_dataset.py     pembersihan, filter relevansi, domain+skill
│   ├── validate_data.py     15 check integritas
│   ├── run_sql_analysis.py  eksekutor queries.sql -> CSV
│   └── key_metrics.py       semua angka dokumen, terhitung otomatis
├── docs/                    sumber, data dictionary, executive report
├── notebooks/               EDA + statistik ter-execute
└── outputs/                 key_metrics.md + hasil query CSV
```

## Cara menjalankan

```bash
pip install -r requirements.txt

# pipeline data (opsional — data/processed sudah ter-commit)
python src/fetch_jobs.py        # Kalibrr — resume-able
python src/fetch_linkedin.py    # LinkedIn — resume-able, ada throttle
python src/drip_details.py      # lanjutkan detail LinkedIn yang pending
python src/build_dataset.py     # bersih + filter + domain + skill -> CSV+DB
python src/validate_data.py     # 15/15 checks
python src/run_sql_analysis.py  # 14 query -> outputs/sql_results/

streamlit run dashboard/app.py  # dashboard
```

## Metodologi & keterbatasan (penting dibaca)

- **Sumber**: endpoint publik `kalibrr.com/kjs/job_board/search` dan
  `linkedin.com/jobs-guest/jobs/api/...` — tanpa auth, delay sopan.
- **Cakupan**: ~76 kata kunci pencarian mencakup seluruh ekosistem IT —
  data/science/BI, software/web/mobile, DevOps/cloud, QA, security,
  UI/UX, ERP/SAP, IT project/change management, network/sysadmin/DBA,
  IT support, hingga smart-city & digital transformation.
- **Filter relevansi**: lowongan dipertahankan jika judulnya match pola
  IT/analyst **atau** deskripsinya menuntut ≥2 skill inti. Peran non-IT
  yang lolos gerbang skill (mis. "Marketing Research") dipisahkan ke
  domain **Adjacent (non-IT)** — dilaporkan jujur, tidak dibuang diam-diam.
- **Klasifikasi**: setiap lowongan mendapat `role_family` (21 keluarga)
  dan `domain` (8 segmen) via aturan regex berjenjang — transparan dan
  reproducible, bukan black-box.
- **Ekstraksi skill**: regex kata kunci atas teks deskripsi (39 skill
  terdeteksi) — bisa meleset pada frasa ambigu.
- **Keterbatasan sumber**: LinkedIn throttling ketat → detail di-fetch
  bertahap (drip + checkpoint); sebagian baris LinkedIn tanpa deskripsi.
  Gaji hanya tersedia di Kalibrr dan hanya ~3% lowongan.
- **Snapshot**: pasar kerja bergerak — dataset ini potret Okt 2026,
  bukan tren historis.
