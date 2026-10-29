# Data Dictionary — IT & Analytics Job Market

Dua tabel relasional: `lowongan` 1—n `job_skill`.

## `lowongan` (1 baris = 1 lowongan)

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id_lowongan` | str | `kb_<id>` (Kalibrr) / `li_<id>` (LinkedIn) — PK |
| `sumber` | str | `kalibrr` / `linkedin` |
| `judul` | str | Judul lowongan (dibersihkan dari karakter rusak) |
| `peran_analyst` | bool | True jika judul match pola analyst/data/MIS |
| `role_family` | str | 21 keluarga peran (lihat daftar di bawah) |
| `domain` | str | Segmen pasar: `Data & Analytics` · `Software Engineering` · `Infra & Network` · `Security` · `IT Support` · `IT Mgmt & Consulting` · `Design (UI/UX)` · `Adjacent (non-IT)` |
| `senioritas` | str | `Junior / Entry` · `Mid` · `Senior / Lead` — dari judul + kode pengalaman (Kalibrr) atau kriteria LinkedIn |
| `perusahaan` | str | Nama perusahaan |
| `industri` | str | Industri perusahaan (Kalibrr) / criteria LinkedIn |
| `fungsi` | str | Job function kategori platform |
| `kota` / `provinsi` | str | Lokasi — provinsi dinormalisasi ("West Java (Jawa Barat)" → "Jawa Barat") |
| `tipe` | str | Full time · Contractual · Part time · Freelance · Internship |
| `remote` / `hybrid` / `fresh_grad_ok` | bool | Flag dari platform / teks |
| `pengalaman` | str | Label level pengalaman (Kalibrr enum dipetakan; LinkedIn criteria) |
| `pendidikan` | str | Level pendidikan (Kalibrr enum dipetakan; LinkedIn: null) |
| `gaji_min_jt` / `gaji_max_jt` | float | Rp juta/bulan — hanya Kalibrr, ~3% terisi |
| `tgl_posting` / `tgl_tutup` | str | Tanggal aktivasi / deadline (ISO) |
| `teks` | str | Deskripsi+kualifikasi bersih (tidak masuk DB, hanya CSV) |

## `job_skill` (long format)

| Kolom | Keterangan |
|---|---|
| `id_lowongan` | FK → lowongan |
| `skill` | 1 dari 39 skill terdeteksi — analitik (SQL, Python, Excel, PBI, Tableau, Statistik, ML, ETL, dsb.) + IT (JavaScript/TS, React, Node.js, Java, PHP, Git, Docker/K8s, CI/CD, Cloud, Linux, Networking, API, JIRA, ERP/SAP, QA tools, UI/UX, dsb.) |

## `role_family` — 21 keluarga

Data Analyst · Data Scientist · Data Engineer · BI/Analytics ·
Business/System Analyst · MIS/Reporting · Risk & Credit · Ops & Domain ·
Product · Marketing · Financial · Analyst Lainnya · Software
Engineering · QA & Testing · Security · DevOps & Infra · IT Support ·
UI/UX Design · ERP & IT Consulting · DBA/Database · Adjacent.

`Adjacent` = judul tidak match pola IT/analyst manapun tapi lolos gerbang
skill — dilaporkan terpisah supaya klasifikasi jujur.

## Pemetaan enum (asumsi terdokumentasi)

**work_experience (Kalibrr):** 100=<1 thn, 200=1–3 thn, 300=3–5 thn,
400=5–10 thn, 500=>10 thn.
**education_level (Kalibrr):** 200=SMA/SMK, 350–450=D1–D4, 550=S1,
≥600=S2/S3.
Pemetaan ini inferensi dari urutan kode — tidak ada dokumentasi resmi
Kalibrr yang dipublikasikan; dicatat sebagai asumsi.

## Aturan filter relevansi

Baris dipertahankan jika salah satu terpenuhi:
1. `peran_analyst` — judul match pola analyst/data/MIS
2. Judul match pola IT (developer, engineer, devops, QA, security,
   UI/UX, ERP, IT support, network, sysadmin, DBA, IT manager/PMO, dll.)
3. Deskripsi menuntut ≥2 skill inti terdeteksi (gerbang skill) — hasilnya
   masuk `Adjacent` jika judulnya bukan IT/analyst.
