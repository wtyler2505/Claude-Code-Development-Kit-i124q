---
name: deploy-preview
description: Trigger GitHub Action to deploy preview site for current branch.
allowed-tools: ["bash"]
---
Runs `gh workflow run deploy-preview.yml -F ref=$BRANCH`.
