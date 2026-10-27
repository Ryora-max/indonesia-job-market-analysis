# Data Dictionary — Job Market Indonesia

Dua tabel relasional: `lowongan` 1—n `job_skill`.

## `lowongan` (1 baris = 1 lowongan)

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id_lowongan` | str | `kb_<id>` (Kalibrr) / `li_<id>` (LinkedIn) — PK |
| `sumber` | str | `kalibrr` / `linkedin` |
| `judul` | str | Judul lowongan (dibersihkan dari karakter rusak) |
| `peran_analyst` | bool | True jika judul match pola analyst/data/MIS |
| `role_family` | str | Data Analyst · Data Scientist · Data Engineer · BI/Analytics · Business/System Analyst · MIS/Reporting · Risk & Credit · Ops & Domain · Product · Marketing · Financial · Analyst Lainnya |
| `senioritas` | str | `Junior / Entry` · `Mid` · `Senior / Lead` — dari judul + kode pengalaman (Kalibrr) atau kriteria LinkedIn |
| `perusahaan` | str | Nama perusahaan |
| `industri` | str | Industri perusahaan (Kalibrr) / criteria LinkedIn |
| `fungsi` | str | Job function kategori platform |
| `kota` / `provinsi` | str | Lokasi — provinsi dinormalisasi ("West Java (Jawa Barat)" → "Jawa Barat") |
| `tipe` | str | Full time · Contractual · Part time · Freelance · Internship |
| `remote` / `hybrid` / `fresh_grad_ok` | bool | Flag dari platform / teks |
| `pengalaman` | str | Label level pengalaman (Kalibrr enum dipetakan; LinkedIn criteria) |
| `pendidikan` | str | Level pendidikan (Kalibrr enum dipetakan; LinkedIn: null) |
| `gaji_min_jt` / `gaji_max_jt` | float | Rp juta/bulan — hanya Kalibrr, mayoritas null |
| `tgl_posting` / `tgl_tutup` | str | Tanggal aktivasi / deadline (ISO) |
| `teks` | str | Deskripsi+kualifikasi bersih (tidak masuk DB, hanya CSV) |

## `job_skill` (long format)

| Kolom | Keterangan |
|---|---|
| `id_lowongan` | FK → lowongan |
| `skill` | 1 dari 22 skill terdeteksi (SQL, Python, R, Excel, GSheets, Power BI, Tableau, Looker, BigQuery, Cloud, Spark, Airflow, ETL, Statistik, ML, Visualisasi, Storytelling, dbt, Git, SPSS/SAS, JIRA, NoSQL, ERP/SAP) |

## Pemetaan enum (asumsi terdokumentasi)

**work_experience (Kalibrr):** 100=<1 thn, 200=1–3 thn, 300=3–5 thn,
400=5–10 thn, 500=>10 thn.
**education_level (Kalibrr):** 200=SMA/SMK, 350–450=D1–D4, 550=S1,
≥600=S2/S3.
Pemetaan ini inferensi dari urutan kode — tidak ada dokumentasi resmi
Kalibrr yang dipublikasikan; dicatat sebagai asumsi.

## Aturan filter relevansi

Baris dipertahankan jika: `peran_analyst` (judul match) **atau**
≥2 dari 12 core skill (SQL, Python, R, Excel, PBI, Tableau, Looker,
BigQuery, Statistik, Visualisasi, GSheets, ETL) terdeteksi di teks.
