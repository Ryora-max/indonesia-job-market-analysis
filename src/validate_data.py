"""Validasi dataset job market — check integritas & aturan bisnis."""
import sys
import pandas as pd

lv = pd.read_csv("data/processed/lowongan.csv")
sk = pd.read_csv("data/processed/job_skill.csv")
checks = []

def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

check("baris lowongan > 0", len(lv) > 0, f"{len(lv)} baris")
check("id_lowongan unik", lv.id_lowongan.is_unique)
check("judul tidak kosong", lv.judul.notna().all())
check("peran_analyst boolean", lv.peran_analyst.dtype == bool)
check("role_family terisi", lv.role_family.notna().all())
check("senioritas valid", lv.senioritas.isin(
    ["Junior / Entry", "Mid", "Senior / Lead"]).all())
check("tgl_posting format", lv.tgl_posting.str.match(r"\d{4}-\d{2}-\d{2}").all())
check("gaji masuk akal (0.5–100 jt)",
      ((lv.gaji_max_jt.dropna() >= 0.5) & (lv.gaji_max_jt.dropna() <= 100)).all())
check("gaji_min <= gaji_max",
      (lv.dropna(subset=["gaji_min_jt", "gaji_max_jt"])
         .pipe(lambda d: d.gaji_min_jt <= d.gaji_max_jt)).all())
check("job_skill -> lowongan FK",
      set(sk.id_lowongan) <= set(lv.id_lowongan))
check("skill tidak kosong", sk.skill.notna().all())
check("ada >= 10 skill terdeteksi", sk.skill.nunique() >= 10,
      f"{sk.skill.nunique()} skill")
check("tidak ada karakter rusak",
      ~lv.judul.str.contains("�", regex=False).any())
check("provinsi terisi >80%",
      lv.provinsi.notna().mean() > 0.8,
      f"{lv.provinsi.notna().mean():.0%}")
check("tipe kerja valid",
      lv.tipe.isin(["Full time", "Contractual", "Part time", "Freelance",
                    "Internship", None]).all())

gagal = [c for c in checks if not c[1]]
for name, ok, detail in checks:
    print(f"  [{'OK' if ok else 'GAGAL'}] {name} {detail}")
print(f"\n{len(checks)-len(gagal)}/{len(checks)} checks lolos")
sys.exit(1 if gagal else 0)
