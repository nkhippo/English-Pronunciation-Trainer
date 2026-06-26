# -*- coding: utf-8 -*-
"""Merge gloss-fil-batchNN.json files into the wordlist's gloss.fil."""
import json
import glob
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WL = os.path.join(ROOT, "wordlist_GA_a1a2_plus_phonics.json")
BATCH_GLOB = os.path.join(ROOT, "data", "gloss-fil-batch*.json")

wl = json.load(open(WL, encoding="utf-8"))
fil = {}
files = sorted(glob.glob(BATCH_GLOB))
for f in files:
    fil.update(json.load(open(f, encoding="utf-8")))

applied, missing = 0, []
for it in wl:
    w = it["w"]
    v = fil.get(w)
    if v and v.strip():
        it.setdefault("gloss", {})["fil"] = v
        applied += 1
    else:
        missing.append(w)

json.dump(wl, open(WL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"batches: {len(files)} | fil entries: {len(fil)} | applied: {applied} | "
      f"words still without fil: {len(missing)}")
if missing[:20]:
    print("missing sample:", missing[:20])

c = Counter(it["gloss"]["fil"] for it in wl if "fil" in it.get("gloss", {}))
dups = {k: n for k, n in c.items() if n > 1}
print(f"identical fil cells (Mode B distractor-collision candidates): {len(dups)}")
if dups:
  top = sorted(dups.items(), key=lambda x: -x[1])[:10]
  print("top duplicates:", top)
