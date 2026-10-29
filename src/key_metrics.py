"""Hitung semua angka yang dipakai di README/laporan -> outputs/key_metrics.md.

Satu-satunya sumber angka dokumen — jalankan ulang setelah data berubah.
"""
import pandas as pd

lv = pd.read_csv("data/processed/lowongan.csv")
sk = pd.read_csv("data/processed/job_skill.csv")
n = len(lv)
out = []

def add(s=""):
    out.append(s)
    print(s)

add("# Key Metrics — Job Market Indonesia (dihitung otomatis)")
add()
add(f"- Lowongan relevan: **{n:,}**")
add(f"- Peran analyst (judul match): **{lv.peran_analyst.sum()}** "
    f"({lv.peran_analyst.mean():.0%})")
add(f"- Periode posting: **{lv.tgl_posting.min()} s.d. {lv.tgl_posting.max()}**")
add(f"- Menampilkan gaji: **{lv.gaji_max_jt.notna().sum()}** "
    f"({lv.gaji_max_jt.notna().mean():.0%})")
add(f"- Remote: **{lv.remote.sum()}** ({lv.remote.mean():.0%}) | "
    f"Hybrid: **{lv.hybrid.sum()}** ({lv.hybrid.mean():.0%})")
add(f"- Fresh-grad friendly: **{lv.fresh_grad_ok.sum()}** "
    f"({lv.fresh_grad_ok.mean():.0%})")
add()
add("## Top 10 skill")
top = (sk.skill.value_counts().head(10))
for s, c in top.items():
    add(f"- {s}: {c} lowongan ({c/n:.0%})")
add()
add("## Domain pekerjaan")
for d, c in lv.domain.value_counts().items():
    add(f"- {d}: {c} ({c/n:.0%})")
add()
add("## Keluarga peran")
for r, c in lv.role_family.value_counts().items():
    add(f"- {r}: {c} ({c/n:.0%})")
add()
add("## Top 5 provinsi")
for p, c in lv.provinsi.value_counts().head(5).items():
    add(f"- {p}: {c} ({c/n:.0%})")
add()
add("## Gaji (lowongan bergaji)")
add(f"- Median max: **Rp{lv.gaji_max_jt.median():.1f} jt/bln**")
add(f"- Rentang max: Rp{lv.gaji_max_jt.min():.1f} s.d. {lv.gaji_max_jt.max():.1f} jt")
add()
add("## Senioritas")
for s_, c in lv.senioritas.value_counts().items():
    add(f"- {s_}: {c} ({c/n:.0%})")

open("outputs/key_metrics.md", "w", encoding="utf-8").write("\n".join(out))
print("\n-> outputs/key_metrics.md")
