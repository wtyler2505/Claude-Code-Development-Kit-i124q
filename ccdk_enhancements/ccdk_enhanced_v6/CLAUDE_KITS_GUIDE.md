# Claude Usage Guide for CCDK Kits 1–6

## General conventions
* **Slash‑commands** live in `.claude/commands/*.md`.
* **Agents** in `.claude/agents/*.md`.
* **Hooks** in `.claude/hooks/*.ts` and registered in `.claude/settings.json`.
* Use `/full-context` first on a new project, then compose with context‑specific loaders.

---

## Kit 1 – Core Extensions
* `/security-audit`, `/run-tests`, `/git-create-pr`, `/context-frontend`
* Agents: backend‑architect, python‑engineer, ui-designer, security-auditor
* Hooks: session memory init/save
* CLI: `scripts/ccdk-cli.sh`

### How to use
```bash
/swarm-run "Implement login feature"
/security-audit .
```

---

## Kit 2 – Dependency & Performance
Commands: `update-dependencies`, `accessibility-review`, `profile-performance`, scaffold helpers.  
Agents: data-scientist, devops-troubleshooter, performance-engineer, project-task-planner.  
Hooks: pre‑compact summary, subagent stop log, post‑tool lint.

Usage tip: run `/update-dependencies` weekly; invoke `@performance-engineer` on slow endpoints.

---

## Kit 3 – Hive‑Mind & Memory
* Start persistent hive: `/hive-start mysession`
* Control via `scripts/ccdk-hive.py`
* Memory auto-injected every new session via SQLite.

---

## Kit 4 – Analytics, TTS, Swarm
* `/swarm-run "task"` parallel burst.
* Analytics log at `.ccd_analytics.log`, live dashboard at `python dashboard/app.py`.
* Voice notifications via OS TTS.

---

## Kit 5 – CI & Docs
* GitHub Actions workflow triggers on push.
* `/deploy-preview` kicks preview env.
* MkDocs site served with `mkdocs serve`.
* `postEdit` hook auto‑runs `gh workflow run`.

---

## Kit 6 – Web UI & Streaming Context (this kit)
* Start dashboard: `/webui-start` then open `http://localhost:7000`.
* UI lists agents, commands, live analytics, memory explorer (coming).
* Streaming hook injects tool output back into chain-of-thought.
* `auto-pr-reviewer` agent can be invoked in PR descriptions:
  ```
  @agent-auto-pr-reviewer please review
  ```

---

### Best Practices
1. Prime context loaders before heavy tasks.
2. Combine agents strategically: architect → coder → tester.
3. Keep hooks minimal—disable noisy ones in large teams.
4. Use analytics dashboard to identify slow tools or frequent failures.
5. Version control `.claude/` directory; keep secrets out of agents.

Enjoy the power!  – ARK
