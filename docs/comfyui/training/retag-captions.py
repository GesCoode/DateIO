#!/usr/bin/env python3
"""Rewrite old identity triggers to vsgly_id in Kohya caption .txt files.

  python retag-captions.py "C:\\Users\\jeroe\\OneDrive\\Desktop\\Visagely\\Laptop\\TrainingSets\\TrainingSix\\zdp"
  python retag-captions.py /workspace/flux_train/zdp
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TRIGGER = "vsgly_id"
OLD = [
    r"zpd[_\s-]+person",
    r"zdp[_\s-]+person",
    r"ohwx[_\s-]+person",
    r"ohwx",
    r"zpd",
    r"zdp",
]


def compile_old() -> list[re.Pattern[str]]:
    # Longer phrases first so "zpd person" is not left as "vsgly_id person"
    pats = []
    for raw in OLD:
        pats.append(re.compile(rf"\b{raw}\b", re.IGNORECASE))
    return pats


def rewrite(text: str, pats: list[re.Pattern[str]]) -> str:
    out = text
    for pat in pats:
        out = pat.sub(TRIGGER, out)
    out = re.sub(rf"\b{re.escape(TRIGGER)}(?:\s+person)+\b", TRIGGER, out, flags=re.IGNORECASE)
    nl = "\n" if text.endswith("\n") else ""
    out = out.rstrip("\n")
    body = re.sub(rf"\b{re.escape(TRIGGER)}\b[,]?\s*", "", out, flags=re.IGNORECASE)
    body = re.sub(r"\s{2,}", " ", body).strip(" ,;")
    if not body:
        return f"{TRIGGER}{nl}"
    return f"{TRIGGER}, {body}{nl}"


def main() -> int:
    p = argparse.ArgumentParser(description="Replace old LoRA triggers with vsgly_id")
    p.add_argument("folder", type=Path, help="Folder with photo_##.txt captions")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    folder: Path = args.folder
    if not folder.is_dir():
        print(f"not a directory: {folder}", file=sys.stderr)
        return 1
    pats = compile_old()
    files = sorted(folder.glob("*.txt"))
    if not files:
        print(f"no .txt captions in {folder}", file=sys.stderr)
        return 1
    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        updated = rewrite(original, pats)
        if updated == original:
            continue
        changed += 1
        print(f"--- {f.name}")
        print(f"  was: {original.strip()[:160]}")
        print(f"  now: {updated.strip()[:160]}")
        if not args.dry_run:
            f.write_text(updated, encoding="utf-8")
    print(f"==> {changed}/{len(files)} captions {'would change' if args.dry_run else 'updated'} → {TRIGGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
