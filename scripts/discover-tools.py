#!/usr/bin/env python3
import os, json, pathlib, sys
TOOLS_DIR = pathlib.Path('tools')
commands_dir = pathlib.Path('.claude/commands')
commands_dir.mkdir(parents=True, exist_ok=True)
for py in TOOLS_DIR.glob('*.py'):
    name = py.stem
    md = commands_dir/f'{name}.md'
    if not md.exists():
        md.write_text(f"""---
name: {name}
description: Auto-generated wrapper for tool {name}
allowed-tools: ["python"]
---
## {name} Tool

Calls local script `{py}` with provided arguments.
""", encoding='utf-8')
        print(f'Generated command for {name}')
