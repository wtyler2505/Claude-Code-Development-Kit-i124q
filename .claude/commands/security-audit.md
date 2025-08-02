---
name: security-audit
description: Run dependency and static‑analysis vulnerability scans, summarise critical findings and propose fixes.
allowed-tools: ["bash","python"]
argument-hint: "[path(optional)]"
---
## Security Audit

**What it does**

1. Detects project language & package manager
2. Runs appropriate scanners (`npm audit`, `pip-audit`, Bandit, Trivy, etc.)
3. Summarises CVEs, ranks severity, suggests upgrade or patch steps.

**WHY?** Keeps your codebase safe and compliant automatically.
