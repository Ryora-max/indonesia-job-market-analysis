# Executive Report — Indonesia Analytics Job Market

**Basis:** 465 lowongan relevan (Kalibrr + LinkedIn guest API), snapshot
Okt 2026. Semua angka dihitung `src/key_metrics.py`; uji statistik di
`notebooks/02_statistik_job_market.ipynb`. **Data riil, bukan sintetis.**

## Ringkasan eksekutif

Pasar kerja analitik Indonesia terkonsentrasi ekstrem di Jakarta dan
— temuan paling penting — **tersegmentasi oleh platform**: Kalibrr
melayani segmen spreadsheet-first (Excel 60%), LinkedIn melayani segmen
teknikal (SQL 66%, Python 53%). Pertanyaan "skill apa yang diminta
pasar?" tidak punya satu jawaban; jawabannya bergantung kanal.

## Temuan terkuantifikasi

### 1. Komposisi permintaan
- **465** lowongan relevan dari **2.110** hasil fetch → hanya **~22%**
  hasil pencarian yang benar-benar relevan (Kalibrr ~8%, LinkedIn ~85%:
  pencarian LinkedIn jauh lebih presisi untuk peran ini).
- 77% berjudul analyst/data; 23% peran adjacent yang menuntut skill
  analitik.
- Keluarga peran terbesar: Business/System Analyst (15%), Data Engineer
  (13%), Data Analyst (12%), Data Scientist (9%); sisanya analyst
  lintas domain (38%).
- Senioritas: 71% Mid, 24% Senior/Lead, 5% Junior/Entry → pasar
  mencari yang sudah jadi, bukan melatih dari nol.

### 2. Dua platform, dua pasar
| Skill | Kalibrr (n=117) | LinkedIn (n=319) |
|---|---|---|
| Excel | **60%** | 32% |
| SQL | 41% | **66%** |
| Google Sheets | 36% | 8% |
| Python | 21% | **53%** |
| Power BI | 10% | **34%** |
| ETL/Pipeline | 11% | **33%** |
| Visualisasi | 24% | **43%** |
| Statistik | 27% | 41% |

Share atas lowongan ber-skill terdeteksi per platform — angka riil,
bukan estimasi.

→ Kalibrr mensampling UKM/perusahaan lokal (spreadsheet-first);
LinkedIn mensampling enterprise/tech (stack-first). Untuk pencari
kerja: Excel membuka pintu di segmen lokal, SQL+Python di segmen
enterprise — **roadmap belajar ideal mencakup keduanya**.

### 3. Geografi & cara kerja
- **79% lowongan di DKI Jakarta**; Jawa Barat 6%, Banten 4% — pasar
  analitik praktis = pasar Jakarta.
- Remote murni: **1%**. Hybrid: 6%. → On-site tetap default.
- Fresh-grad friendly hanya ~12% + junior hanya 5% → pintu masuk
  paling realistis via internship/MBKM, bukan lowongan terbuka.

### 4. Gaji — temuan dengan keterbatasan keras
- Hanya **18/465 (4%)** lowongan menampilkan gaji (Kalibrr saja;
  LinkedIn tidak menampilkan gaji di guest API).
- Median gaji max: **Rp10,5 jt/bln**; rentang Rp2,6–25 jt.
- Per senioritas (n kecil): Junior ~6,8 → Mid 10,0 → Senior ~22,5.

### 5. Perusahaan & industri
- Industri teraktif: IT (43), Financial Services (22), E-Commerce (20).
- Perekrut teratas: Astro Technologies (20), BFI Finance (12), Kredivo
  (9), Kompas Gramedia (8), Monee (8), Ruangguru (6) → fintech, media,
  edtech mendominasi.

## Uji statistik — termasuk yang TIDAK signifikan

| Uji | Hasil | Interpretasi |
|---|---|---|
| Judul analyst × senioritas | chi²=1,3, p=0,51 | Tidak ada asosiasi |
| Judul analyst × fresh-grad | chi²=1,1, p=0,29 | Tidak ada asosiasi |
| Gaji junior < senior | n=18 | Deskriptif saja |

**Integritas:** dengan n=465 dan tetap tidak signifikan, kesimpulan
"tidak ada asosiasi" lebih kuat dari sebelumnya — bukan kurang bukti,
melainkan memang tidak ada pola.

## Keterbatasan (wajib dibaca)

1. Sampel 2 platform; JobStreet (bot-block), Glints (firewall),
   RemoteOK (no ID) tidak tercakup → bukan sensus.
2. Skill mix berbeda antar platform = sampling artefak, dicatat apa
   adanya — bukan digabung jadi satu angka.
3. Gaji: bias ke perusahaan transparan, n=18.
4. Snapshot Nov 2025–Okt 2026; tanggal posting = aktivasi platform.

## Implikasi untuk pencari kerja

Excel+SQL adalah lantai universal; Python membedakan di segmen
enterprise; Jakarta adalah medan utama; dan — temuan paling berguna —
**pilih platform sesuai target segmen**, karena keduanya memotret
pasar yang berbeda.
