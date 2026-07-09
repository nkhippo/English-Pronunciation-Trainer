import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
import paths
# -*- coding: utf-8 -*-
"""Merge cs_rule.fil into connected_speech.json and weak_forms.json."""
import json

def merge(data_path, map_path, label):
    data = json.load(open(data_path, encoding="utf-8"))
    fil_map = json.load(open(map_path, encoding="utf-8"))
    applied, missing = 0, []
    for item in data:
        v = fil_map.get(item["id"])
        if v and v.strip():
            item.setdefault("cs_rule", {})["fil"] = v
            applied += 1
        else:
            missing.append(item["id"])
    json.dump(data, open(data_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{label}: applied={applied}, missing={missing}")

merge(str(paths.CONNECTED_SPEECH), str(paths.CS_RULE_FIL_CONNECTED), "CS")
merge(str(paths.WEAK_FORMS),        str(paths.CS_RULE_FIL_WEAK),      "WF")
