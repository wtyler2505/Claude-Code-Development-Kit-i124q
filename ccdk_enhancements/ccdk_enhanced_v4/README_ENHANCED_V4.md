# CCDK Enhanced – Kit 4  (2025-08-01T14:39:34.115685Z)

### Additions
* **Swarm‑Run** command for fast parallel expert bursts
* **Analytics hook** (`postToolUse-analytics.ts`) logs every tool use to `.ccd_analytics.log`
* **TTS notifications** hook reads notifications aloud (`say` or `espeak`)
* **Three new agents**: accessibility‑specialist, blockchain‑developer, ai‑engineer
* **Flask dashboard** (`dashboard/app.py`) shows hive sessions and recent tool metrics at http://localhost:5005

### Quick start
```bash
pip install flask
python dashboard/app.py   # open browser
```
