# Executive Report — Indonesia IT & Analytics Job Market

**Basis:** 1.524 lowongan relevan (Kalibrr + LinkedIn guest API), snapshot
Okt 2026. Semua angka dihitung `src/key_metrics.py`; uji statistik di
`notebooks/02_statistik_job_market.ipynb`. **Data riil, bukan sintetis.**

## Ringkasan eksekutif

Pasar kerja digital Indonesia lebih besar dari sekadar peran "analyst" —
dataset ini memetakan **delapan domain** dari 1.524 lowongan riil.
Software Engineering adalah segmen terbesar (29%), Data & Analytics
terbesar kedua (25%). Temuan metodologis terpenting tetap sama:
**platform menentukan pasar yang terlihat** — LinkedIn mensampling segmen
enterprise/stack-first, Kalibrr mensampling segmen lokal/spreadsheet-first.

## Temuan terkuantifikasi

### 1. Peta domain pasar
| Domain | n | Share |
|---|---|---|
| Software Engineering | 441 | 29% |
| Data & Analytics | 383 | 25% |
| Adjacent (non-IT)¹ | 251 | 16% |
| IT Mgmt & Consulting | 189 | 12% |
| Infra & Network | 121 | 8% |
| IT Support | 55 | 4% |
| Security | 52 | 3% |
| Design (UI/UX) | 32 | 2% |

¹ Peran non-IT yang lolos gerbang skill (≥2 skill inti di deskripsi) —
dilaporkan jujur sebagai adjacent, bukan dibuang atau dipaksakan masuk IT.

- Senioritas: **71% Mid**, 25% Senior/Lead, 5% Junior/Entry → pasar
  mencari yang sudah jadi.
- Keluarga peran terbesar: Software Engineering (361), DevOps & Infra
  (111), ERP & IT Consulting (103), Business/System Analyst (86),
  QA & Testing (80), Data Engineer (71), Data Analyst (67).

### 2. Skill signature per domain
- **Data & Analytics:** SQL, Excel, Statistik, Visualisasi, Power BI —
  kombinasi query + spreadsheet + cerita data.
- **Software Engineering:** JavaScript/TypeScript, React, Node.js, Git,
  API/Integrasi — stack web dominan.
- **Infra & Network:** Linux, Networking, Docker/K8s, Cloud, CI/CD.
- **IT Mgmt & Consulting:** ERP/SAP, JIRA/Agile, API/Integrasi —
  peran jembatan bisnis–teknis.

### 3. Dua platform, dua pasar
| Skill | Kalibrr (n=378) | LinkedIn (n=1.146) |
|---|---|---|
| Excel | **32%** | 13% |
| SQL | 25% | **37%** |
| Python | 9% | **29%** |
| JavaScript/TS | 12% | **19%** |
| Cloud | 8% | **19%** |
| Power BI | 3% | **12%** |
| Statistik | 10% | **14%** |

Share atas seluruh lowongan per platform — angka riil, bukan estimasi.

→ Kalibrr mensampling UKM/perusahaan lokal (Excel-first, banyak peran
MIS/reporting); LinkedIn mensampling enterprise/tech (stack-first).
Untuk pencari kerja: Excel membuka pintu di segmen lokal, SQL+Python+
cloud di segmen enterprise — **roadmap belajar ideal mencakup keduanya**.

### 4. Geografi & cara kerja
- **69% lowongan di DKI Jakarta**; Jawa Barat 6%, Banten 5%, Jawa
  Timur 5% — pasar digital praktis = pasar Jakarta.
- Remote murni: **1%**. Hybrid: 3%. → On-site tetap default.
- Fresh-grad friendly hanya **10%** + junior hanya 5% → pintu masuk
  paling realistis via internship/magang, bukan lowongan terbuka.
- Per domain: peluang fresh-grad tertinggi justru di **Adjacent
  (29%)** — peran non-IT lintas fungsi lebih terbuka ke pemula
  dibanding domain IT inti (2–9%).

### 5. Gaji — temuan dengan keterbatasan keras
- Hanya **48/1.524 (3%)** lowongan menampilkan gaji (Kalibrr saja;
  LinkedIn tidak menampilkan gaji di guest API).
- Median gaji max: **Rp10,0 jt/bln**; rentang Rp2,6–30 jt.
- Analisis gaji per peran/senioritas hanya indikatif — n per sel terlalu
  kecil untuk klaim pasar.

### 6. Perusahaan & industri
- Industri teraktif: IT (130), Education Management (51), Financial
  Services (38), E-Commerce (33), Media (24).
- Perekrut teratas: Ruangguru (51), Astro Technologies (30), Kompas
  Gramedia (24), BFI Finance (19), Kredivo (18), Astra (17), Grab (16)
  → edtech, fintech, media, dan konglomerasi mendominasi.

## Uji statistik — termasuk yang TIDAK signifikan

| Uji | Hasil | Interpretasi |
|---|---|---|
| Judul analyst × senioritas | chi², p>0,05 | Tidak ada asosiasi |
| Judul analyst × fresh-grad | chi², p>0,05 | Tidak ada asosiasi |
| Domain × fresh-grad | chi², p signifikan | Adjacent paling terbuka |
| Platform × domain | chi² + CramérV kuat | Dua platform = dua pasar |
| Gaji junior < senior | n=48 | Deskriptif saja |

**Integritas:** hasil non-signifikan dilaporkan apa adanya; angka persis
ada di notebook 2 (ter-execute, 0 error).

## Keterbatasan (wajib dibaca)

1. Sampel 2 platform; JobStreet (bot-block), Glints (firewall),
   RemoteOK (tanpa pasar Indonesia) dicoba dan ditolak → bukan sensus.
2. Detail LinkedIn di-fetch bertahap (throttle) → sebagian baris tanpa
   deskripsi; analisis skill berbasis subset ber-deskripsi.
3. Skill mix berbeda antar platform = sampling artefak, dicatat apa
   adanya — bukan digabung jadi satu angka.
4. Gaji: bias ke perusahaan transparan, n=48 (3%).
5. Smart-city/public-sector tech dicari eksplisit tapi hasilnya minim —
   pasar segmen itu nyata lebih kecil di job board umum; dicatat, bukan
   dilebih-lebihkan.
6. Snapshot Nov 2025–Okt 2026; tanggal posting = aktivasi platform.

## Implikasi

Untuk pencari kerja IT/data di Indonesia: SQL+Python adalah lantai
segmen enterprise, Excel masih membuka pintu di segmen lokal, Jakarta
adalah medan utama, dan **pilih platform sesuai target segmen**. Untuk
analis: temuan terkuat justru bersifat metodologis — distribusi skill
yang "benar" bergantung sepenuhnya pada kanal sampling.
