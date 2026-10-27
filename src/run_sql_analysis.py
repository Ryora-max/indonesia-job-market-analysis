"""Jalankan semua query di database/queries.sql -> outputs/sql_results/."""
import re
import sqlite3
from pathlib import Path

import pandas as pd

con = sqlite3.connect("database/jobmarket.db")
sql = Path("database/queries.sql").read_text(encoding="utf-8")
out_dir = Path("outputs/sql_results")
out_dir.mkdir(parents=True, exist_ok=True)

blocks = [b.strip() for b in re.split(r"--\s*\d{2}\s", sql) if "SELECT" in b]
for i, block in enumerate(blocks, 1):
    q = "\n".join(l for l in block.splitlines()[1:]
                  if not l.strip().startswith("--")).split(";")[0]
    df = pd.read_sql_query(q, con)
    df.to_csv(out_dir / f"q{i:02d}.csv", index=False)
    print(f"--- query {i} ({len(df)} baris) ---")
    print(df.head(10).to_string(index=False))
    print()
con.close()
print(f"{len(blocks)} query dieksekusi -> {out_dir}/")
