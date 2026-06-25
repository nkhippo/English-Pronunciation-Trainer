"""Rule-based GA IPA → RP IPA conversion (STEP5 offline fallback)."""
from __future__ import annotations

MULTI = ["tʃ", "dʒ", "eɪ", "aɪ", "ɔɪ", "oʊ", "aʊ"]

BATH_WORDS = {
    "after", "answer", "ask", "bath", "branch", "castle", "chance", "class",
    "dance", "example", "fast", "glass", "graph", "half", "laugh", "last",
    "master", "pass", "past", "path", "plant", "rather", "staff",
}

OVERRIDES = {
    "Z": "/zɛd/",
    "R": "/ɑː/",
}


def tokenize(ipa: str) -> list[str]:
    s = ipa.replace("/", "").replace("ˈ", "ˈ").replace("ˌ", "ˌ")
    out: list[str] = []
    i = 0
    while i < len(s):
        matched = None
        for x in MULTI:
            if s.startswith(x, i):
                matched = x
                break
        if matched:
            out.append(matched)
            i += len(matched)
        else:
            out.append(s[i])
            i += 1
    return out


def detokenize(tokens: list[str]) -> str:
    return "/" + "".join(tokens) + "/"


def ga_to_rp(word: str, ga_ipa: str) -> str:
    if word in OVERRIDES:
        return OVERRIDES[word]

    inner = ga_ipa.strip("/")

    # TRAP-BATH before other vowel rules
    if word in BATH_WORDS:
        inner = inner.replace("æ", "ɑː")

    # Non-rhotic and diphthong+r (longest first)
    for src, dst in [
        ("aʊr", "aʊə"),
        ("aɪr", "aɪə"),
        ("ɔɪr", "ɔɪə"),
        ("eɪr", "eɪə"),
        ("ɑr", "ɑː"),
        ("ɔr", "ɔː"),
        ("ɪr", "ɪə"),
        ("ɛr", "eə"),
        ("ʊr", "ʊə"),
        ("ɝ", "ɜː"),
        ("ɚ", "ə"),
        ("oʊ", "əʊ"),
    ]:
        inner = inner.replace(src, dst)

    tokens = tokenize("/" + inner + "/")
    mapped: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        if tok in ("ˈ", "ˌ"):
            mapped.append(tok)
            i += 1
            continue
        if tok == "ɑ" and nxt == "ː":
            mapped.extend(["ɑ", "ː"])
            i += 2
            continue
        if tok == "ɔ" and nxt == "ː":
            mapped.extend(["ɔ", "ː"])
            i += 2
            continue
        if tok == "i":
            mapped.append("iː")
        elif tok == "u":
            mapped.append("uː")
        elif tok == "ɔ":
            mapped.append("ɔː")
        elif tok == "ɛ":
            mapped.append("e")
        elif tok == "ɑ":
            mapped.append("ɒ")
        elif tok == "r":
            i += 1
            continue
        else:
            mapped.append(tok)
        i += 1

    rp = detokenize(mapped)
    if not rp.startswith("/") or len(rp) < 3:
        return ga_ipa
    return rp
