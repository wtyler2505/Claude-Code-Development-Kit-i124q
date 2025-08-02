---
name: hive-start
description: Launch a persistent Hive‑Mind session (Queen + workers) with shared memory.
argument-hint: "[session-name]"
---
## Hive‑Mind Mode

Starts **Queen** coordinator plus default workers: architect, coder, tester, security.  
Stores session state in `.ccd_hive/<session>/` and shares SQLite memory across agents.
