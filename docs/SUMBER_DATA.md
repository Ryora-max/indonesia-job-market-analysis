# Sumber Data — Job Market Indonesia

Semua data **riil**, bukan sintetis. Diambil dari endpoint publik pada
27 Oktober 2026.

## Sumber

| Sumber | Endpoint | Data yang didapat | Status |
|---|---|---|---|
| **Kalibrr** | `kalibrr.com/kjs/job_board/search` | Judul, perusahaan, industri, lokasi (city/region), deskripsi+kualifikasi lengkap, gaji (subset), tipe kerja, flag remote/hybrid/fresh-grad, kode pengalaman & pendidikan, tanggal posting | ✅ sumber utama |
| **LinkedIn guest API** | `linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search` + `.../jobPosting/{id}` | Judul, perusahaan, lokasi, tanggal posting; detail (deskripsi, seniority, employment type, industri) untuk subset | ⚠️ throttle 429 — diatasi dgn drip-fetch |
| **JobStreet** | `id.jobstreet.com/api/chalice-search/v4` | — | ❌ bot-protection (challenge page) |
| **Glints** | `glints.com/api/jobVacancies` | — | ❌ firewall blokir |
| **RemoteOK / Remotive** | `remoteok.com/api`, `remotive.com/api` | — | ❌ tidak ada lowongan Indonesia-relevan |

## Catatan pengumpulan

- **Paginasi + dedup**: Kalibrr 52 kata kunci × maks 16 halaman
  (@50 baris); LinkedIn 9 kata kunci × maks 10 halaman (@10 baris).
  Dedup berdasarkan `id` lowongan antar-kata-kunci — satu lowongan bisa
  muncul di banyak pencarian.
- **Fuzzy search noise**: kedua platform mengembalikan hasil longgar
  (mis. query "mis officer" → "Community Officer"). Hanya ~8–17%
  hasil yang lolos filter relevansi — ini temuan tersendiri tentang
  kualitas pencarian job board.
- **Etika**: hanya endpoint publik tanpa login, `User-Agent` jelas,
  delay 0,6–2,2 detik antar request, checkpoint berkala. Tidak ada
  data pribadi pelamar — hanya metadata lowongan yang memang publik.

## Keterbatasan yang harus dibaca sebelum mengutip angka

1. **Coverage platform**: hanya 2 job board. JobStreet, Glints
   (firewall), Jobstreet/internal portal perusahaan tidak tercakup →
   dataset ini *sampel pasar*, bukan sensus.
2. **Skill**: diekstrak regex dari teks — akurat untuk skill eksplisit,
   bisa meleset pada penyebutan ambigu.
3. **Gaji**: hanya Kalibrr yang menampilkannya, dan hanya ~4% lowongan.
   Analisis gaji = kondisi perusahaan transparan, bukan pasar.
4. **Deskripsi LinkedIn**: throttle 429 membatasi fetch detail ke
   394/394 detail → analisis skill kini mencakup kedua platform secara berimbang; kontribusi LinkedIn
   terutama pada komposisi peran/lokasi/perusahaan/tren.
5. **Snapshot**: tanggal posting = tanggal aktivasi di platform,
   November 2025 – Oktober 2026.
