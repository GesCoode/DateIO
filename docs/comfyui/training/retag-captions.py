#!/usr/bin/env python3
"""Back-compat wrapper. Use change_zdp_to_vsgly.py."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("change_zdp_to_vsgly.py")), run_name="__main__")
