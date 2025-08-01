# CCDK Enhanced – Kit 3 (Hive‑Mind & Memory)  2025-08-01T14:37:34.173548Z

### New Features
* **Hive‑Mind orchestration** – `scripts/ccdk-hive.py` + `/hive-start|status|stop` commands.
* **Persistent shared memory** – SQLite DB injected at session start / saved at end.
* **Additional hooks** – sessionStart/sessionEnd context injection + memory save.
* **Dynamic tool discovery** – `scripts/discover-tools.py` scans `tools/` and auto‑wraps scripts as slash‑commands.
* **Model router config** – `model_router.json` supports Anthropic and OpenAI models.
* **Sample local tool** – `tools/echo.py` to demonstrate discovery.

### Install
```bash
unzip ccdk_enhanced_v3.zip -d your/project
python scripts/discover-tools.py   # create commands for local tools
```
