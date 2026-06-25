#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_rp_ipa.py
Claude API を使って全2840語のRP発音記号を生成する。
- バッチサイズ: 80語
- 進捗は rp_progress.json に随時保存（中断再開可能）
- 完成後 rp_complete.json に出力
"""

import json, time, re, sys, os

# ── 設定 ──────────────────────────────────────────
BATCH_SIZE   = 80
PROGRESS_FILE = "rp_progress.json"
COMPLETE_FILE = "rp_complete.json"
INPUT_FILE    = "wordlist_GA_a1a2_plus_phonics.json"
# ──────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precise British English phonetician. 
Your task: given a list of English words WITH their General American (GA) IPA, 
output the Received Pronunciation (RP / BBC English) IPA for each word.

STRICT RULES for RP transcription:
1. Use BROAD transcription (same level of detail as GA input).
2. Use ː for long vowels: iː uː ɑː ɔː ɜː
3. RP is NON-RHOTIC: drop /r/ after vowels (car → /kɑː/, water → /ˈwɔːtə/).
   Exception: linking-r before vowels may be shown but is NOT required here.
4. Vowel inventory differences from GA:
   GA /ɑ/ (hot)  → RP /ɒ/      (short rounded o)
   GA /i/        → RP /iː/
   GA /u/        → RP /uː/
   GA /ɔ/        → RP /ɔː/
   GA /oʊ/       → RP /əʊ/
   GA /ɝ/        → RP /ɜː/
   GA /ɚ/        → RP /ə/  (syllabic schwa, r dropped)
   GA /æ/ (TRAP) → RP /æ/  (same)
   GA /ʌ/ (STRUT)→ RP /ʌ/  (same)
   GA /ɛ/ (DRESS)→ RP /e/  (RP uses /e/ not /ɛ/)
   GA /ɪ/        → RP /ɪ/  (same)
   GA /ʊ/        → RP /ʊ/  (same)
   GA /ə/        → RP /ə/  (same)
   GA /eɪ/       → RP /eɪ/ (same)
   GA /aɪ/       → RP /aɪ/ (same)
   GA /aʊ/       → RP /aʊ/ (same)
   GA /ɔɪ/       → RP /ɔɪ/ (same)
5. Stress marks: ˈ (primary) ˌ (secondary) placed before the stressed syllable onset.
   Monosyllables: omit stress marks.
6. Wrap each IPA in /slashes/.
7. CODA-r rule examples:
   car   GA:/kɑr/   → RP:/kɑː/
   word  GA:/wɝd/   → RP:/wɜːd/
   water GA:/ˈwɔtɚ/ → RP:/ˈwɔːtə/
   more  GA:/mɔr/   → RP:/mɔː/
   near  GA:/nɪr/   → RP:/nɪə/
   care  GA:/kɛr/   → RP:/keə/
   poor  GA:/pʊr/   → RP:/pʊə/ or /pɔː/
   fire  GA:/faɪr/  → RP:/faɪə/
   hour  GA:/aʊr/   → RP:/aʊə/
8. TRAP-BATH split: words like 'path','bath','grass','ask','dance','can't','aren't'
   use /ɑː/ in RP (not /æ/). This also applies to 'after','answer','example','class',
   'last','past','fast','glass','half','laugh','rather','chance','plant','branch','castle'.
9. ALPHABET LETTER NAMES (single uppercase letter as the word): most are same as GA
   but TWO differ in RP:
     Z  GA:/zi/  → RP:/zɛd/   (zed, NOT zee)
     R  GA:/ɑr/  → RP:/ɑː/    (r dropped)
   Others apply normal rules: H /eɪtʃ/, W /ˈdʌbəljuː/, A /eɪ/, etc.
10. CONTRACTIONS keep citation/strong form, apply non-rhotic + vowel rules:
     you're GA:/jʊr/  → RP:/jʊə/ (or /jɔː/)
     they're GA:/ðɛr/ → RP:/ðeə/
     we're  GA:/wir/  → RP:/wɪə/
     aren't GA:/ˈɑrənt/ → RP:/ɑːnt/  (TRAP-BATH + r drop)
     weren't GA:/ˈwɝənt/ → RP:/wɜːnt/
11. CASUAL reduced forms (gonna, sorta, outta...) keep their reduced shape, apply rules:
     sorta GA:/ˈsɔrtə/ → RP:/ˈsɔːtə/    gonna GA:/ˈɡɑnə/ → RP:/ˈɡɒnə/
     gotta GA:/ˈɡɑtə/ → RP:/ˈɡɒtə/      outta GA:/ˈaʊtə/ → RP:/ˈaʊtə/
12. Output ONLY a JSON object mapping word → RP IPA. No explanation. No markdown.
   Example: {"cat":"/kæt/","water":"/ˈwɔːtə/","bird":"/bɜːd/"}"""

def make_user_prompt(batch):
    lines = [f'{e["w"]} (GA: {e["ipa"]})' for e in batch]
    return "Convert these words to RP IPA:\n" + "\n".join(lines)

def call_api(batch):
    import urllib.request, urllib.error
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("環境変数 ANTHROPIC_API_KEY が未設定。\n実行前に: export ANTHROPIC_API_KEY=\'sk-ant-...\'")
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 2048,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": make_user_prompt(batch)}]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API Error {e.code}: {e.read().decode()[:200]}")
    raw = body["content"][0]["text"].strip()
    raw = re.sub(r'^```[a-z]*\n?', '', raw)
    raw = re.sub(r'\n?```$', '', raw)
    m = re.search(r'\{[\s\S]+\}', raw)
    if m: raw = m.group(0)
    return json.loads(raw)

def validate_rp(word, rp_ipa):
    """Basic sanity check: must be /…/, contain at least one IPA char."""
    if not rp_ipa: return False
    if not (rp_ipa.startswith('/') and rp_ipa.endswith('/')): return False
    inner = rp_ipa[1:-1]
    if len(inner) < 1: return False
    return True

def main():
    data = json.load(open(INPUT_FILE, encoding='utf-8'))
    total = len(data)

    # load progress
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        progress = json.load(open(PROGRESS_FILE, encoding='utf-8'))
        print(f"再開: 既存 {len(progress)} 語ロード済み")

    remaining = [e for e in data if e['w'] not in progress]
    print(f"残り {len(remaining)} 語 / 全 {total} 語")
    print(f"バッチ数: {-(-len(remaining)//BATCH_SIZE)}")

    failed = []
    batch_num = 0

    for i in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[i:i+BATCH_SIZE]
        batch_num += 1
        words_str = ', '.join(e['w'] for e in batch[:5]) + '...'
        print(f"\nバッチ {batch_num} ({len(batch)}語): {words_str}", flush=True)

        for attempt in range(3):
            try:
                result = call_api(batch)
                # validate and store
                ok, ng = 0, 0
                for e in batch:
                    w = e['w']
                    rp = result.get(w)
                    if rp and validate_rp(w, rp):
                        progress[w] = rp; ok += 1
                    else:
                        ng += 1
                        print(f"  NG: {w} → {rp}")
                        failed.append(w)
                print(f"  ✓ {ok}語OK / {ng}語NG", flush=True)
                # save progress after every batch
                json.dump(progress, open(PROGRESS_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
                time.sleep(0.5)
                break
            except Exception as ex:
                print(f"  エラー (attempt {attempt+1}/3): {ex}", flush=True)
                if attempt < 2: time.sleep(3 * (attempt+1))
                else: failed.extend(e['w'] for e in batch)

    print(f"\n=== 完了 ===")
    print(f"成功: {len(progress)} 語 / 全 {total} 語")
    print(f"失敗: {len(failed)} 語: {failed[:20]}")

    # merge into final output
    out = []
    for e in data:
        row = dict(e)
        row['rp_ipa'] = progress.get(e['w'])
        out.append(row)
    json.dump(out, open(COMPLETE_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"→ {COMPLETE_FILE} 出力完了 ({len(out)}語)")

if __name__ == '__main__':
    main()
