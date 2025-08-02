---
name: run-tests
description: Generate and execute unit/integration tests, report coverage and failing cases.
allowed-tools: ["bash","python"]
argument-hint: "[test_path(optional)]"
---
## Run Tests

1. Auto‑detects test framework (pytest, jest, etc.)
2. Generates missing test stubs if coverage < 80 %
3. Executes tests and returns a colourised coverage report.
