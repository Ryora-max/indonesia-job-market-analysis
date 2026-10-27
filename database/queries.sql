-- Analisis pasar kerja analitik Indonesia (Kalibrr, data riil)
-- 12 query: skill demand, geografi, gaji, senioritas, pola perusahaan

-- 01 Skill paling banyak diminta (share atas seluruh lowongan)
SELECT s.skill,
       COUNT(*)                          AS n_lowongan,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM lowongan), 1) AS persen
FROM job_skill s
GROUP BY s.skill
ORDER BY n_lowongan DESC;

-- 02 Skill per keluarga peran — top skill untuk peran "Data Analyst" murni
SELECT s.skill, COUNT(*) AS n
FROM job_skill s
JOIN lowongan l ON l.id_lowongan = s.id_lowongan
WHERE l.role_family = 'Data Analyst'
GROUP BY s.skill
ORDER BY n DESC;

-- 03 Distribusi keluarga peran
SELECT role_family, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM lowongan), 1) AS persen
FROM lowongan
GROUP BY role_family
ORDER BY n DESC;

-- 04 Provinsi dengan permintaan terbanyak
SELECT provinsi, COUNT(*) AS n
FROM lowongan
WHERE provinsi IS NOT NULL
GROUP BY provinsi
ORDER BY n DESC
LIMIT 15;

-- 05 Kota: jumlah lowongan + % remote
SELECT kota, COUNT(*) AS n,
       ROUND(100.0 * SUM(remote) / COUNT(*), 1) AS pct_remote,
       ROUND(100.0 * SUM(hybrid) / COUNT(*), 1) AS pct_hybrid
FROM lowongan
WHERE kota IS NOT NULL
GROUP BY kota
HAVING n >= 3
ORDER BY n DESC;

-- 06 Rentang gaji per keluarga peran (hanya lowongan yg menampilkan gaji)
SELECT role_family,
       COUNT(*) AS n_dengan_gaji,
       ROUND(AVG(gaji_min_jt), 1) AS avg_min,
       ROUND(AVG(gaji_max_jt), 1) AS avg_max
FROM lowongan
WHERE gaji_max_jt IS NOT NULL
GROUP BY role_family
HAVING n_dengan_gaji >= 3
ORDER BY avg_max DESC;

-- 07 Gaji per provinsi (lowongan bergaji)
SELECT provinsi, COUNT(*) AS n,
       ROUND(AVG(gaji_max_jt), 1) AS avg_max_jt
FROM lowongan
WHERE gaji_max_jt IS NOT NULL AND provinsi IS NOT NULL
GROUP BY provinsi
HAVING n >= 3
ORDER BY avg_max_jt DESC;

-- 08 Skill premium: rata-rata gaji_max untuk lowongan yang menuntut skill tsb
SELECT s.skill,
       COUNT(*) AS n_bergaji,
       ROUND(AVG(l.gaji_max_jt), 1) AS avg_gaji_max_jt
FROM job_skill s
JOIN lowongan l ON l.id_lowongan = s.id_lowongan
WHERE l.gaji_max_jt IS NOT NULL
GROUP BY s.skill
HAVING n_bergaji >= 3
ORDER BY avg_gaji_max_jt DESC;

-- 09 Senioritas x keluarga peran
SELECT senioritas, role_family, COUNT(*) AS n
FROM lowongan
GROUP BY senioritas, role_family
ORDER BY senioritas, n DESC;

-- 10 Remote/hybrid/fresh-grad rate per keluarga peran
SELECT role_family,
       COUNT(*) AS n,
       ROUND(100.0 * SUM(remote) / COUNT(*), 1)  AS pct_remote,
       ROUND(100.0 * SUM(hybrid) / COUNT(*), 1)  AS pct_hybrid,
       ROUND(100.0 * SUM(fresh_grad_ok) / COUNT(*), 1) AS pct_fresh_ok
FROM lowongan
GROUP BY role_family
ORDER BY n DESC;

-- 11 Industri perekrut terbanyak
SELECT industri, COUNT(*) AS n
FROM lowongan
WHERE industri IS NOT NULL
GROUP BY industri
ORDER BY n DESC
LIMIT 15;

-- 12 Tren posting per bulan
SELECT substr(tgl_posting, 1, 7) AS bulan, COUNT(*) AS n
FROM lowongan
GROUP BY bulan
ORDER BY bulan;
