#!/usr/bin/env python3
"""
Merge rule-generated respell_ga / respell_rp into the wordlist.
Overwrites both fields for every word present in phase2b_respell_draft.json.
Does NOT touch ipa, rp_ipa, ipa_actual_ga, ipa_actual_rp, or any other field.

The 52 words in phase2b_respell_pending.json are intentionally NOT included
in phase2b_respell_draft.json (their GA narrow IPA is still awaiting TTS
review from Phase 2a) — this script only processes the draft file, so those
52 words are left untouched (no respell_ga/respell_rp added yet).
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDLIST = ROOT / "wordlist_GA_a1a2_plus_phonics.json"
DEFAULT_DRAFT = ROOT / "phase2b_respell_draft.json"
PENDING = ROOT / "phase2b_respell_pending.json"


def main():
    parser = argparse.ArgumentParser(description="Merge respell_ga / respell_rp into wordlist")
    parser.add_argument(
        "--draft",
        type=Path,
        default=DEFAULT_DRAFT,
        help="Respelling draft JSON (default: phase2b_respell_draft.json)",
    )
    parser.add_argument(
        "--clear-pending",
        action="store_true",
        default=None,
        help="Clear respell on phase2b_respell_pending.json words before merge",
    )
    parser.add_argument(
        "--no-clear-pending",
        action="store_true",
        help="Do not clear respell on pending-review words",
    )
    args = parser.parse_args()
    draft_path = args.draft if args.draft.is_absolute() else ROOT / args.draft
    clear_pending = args.clear_pending
    if clear_pending is None:
        clear_pending = draft_path.resolve() == DEFAULT_DRAFT.resolve()
    if args.no_clear_pending:
        clear_pending = False

    data = json.loads(WORDLIST.read_text(encoding="utf-8"))
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    pending_words = set()
    if clear_pending and PENDING.exists():
        pending_words = {r["w"] for r in json.loads(PENDING.read_text(encoding="utf-8"))}
    lookup = {w["w"]: w for w in data}

    cleared = 0
    for word in pending_words:
        entry = lookup.get(word)
        if not entry:
            continue
        had = "respell_ga" in entry or "respell_rp" in entry
        entry.pop("respell_ga", None)
        entry.pop("respell_rp", None)
        if had:
            cleared += 1

    merged, skipped = 0, []
    for d in draft:
        word = d["w"]
        if word not in lookup:
            skipped.append(word)
            continue
        entry = lookup[word]
        entry["respell_ga"] = d["respell_ga"]
        entry["respell_rp"] = d["respell_rp"]
        merged += 1

    WORDLIST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"merged {merged} / {len(draft)} entries from {draft_path.name}")
    if clear_pending and cleared:
        print(f"cleared respell on {cleared} pending-review words")
    if skipped:
        print(f"WARN: skipped (not in wordlist): {skipped}")


if __name__ == "__main__":
    main()
