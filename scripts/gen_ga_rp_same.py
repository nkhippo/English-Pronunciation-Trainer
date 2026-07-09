#!/usr/bin/env python3
"""
gen_ga_rp_same.py — Assign `ga_rp_same` / `ga_rp_same_reason` fields.

DEFINITION (STRICT + GA-allophony carve-out)
============================================
A word is `ga_rp_same = true` iff its GA and RP realisations differ ONLY
in transcription conventions that do not affect what a learner hears:

  * Length marks (ː)                              — GA omits, RP shows
  * Secondary-stress markers (ˌ)                  — dictionary-source variation
  * DRESS vowel notation (ɛ ↔ e)                  — same phoneme, editorial choice

Everything else is `different`, in particular:

  * Primary-stress placement changes              — audible (baseball)
  * GOAT vowel (oʊ ↔ əʊ)                          — quality difference
  * LOT vowel (ɑ ↔ ɒ)                             — quality difference
  * Rhoticity (GA /r/, ɚ, ɝ vs RP schwa/long)     — structural
  * TRAP-BATH, CLOTH-LOT, yod-dropping, weak-vowel choice
  * GA-only allophony captured by ipa_actual_ga:
      – Flap-T [ɾ]         (city → [sɪɾi])
      – Syllabic consonants (button → [bʌʔn̩])
      – Glottal stop [ʔ]
    These are audibly different from RP even when phonemic /ipa/ matches.

REASON TAXONOMY
===============
same:
  identical               raw strings match
  length_marking_only     only ː differs
  stress_marking_only     only ˌ differs
  dress_notation_only     only ɛ↔e differs
  notation_composite      combination of the above

different:
  ga_allophony            ipa_actual_ga ≠ ipa (highest-priority carve-out)
  stress_placement        primary stress on different syllable
  rhoticity               peel-off matches after non-rhotic conversion
  goat_vowel              only oʊ↔əʊ remains after other peels
  lot_vowel               only ɑ↔ɒ remains
  trap_bath               only æ↔ɑː remains
  cloth_lot               only GA ɔ ↔ RP ɒ remains
  square_near_cure        r-coloured diphthong shifts (ɛr↔eə, ɪr↔ɪə, ʊr↔ʊə)
  yod                     GA drops /j/ where RP keeps it (new, tune, due)
  weak_vowel              schwa vs /ɪ/ etc. in unstressed syllables
  cot_caught              GA /ɑ/ merges with RP /ɔː/ (bought, thought)
  composite_structural    multiple structural differences (typical for
                          rhotic + BATH words like "after")
  lexical                 whole-word divergence (schedule, zebra, vitamin)
  structural_other        residual — cannot decompose into any of the above

USAGE
=====
Runs from repo root. Rewrites the three JSON files in place unless --dry-run.
"""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

# --- normalisation helpers ---------------------------------------------------

def strip_slashes(s: str) -> str:
    return s.strip().lstrip("/").rstrip("/").strip()

def drop_length(s: str) -> str:
    return s.replace("ː", "").replace(":", "")

def drop_secondary(s: str) -> str:
    return s.replace("ˌ", "")

def drop_all_stress(s: str) -> str:
    return s.replace("ˈ", "").replace("ˌ", "")

def unify_dress(s: str) -> str:
    return s.replace("ɛ", "e")

def notation_norm(s: str) -> str:
    return unify_dress(drop_secondary(drop_length(strip_slashes(s))))

# --- primary-stress position ------------------------------------------------

def primary_syllable_index(s: str) -> int:
    """Index of the primary-stress ˈ in the string after removing length &
    secondary marks. -1 if no primary stress mark."""
    s = drop_length(drop_secondary(strip_slashes(s)))
    return s.find("ˈ")

# --- structural transformations (applied when trying to explain a diff) -----

RHOTICITY_MAP = [
    ("aʊr", "aʊə"), ("aɪr", "aɪə"), ("ɔɪr", "ɔɪə"), ("eɪr", "eɪə"),
    ("ɑr", "ɑː"),   ("ɔr", "ɔː"),   ("ɪr", "ɪə"),   ("ɛr", "eə"),
    ("ʊr", "ʊə"),   ("ɝ", "ɜː"),    ("ɚ", "ə"),
]

def apply_rhoticity(ga_inner: str) -> str:
    s = ga_inner
    for src, dst in RHOTICITY_MAP:
        s = s.replace(src, dst)
    return s

BATH_WORDS = {
    "after","answer","ask","bath","branch","castle","chance","class",
    "dance","example","fast","glass","graph","half","laugh","last",
    "master","pass","past","path","plant","rather","staff","aunt",
    "banana","can't","aren't","afternoon","france","french","grass",
    "advantage","advance","afterwards",
}

# --- reason detectors --------------------------------------------------------

def reason_when_same(ga_raw: str, rp_raw: str) -> str:
    ga = strip_slashes(ga_raw)
    rp = strip_slashes(rp_raw)
    if ga == rp:
        return "identical"
    only_length = drop_length(ga) == drop_length(rp)
    only_stress = drop_secondary(ga) == drop_secondary(rp)
    only_dress  = unify_dress(ga) == unify_dress(rp)
    # single-axis wins
    if only_length and not only_stress and not only_dress:
        return "length_marking_only"
    if only_stress and not only_length and not only_dress:
        return "stress_marking_only"
    if only_dress and not only_length and not only_stress:
        return "dress_notation_only"
    return "notation_composite"

def reason_when_different(word: str, ga_raw: str, rp_raw: str) -> str:
    ga_inner = strip_slashes(ga_raw)
    rp_inner = strip_slashes(rp_raw)

    # 0. Stress-placement check (only if not just secondary-stress diff).
    ga_pri = primary_syllable_index(ga_inner)
    rp_pri = primary_syllable_index(rp_inner)
    if ga_pri >= 0 and rp_pri >= 0 and ga_pri != rp_pri:
        # Confirm rest matches when stress is stripped
        if notation_norm(ga_inner.replace("ˈ","")) == notation_norm(rp_inner.replace("ˈ","")):
            return "stress_placement"

    # 1. Yod (GA drops /j/ before /u/ after coronals: new, tune, due, produce)
    #    GA has /Cu/ where RP has /Cjuː/
    if "j" in rp_inner and "j" not in ga_inner:
        # Insert j before every u in ga_inner and see if it matches
        if notation_norm(ga_inner.replace("u", "ju")) == notation_norm(rp_inner):
            return "yod"

    # 2. Rhoticity — apply non-rhotic transform to GA, compare
    ga_derhotic = apply_rhoticity(ga_inner)
    if notation_norm(ga_derhotic) == notation_norm(rp_inner):
        return "rhoticity"

    # 3. GOAT — after rhoticity
    ga_goat = ga_derhotic.replace("oʊ", "əʊ")
    if notation_norm(ga_goat) == notation_norm(rp_inner):
        return "goat_vowel" if ga_derhotic != ga_goat else "rhoticity"

    # 4. LOT
    ga_lot = ga_goat.replace("ɑ", "ɒ")
    if notation_norm(ga_lot) == notation_norm(rp_inner):
        return "lot_vowel" if ga_goat != ga_lot else "goat_vowel"

    # 5. TRAP-BATH (word-triggered)
    if word.lower() in BATH_WORDS or ("æ" in ga_inner and "ɑː" in rp_inner):
        ga_bath = ga_lot.replace("æ", "ɑː")
        if notation_norm(ga_bath) == notation_norm(rp_inner):
            return "trap_bath"

    # 6. CLOTH-LOT / COT-CAUGHT split (GA merges ɔ/ɑ; RP separates)
    #    GA "bought" /bɑt/ vs RP /bɔːt/: GA ɑ → RP ɔː
    ga_cot = ga_lot.replace("ɑ", "ɔː")
    if notation_norm(ga_cot) == notation_norm(rp_inner):
        return "cot_caught"

    # 7. SQUARE / NEAR / CURE composites (peel goat/lot after rhoticity)
    #    "bear" /bɛr/ → /beə/, "dear" /dɪr/ → /dɪə/
    ga_sq = ga_inner.replace("ɛr", "eə").replace("ɪr", "ɪə").replace("ʊr", "ʊə")
    if notation_norm(ga_sq) == notation_norm(rp_inner):
        return "square_near_cure"

    # 8. Composite structural (rhoticity + BATH / rhoticity + LOT etc.)
    ga_combo = apply_rhoticity(ga_inner)
    ga_combo = ga_combo.replace("oʊ", "əʊ").replace("ɑ", "ɒ")
    if word.lower() in BATH_WORDS:
        ga_combo = ga_combo.replace("æ", "ɑː")
    if notation_norm(ga_combo) == notation_norm(rp_inner):
        return "composite_structural"

    # 9. Try weak-vowel: ə ↔ ɪ swap in unstressed syllables
    if notation_norm(ga_inner.replace("ə", "ɪ")) == notation_norm(rp_inner) or \
       notation_norm(ga_inner.replace("ɪ", "ə")) == notation_norm(rp_inner):
        return "weak_vowel"

    return "structural_other"

# --- main classifier --------------------------------------------------------

def classify(word: str, ipa: str, rp_ipa: str,
             ipa_actual_ga: str | None,
             ipa_actual_rp: str | None) -> tuple[bool, str]:
    if not ipa or not rp_ipa:
        return (False, "missing_data")

    # ---- CARVE-OUT: GA-only allophony (flap-T, syllabic C, glottal stop) ----
    # If GA has a narrow-level form that differs from its phonemic form, then
    # even when the phonemic forms match RP, the AUDIBLE forms differ.
    if ipa_actual_ga and ipa_actual_ga != ipa:
        rp_narrow = ipa_actual_rp or rp_ipa
        # Only overturn to different if the RP audible form does NOT match
        # the GA narrow form (defensive; ipa_actual_rp is currently empty
        # in this dataset).
        if notation_norm(ipa_actual_ga) != notation_norm(rp_narrow):
            return (False, "ga_allophony")

    # ---- Same-under-notation check ----
    if notation_norm(ipa) == notation_norm(rp_ipa):
        return (True, reason_when_same(ipa, rp_ipa))

    # ---- Different: find the best reason ----
    return (False, reason_when_different(word, ipa, rp_ipa))

# --- driver -----------------------------------------------------------------

SAME_REASONS = {"identical", "length_marking_only", "stress_marking_only",
                "dress_notation_only", "notation_composite"}

def process(items: list[dict], word_field: str = "w") -> dict:
    stats: dict[str, int] = {}
    for it in items:
        w = it.get(word_field, "")
        ipa = it.get("ipa", "")
        rp = it.get("rp_ipa", "")
        actual_ga = it.get("ipa_actual_ga")
        actual_rp = it.get("ipa_actual_rp")
        is_same, reason = classify(w, ipa, rp, actual_ga, actual_rp)
        it["ga_rp_same"] = is_same
        it["ga_rp_same_reason"] = reason
        stats[reason] = stats.get(reason, 0) + 1
    return stats

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wordlist", default="wordlist_GA_a1a2_plus_phonics.json")
    ap.add_argument("--connected", default="data/connected_speech.json")
    ap.add_argument("--weak", default="data/weak_forms.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default=None,
                    help="Optional path to write a JSON report of counts and samples.")
    args = ap.parse_args()

    all_report: dict = {}

    for label, path in [("wordlist", args.wordlist),
                        ("connected", args.connected),
                        ("weak", args.weak)]:
        p = Path(path)
        if not p.exists():
            print(f"skip (not found): {path}", file=sys.stderr)
            continue
        with p.open() as f:
            items = json.load(f)
        stats = process(items)
        total = len(items)
        same_n = sum(v for k, v in stats.items() if k in SAME_REASONS)
        print(f"\n{path}: {total} items — {same_n} same, {total - same_n} different")
        for reason, n in sorted(stats.items(), key=lambda x: -x[1]):
            tag = "SAME" if reason in SAME_REASONS else "DIFF"
            print(f"  [{tag}] {reason:25s} {n:5d}")

        all_report[label] = {"total": total, "same": same_n,
                             "different": total - same_n, "by_reason": stats}

        if not args.dry_run:
            with p.open("w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"  → wrote {path}")

    if args.report:
        with open(args.report, "w") as f:
            json.dump(all_report, f, ensure_ascii=False, indent=2)
        print(f"\nreport → {args.report}")

if __name__ == "__main__":
    main()
