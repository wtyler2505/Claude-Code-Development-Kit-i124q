# CCDK Enhanced – Kit 5  (2025-08-01T14:41:38.800022Z)

### Highlights
* **GitHub Actions CI** (`.github/workflows/ci.yml`) – tests, lint, and docs build.
* **Slash‑commands** – `/deploy-preview` triggers preview workflow; `/generate-changelog` updates CHANGELOG.md.
* **postEdit CI hook** – auto‑kicks CI via `gh` CLI after each successful edit.
* **MkDocs scaffold** – `mkdocs.yml` + `docs/` ready for rich project documentation.
* **VS Code snippets** – frontmatter shortcut (`ccmd`) for rapid command creation.

### Usage
```bash
# run docs locally
pip install mkdocs mkdocs-material
mkdocs serve

# commit & push; GitHub Actions will run automatically
```
