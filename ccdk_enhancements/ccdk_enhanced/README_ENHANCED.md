# CCDK Enhanced (Auto‑generated on 2025-08-01T14:29:22.054029Z)

This archive adds:

* **4 new slash‑commands** (`security-audit`, `run-tests`, `git-create-pr`, `context-frontend`)
* **4 specialist agents** (backend‑architect, python‑engineer, ui‑designer, security‑auditor)
* **3 TypeScript hooks** covering `sessionStart`, `postTask`, `preSearch`
* Updated `.claude/settings.json` registering new hooks
* Simple **CLI** script `scripts/ccdk-cli.sh` to list agents/commands
* SQLite memory DB initialised via `session-start-persist.ts` hook

To install:
```bash
unzip ccdk_enhanced.zip -d /path/to/your/project
```
