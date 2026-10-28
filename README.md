# Indonesia Analytics Job Market — Analisis Lowongan Data Analyst

![Python](https://img.shields.io/badge/Python-3.12-7C3AED)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![pandas](https://img.shields.io/badge/pandas-EDA-150458)
![Data](https://img.shields.io/badge/Data-RIIL%20Bukan%20Sintetis-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

Portofolio Data Analyst: analisis **pasar kerja analitik Indonesia** dari
**data riil** — 2.110 lowongan diambil dari API publik Kalibrr + LinkedIn
guest API, disaring menjadi **465 lowongan relevan** untuk profil data
analyst, lalu diekstrak skill, gaji, lokasi, dan pola perekrutannya.

> **Bedanya dengan 2 project lain di portfolio ini:** data di sini **bukan
> sintetis** — semua baris adalah lowongan nyata yang diposting perusahaan
> Indonesia. Ini mendemonstrasikan skill yang tidak bisa ditunjukkan data
> buatan: data acquisition, deduplikasi, pembersihan teks tidak rapi,
> normalisasi kategori, dan dokumentasi keterbatasan data secara jujur.

## Pertanyaan bisnis yang dijawab

1. Skill apa yang **paling sering diminta** perusahaan — dan kombinasi skill
   apa yang paling sering muncul bersamaan?
2. Berapa gaji yang ditawarkan (yang berani menampilkannya), per peran?
3. Di mana lowongan terkonsentrasi — dan seberapa terbuka pasar untuk
   fresh graduate / remote?
4. Industri dan perusahaan mana yang paling aktif merekrut profil analitik?

## Temuan kunci (dihitung via `src/key_metrics.py`)

- **465 lowongan relevan** dari 2.110 hasil fetch dua platform — hanya
  **~22% hasil pencarian yang benar-benar relevan** → job board search
  itu noisy; filtering adalah bagian terbesar pekerjaan nyata.
- **Dua platform = dua segmen pasar berbeda.** Kalibrr: Excel 60%,
  SQL 41% (UMKM/lokal). LinkedIn: SQL 66%, Python 53%, Power BI 34%
  (enterprise/tech). Jawaban "skill apa yang diminta" bergantung
  platform tempat mencari — temuan sampling yang penting.
- **79% lowongan di DKI Jakarta** → pasar analitik sangat terpusat di
  ibu kota; peluang regional masih tipis.
- **Hanya 4% lowongan menampilkan gaji** (median max Rp10,5 jt/bln) →
  transparansi gaji rendah; analisis gaji bias ke perusahaan transparan.
- **Remote murni ~1%**, hybrid ~6% → pasar analitik Indonesia masih
  on-site centric; hanya ~12% yang eksplisit fresh-grad friendly.

## Struktur

```
├── data/
│   ├── raw/                 JSON mentah hasil fetch API (apa adanya)
│   └── processed/           lowongan.csv + job_skill.csv (bersih)
├── database/
│   ├── jobmarket.db         SQLite — lowongan 1—n job_skill
│   └── queries.sql          12 query analisis
├── dashboard/app.py         Streamlit 5 tab interaktif
├── src/
│   ├── fetch_jobs.py        scraper API publik Kalibrr (paginasi+dedup)
│   ├── fetch_linkedin.py    scraper LinkedIn guest API (list + detail)
│   ├── build_dataset.py     pembersihan, filter relevansi, ekstraksi skill
│   ├── validate_data.py     15 check integritas
│   ├── run_sql_analysis.py  eksekutor queries.sql -> CSV
│   └── key_metrics.py       semua angka dokumen, terhitung otomatis
├── docs/                    sumber, data dictionary, executive report
├── notebooks/               EDA ter-execute
└── outputs/                 key_metrics.md + hasil query CSV
```

## Cara menjalankan

```bash
pip install -r requirements.txt

# pipeline data (opsional — data/processed sudah ter-commit)
python src/fetch_jobs.py        # Kalibrr — resume-able
python src/fetch_linkedin.py    # LinkedIn — resume-able, ada throttle
python src/build_dataset.py     # bersih + filter + ekstrak skill -> CSV+DB
python src/validate_data.py     # 15/15 checks
python src/run_sql_analysis.py  # 12 query -> outputs/sql_results/

streamlit run dashboard/app.py  # dashboard
```

## Metodologi & keterbatasan (penting dibaca)

- **Sumber**: endpoint publik `kalibrr.com/kjs/job_board/search` dan
  `linkedin.com/jobs-guest/jobs/api/...` — tanpa auth, delay sopan.
- **Filter relevansi**: lowongan dipertahankan jika judulnya mengandung
  pola analyst/data/MIS **atau** deskripsinya menuntut ≥2 skill analitik
  inti (SQL, Python, Excel, BI, statistik, dst.). Kolom `peran_analyst`
  memisahkan keduanya.
- **Ekstraksi skill**: regex kata kunci atas teks deskripsi — transparan
  dan reproducible, tapi bisa meleset pada frasa ambigu ("R" sebagai huruf).
- **Keterbatasan sumber**: LinkedIn throttling ketat → sebagian besar
  baris LinkedIn tanpa deskripsi, sehingga analisis skill dominan
  berbasis Kalibrr. Gaji hanya tersedia di Kalibrr dan hanya ~6% lowongan.
- **Snapshot**: pasar kerja bergerak — dataset ini potret Okt 2026,
  bukan tren historis.
