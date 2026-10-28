# Executive Report — Indonesia Analytics Job Market

**Basis:** 296 lowongan relevan (Kalibrr + LinkedIn guest API), snapshot
Okt 2026. Semua angka dihitung `src/key_metrics.py`; uji statistik di
`notebooks/02_statistik_job_market.ipynb`. **Data riil, bukan sintetis.**

## Ringkasan eksekutif

Pasar kerja analitik Indonesia terkonsentrasi ekstrem di Jakarta,
didominasi permintaan skill fundamental (Excel, SQL, statistik) — bukan
tools hype — dengan transparansi gaji yang sangat rendah dan peluang
remote yang hampir tidak ada. Untuk pencari kerja profil data analyst,
pasar ini menuntut strategi *Jakarta-centric* atau menunggu lebih lama
untuk posisi regional.

## Temuan terkuantifikasi

### 1. Komposisi permintaan
- **296** lowongan relevan dari **1.890** hasil fetch → hanya **~16%**
  hasil pencarian yang benar-benar relevan. Noise job board tinggi:
  fuzzy matching mengembalikan "Community Officer" untuk query analyst.
- 79% berjudul analyst/data; 21% peran adjacent yang menuntut skill
  analitik (sales, ops, IT).
- Keluarga peran terbesar: **Data Analyst (17%)**, Data Scientist (13%),
  Business/System Analyst (12%), Data Engineer (7%) — sisanya analyst
  lintas domain (38%).
- Senioritas: 69% Mid, 24% Senior/Lead, hanya 6% Junior/Entry.

### 2. Geografi & cara kerja
- **80% lowongan di DKI Jakarta**; Banten 6%, Jawa Barat 5%. → Pasar
  analitik praktis = pasar Jakarta.
- Remote murni: **1,7%**. Hybrid: 9,8%. → On-site masih default.
- 89% full-time; 10% kontrak; freelance nyaris tidak ada.

### 3. Skill demand (basis 160 lowongan dengan skill terdeteksi)
| Skill | Share |
|---|---|
| Excel | 26% |
| SQL | 26% |
| Statistik | 21% |
| Python | 17% |
| Google Sheets | 14% |
| Visualisasi Data | 14% |
| Storytelling/Presentasi | 12% |
| Machine Learning | 11% |
| Power BI | 8% |

→ **Paket minimal employable:** Excel + SQL + statistik dasar. Python
adalah pembeda, bukan prasyarat universal. ML diminta 1 dari 9 — niche,
bukan mainstream.

### 4. Gaji — temuan dengan keterbatasan keras
- Hanya **18/296 (6%)** lowongan menampilkan gaji (Kalibrr saja).
- Median gaji max: **Rp10,5 jt/bln**; rentang Rp2,6–25 jt.
- Per senioritas (n sangat kecil): Junior ~6,8 (n=2) → Mid 10,0 (n=14)
  → Senior ~22,5 (n=2). Arah naik konsisten tapi **bukan estimasi
  pasar** — indikatif saja.

### 5. Perusahaan & industri
- Industri teraktif: IT (43), Financial Services (22), E-Commerce (20).
- Perekru teratas: Astro Technologies (20), BFI Finance (12), Kompas
  Gramedia (8), Ruangguru (6), Kredivo (6) → fintech + media + edtech
  mendominasi rekrutmen analitik.

## Uji statistik — termasuk yang TIDAK signifikan

| Uji | Hasil | Interpretasi |
|---|---|---|
| Judul analyst × senioritas | chi²=3,6, **p=0,17** | Tidak ada asosiasi — level senioritas tidak bergantung pada apakah perusahaan menamai peran "analyst" |
| Judul analyst × fresh-grad | chi²=3,7, **p=0,053** | Borderline — arahnya justru sebaliknya: peran non-analyst *lebih* terbuka ke fresh grad (17,5% vs 8,2%) |
| Gaji junior < senior | n terlalu kecil | Deskriptif saja; uji tidak layak secara etis |

**Integritas analisis:** melaporkan hasil non-signifikan sama pentingnya
dengan yang signifikan — itu yang membedakan laporan analis dari daftar
angka.

## Keterbatasan (wajib dibaca)

1. Sampel 2 platform; JobStreet/Glints tidak tercakup → bukan sensus.
2. Deskripsi LinkedIn ter-fetch hanya 46/199 (throttle) → analisis
   skill dominan Kalibrr.
3. Ekstraksi skill via regex — akurat untuk penyebutan eksplisit.
4. Gaji: bias ke perusahaan transparan, n=18.
5. Tanggal posting = aktivasi platform, Nov 2025–Okt 2026.

## Implikasi untuk pencari kerja (konteks portfolio)

Dataset ini sekaligus menjawab "skill apa yang layak diprioritaskan":
Excel+SQL+statistik adalah lantai; Python membedakan; Jakarta adalah
medan utama. Portfolio tiga project ini memetakan persis kompetensi
tersebut.
