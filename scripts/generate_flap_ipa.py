#!/usr/bin/env python3
"""
Phase 2a: Rule-based generator for ipa_actual_ga (narrow IPA with GA allophonic
flap-t/d, glottal stop, syllabic n/l).

MECE rule set (GA, citation-form single words; no cross-word sandhi):

  R1. VtV / VdV flap
      /t/ or /d/, preceded by a vowel (optionally r), followed by an
      UNSTRESSED vowel  ->  /ɾ/
      e.g. party /ˈpɑrti/ -> /ˈpɑrɾi/ ; body /ˈbɑdi/ -> /ˈbɑɾi/

  R2. Syllabic /l/ (t/d + schwa + l at a following-unstressed environment)
      /t/ + ə + l  ->  /ɾ/ + l̩        (schwa deleted, t flaps)
      /d/ + ə + l  ->  /d/ + l̩        (schwa deleted, d stays; d+l cluster
                                        does not canonically flap because the
                                        following segment is not a vowel)
      e.g. bottle /ˈbɑtəl/ -> /ˈbɑɾl̩/ ; middle /ˈmɪdəl/ -> /ˈmɪdl̩/

  R3. Syllabic /n/ with glottal stop (t) / plain (d)
      /t/ + ə + n  ->  /ʔ/ + n̩        (schwa deleted, t glottalizes)
      /d/ + ə + n  ->  /d/ + n̩        (schwa deleted, d stays)
      e.g. button /ˈbʌtən/ -> /ˈbʌʔn̩/ ; garden /ˈɡɑrdən/ -> /ˈɡɑrdn̩/

  R4. VntV / VndV (nasal+stop flap) -- EXCLUDED from auto-generation.
      Speaker variation is high (winter: [ˈwɪɾɚ] vs [ˈwɪntɚ]); flagged for
      manual/Opus review, not auto-applied.

  R5. /t/ or /d/ followed by a STRESSED vowel, or preceded by a consonant
      other than /r/, or at a word boundary before a pause -> no change
      (excluded from candidates entirely).

No LLM is used in this script. Every word below is produced by pure regex /
tokenizer logic over the existing phonemic `ipa` field.
"""
import json
import re
import pathlib

WORDLIST = pathlib.Path("wordlist_GA_a1a2_plus_phonics.json")
OUT_CANDIDATES = pathlib.Path("phase2a_flap_candidates.json")
OUT_REVIEW = pathlib.Path("phase2a_review_needed.json")

# --- tokenizer: mirrors index.html MULTI_GA / VOWELS_GA -------------------
MULTI_GA = ["tʃ", "dʒ", "eɪ", "aɪ", "ɔɪ", "oʊ", "aʊ"]
VOWELS_GA = {"i", "ɪ", "ɛ", "æ", "ə", "ʌ", "ɑ", "ɔ", "ʊ", "u", "ɝ", "ɚ",
             "eɪ", "aɪ", "ɔɪ", "oʊ", "aʊ"}
STRESS = {"ˈ", "ˌ"}


def tokenize(raw):
    s = raw.strip("/")
    out = []
    i = 0
    while i < len(s):
        m = None
        for x in MULTI_GA:
            if s.startswith(x, i):
                m = x
                break
        if m:
            out.append(m)
            i += len(m)
        else:
            out.append(s[i])
            i += 1
    return out


def is_vowel(t):
    return t in VOWELS_GA


def next_real_index(tk, i):
    """Return index of next token skipping stress marks."""
    j = i + 1
    while j < len(tk) and tk[j] in STRESS:
        j += 1
    return j


def prev_real_index(tk, i):
    """Return index of previous token skipping stress marks."""
    j = i - 1
    while j >= 0 and tk[j] in STRESS:
        j -= 1
    return j


def analyze(ipa):
    """
    Returns (narrow_ipa:str|None, reason:str, flags:list[str])
    reason: which rule fired ('R1','R2','R3', 'R4-flagged', 'none')
    flags: list of ambiguity notes for manual review
    """
    tk = tokenize(ipa)
    n = len(tk)
    out = tk[:]  # working copy, will be rebuilt
    fired = []
    flags = []
    i = 0
    result_tokens = []
    consumed_upto = -1

    idx = 0
    while idx < n:
        if idx <= consumed_upto:
            idx += 1
            continue
        t = tk[idx]

        if t not in ("t", "d"):
            result_tokens.append(t)
            idx += 1
            continue

        # If a PRIMARY stress mark (ˈ) sits immediately before this t/d, this
        # consonant is the ONSET of the primary-stressed syllable (e.g.
        # "hotel" /hoʊˈtɛl/, "attack" /əˈtæk/, "cd" /ˌsiˈdi/) and must NOT
        # flap, regardless of what precedes the stress mark. This must be
        # checked before any prev_real_index lookup, since that helper skips
        # stress marks and would otherwise "see through" to the vowel before
        # them.
        #
        # SECONDARY stress (ˌ) does NOT block flapping in actual GA speech —
        # e.g. "thirty" /ˈθɝˌdi/ -> [ˈθɝɾi] ("thirdy"), "photo" /ˈfoʊˌtoʊ/ ->
        # [ˈfoʊɾoʊ] ("pho-doh"), "potato" /pəˈteɪˌtoʊ/ -> the *second* t
        # flaps ([pəˈteɪɾoʊ]) even though this wordlist marks that syllable
        # with ˌ (this dataset appears to use ˌ partly to mark full/tense
        # vowel quality, not strictly full secondary stress). Only ˈ blocks.
        if idx > 0 and tk[idx - 1] == "ˈ":
            result_tokens.append(t)
            idx += 1
            continue

        pj = prev_real_index(tk, idx)
        pre_r = False
        pv_idx = pj
        if pj >= 0 and tk[pj] == "r":
            pre_r = True
            pv_idx = prev_real_index(tk, pj)
        preceded_by_vowel = pv_idx >= 0 and is_vowel(tk[pv_idx])

        # preceded by nasal /n/ which is itself preceded by a vowel
        # (VnCV environment -> candidate for R4, handled separately below)
        preceded_by_n_after_vowel = False
        if pj >= 0 and tk[pj] == "n":
            pv2 = prev_real_index(tk, pj)
            if pv2 >= 0 and is_vowel(tk[pv2]):
                preceded_by_n_after_vowel = True

        nj = next_real_index(tk, idx)
        nxt = tk[nj] if nj < n else None
        # is next token immediately (no stress mark) meaning unstressed
        immediate_next = tk[idx + 1] if idx + 1 < n else None
        next_is_stress_mark = immediate_next in STRESS

        # --- R3: syllabic n:  t/d + ə + n (word-final cluster) ---
        # Checked BEFORE the R4 nasal-cluster check and BEFORE the general
        # preceded_by_vowel gate, because this pattern is self-contained
        # (defined by what FOLLOWS t/d) and applies regardless of whether
        # t/d itself is preceded by a vowel or by /n/ (e.g. "mountain"
        # /ˈmaʊntən/ has t preceded by n, not a vowel, yet still undergoes
        # R3: [ˈmaʊnʔn̩], not R4 — the following environment is a collapsing
        # schwa+n, not a full vowel nucleus, so R4's flap-uncertainty does
        # not apply here).
        if (nxt == "ə" and nj + 1 < n and tk[nj + 1] == "n"
                and not next_is_stress_mark):
            after_n = tk[nj + 2] if nj + 2 < n else None
            if after_n is None or not is_vowel(after_n):
                repl = "ʔ" if t == "t" else "d"
                result_tokens.append(repl)
                result_tokens.append("n̩")
                fired.append("R3")
                consumed_upto = nj + 1  # skip ə and n
                idx += 1
                continue

        # --- R2: syllabic l: t/d + ə + l (word-final cluster) ---
        # Same rationale as R3: self-contained, checked before R4/vowel gate.
        # When t is itself preceded by /n/ (e.g. "gentle" /ˈdʒɛntəl/), the
        # same nasal+t -> glottal-stop simplification used in R3 ("button",
        # "mountain") is applied for consistency, rather than flapping to
        # /ɾ/ — GA "gentle" is [ˈdʒɛnʔl̩] / [ˈdʒɛnl̩], not *[ˈdʒɛnɾl̩].
        if (nxt == "ə" and nj + 1 < n and tk[nj + 1] == "l"
                and not next_is_stress_mark):
            after_l = tk[nj + 2] if nj + 2 < n else None
            if after_l is None or not is_vowel(after_l):
                t_preceded_by_n = pj >= 0 and tk[pj] == "n"
                if t == "t":
                    repl = "ʔ" if t_preceded_by_n else "ɾ"
                else:
                    repl = "d"
                result_tokens.append(repl)
                result_tokens.append("l̩")
                fired.append("R2")
                consumed_upto = nj + 1
                idx += 1
                continue

        # --- R4: VntV / VndV — nasal cluster before a FULL unstressed vowel;
        # excluded from auto-generation (speaker variation is high) ---
        if preceded_by_n_after_vowel and nxt and is_vowel(nxt) and not next_is_stress_mark:
            flags.append("R4-VntV-excluded")
            result_tokens.append(t)  # leave unchanged
            idx += 1
            continue

        if not preceded_by_vowel:
            result_tokens.append(t)
            idx += 1
            continue

        # --- R1: plain VtV / VdV flap before unstressed vowel ---
        if nxt and is_vowel(nxt) and not next_is_stress_mark:
            result_tokens.append("ɾ")
            fired.append("R1")
            idx += 1
            continue

        # default: no change
        result_tokens.append(t)
        idx += 1

    narrow = "".join(result_tokens)
    narrow_ipa = "/" + narrow + "/"

    if not fired and not flags:
        return None, "none", []
    reason = "+".join(sorted(set(fired))) if fired else "none"
    return (narrow_ipa if fired else None), reason, flags


def main():
    data = json.loads(WORDLIST.read_text(encoding="utf-8"))

    candidates = []   # auto-generated, high confidence
    review_needed = []  # R4 flagged or other ambiguity

    for w in data:
        ipa = w.get("ipa", "")
        if not ipa:
            continue
        narrow, reason, flags = analyze(ipa)
        if narrow:
            candidates.append({
                "w": w["w"],
                "ipa": ipa,
                "ipa_actual_ga": narrow,
                "rule": reason,
            })
        if flags:
            review_needed.append({
                "w": w["w"],
                "ipa": ipa,
                "flags": flags,
            })

    OUT_CANDIDATES.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    OUT_REVIEW.write_text(
        json.dumps(review_needed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"Auto-generated candidates (R1/R2/R3): {len(candidates)}")
    print(f"Flagged for review (R4 VntV etc.):    {len(review_needed)}")

    from collections import Counter
    rule_counts = Counter(c["rule"] for c in candidates)
    print("\nBreakdown by rule:")
    for rule, cnt in sorted(rule_counts.items()):
        print(f"  {rule}: {cnt}")


if __name__ == "__main__":
    main()
