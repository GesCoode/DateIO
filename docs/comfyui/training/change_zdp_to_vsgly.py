#!/usr/bin/env python3
"""Replace zdp / zdp person (and zpd spellings) with vsgly_id in caption .txt files.

Copy this file next to your photos, or pass the folder:

  python change_zdp_to_vsgly.py
  python change_zdp_to_vsgly.py "C:\\Users\\jeroe\\OneDrive\\Desktop\\Visagely\\Laptop\\TrainingSets\\TrainingSix\\zdp"
  python change_zdp_to_vsgly.py /workspace/flux_train/zdp
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NEW = "vsgly_id"

DEFAULTS = (
    Path("/workspace/flux_train/zdp"),
    Path("zdp"),
    Path("."),
)

ENCODINGS = ("utf-8-sig", "utf-8", "utf-16", "utf-16-le", "cp1252")


def read_text(path: Path) -> tuple[str, str]:
    last_err: Exception | None = None
    for enc in ENCODINGS:
        try:
            return path.read_text(encoding=enc), enc
        except UnicodeDecodeError as e:
            last_err = e
    raise last_err or UnicodeDecodeError("utf-8", b"", 0, 1, str(path))


def replace_triggers(text: str) -> str:
    out = text
    out = re.sub(r"zdp[_\-\s]+person", NEW, out, flags=re.IGNORECASE)
    out = re.sub(r"zpd[_\-\s]+person", NEW, out, flags=re.IGNORECASE)
    out = re.sub(r"zdp", NEW, out, flags=re.IGNORECASE)
    out = re.sub(r"zpd", NEW, out, flags=re.IGNORECASE)
    out = re.sub(r"vsgly_id(?:[_\-\s]+person)+", NEW, out, flags=re.IGNORECASE)
    return out


def txt_files(folder: Path) -> list[Path]:
    return sorted(p for p in folder.rglob("*.txt") if p.is_file())


def process_folder(folder: Path) -> int:
    folder = folder.expanduser().resolve()
    if not folder.is_dir():
        print(f"ERROR: not a folder: {folder}")
        return 1
    files = txt_files(folder)
    if not files:
        print(f"ERROR: no .txt files under {folder}")
        return 1
    print(f"Folder: {folder}")
    print(f"Found {len(files)} .txt file(s)\n")
    changed = 0
    for path in files:
        original, enc = read_text(path)
        updated = replace_triggers(original)
        rel = path.relative_to(folder)
        if updated == original:
            print(f"  skip  {rel}  (no zdp/zpd)")
            continue
        path.write_text(updated, encoding="utf-8")
        changed += 1
        print(f"  EDIT  {rel}  [{enc}]")
        print(f"        was: {original.strip()[:200]!r}")
        print(f"        now: {updated.strip()[:200]!r}")
    print(f"\nDone. {changed}/{len(files)} files written. Trigger is {NEW}.")
    return 0


def choose_folder(argv: list[str]) -> Path:
    if len(argv) >= 2:
        return Path(argv[1])
    for d in DEFAULTS:
        if d.is_dir() and txt_files(d):
            return d
    return Path(".")


def main() -> int:
    return process_folder(choose_folder(sys.argv))


if __name__ == "__main__":
    raise SystemExit(main())
