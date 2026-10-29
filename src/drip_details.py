"""Resume drip-fetch untuk detail LinkedIn yang masih pending.

Strategi pelan + retry (berhasil di sesi sebelumnya):
- jeda 4 detik antar request
- retry sampai 3x per job dengan backoff 20 detik
- checkpoint tiap 25 job
"""
import json
import sys
import time

sys.path.insert(0, ".")
from src.fetch_linkedin import parse_detail  # noqa: E402

OUT = "data/raw/linkedin_jobs_raw.json"

jobs = {j["id"]: j for j in json.load(open(OUT, encoding="utf-8"))}
pending = [j for j in jobs.values() if not j.get("detail_fetched")]
print(f"pending detail: {len(pending)}")

ok = fail = 0
since = 0
for j in pending:
    done = False
    for attempt in range(3):
        try:
            j.update(parse_detail(j["id"]))
            j["detail_fetched"] = True
            ok += 1
            done = True
            break
        except Exception as e:
            wait = 20 * (attempt + 1)
            print(f"  {j['id']} attempt {attempt + 1}: {e} -> tidur {wait}s")
            time.sleep(wait)
    if not done:
        fail += 1
        j["detail_fetched"] = False
    since += 1
    if since % 25 == 0:
        json.dump(list(jobs.values()), open(OUT, "w", encoding="utf-8"),
                  ensure_ascii=False)
        print(f"checkpoint {since}/{len(pending)} (ok {ok}, gagal {fail})")
    time.sleep(4)

json.dump(list(jobs.values()), open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False)
print(f"selesai: ok {ok}, gagal {fail}, total {len(jobs)}")
