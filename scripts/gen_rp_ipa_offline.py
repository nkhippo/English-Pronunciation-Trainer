#!/usr/bin/env python3
"""Generate data/rp_complete.json via rule-based GA→RP conversion."""
import json
from pathlib import Path

from ga_to_rp import ga_to_rp

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "wordlist_GA_a1a2_plus_phonics.json"
OUTPUT = ROOT / "data" / "rp_complete.json"


def main():
    rows = json.loads(INPUT.read_text(encoding="utf-8"))
    out = []
    for row in rows:
        item = dict(row)
        item["rp_ipa"] = ga_to_rp(row["w"], row["ipa"])
        out.append(item)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    missing = sum(1 for r in out if not r.get("rp_ipa"))
    print(f"generated: {len(out)} entries -> {OUTPUT}")
    print(f"missing rp_ipa: {missing}")


if __name__ == "__main__":
    main()
