#!/usr/bin/env bash
set -e
case "$1" in
  agents) ls .claude/agents | sed 's/\.md$//' | sort ;;
  commands) ls .claude/commands | sed 's/\.md$//' | sort ;;
  install-agent)
    NAME=$2
    echo "--> Scaffolding agent $NAME"
    cat > .claude/agents/$NAME.md <<'EOF'
---
name: NAME_PLACEHOLDER
description: Describe when this agent is useful.
tools: bash,python
---
System prompt here...
EOF
    sed -i "s/NAME_PLACEHOLDER/$NAME/" .claude/agents/$NAME.md
    ;;
  install-command)
    NAME=$2
    echo "--> Scaffolding command $NAME"
    cat > .claude/commands/$NAME.md <<'EOF'
---
name: NAME_PLACEHOLDER
description: Describe what this command does.
allowed-tools: ["bash","python"]
---
## NAME_PLACEHOLDER command
EOF
    sed -i "s/NAME_PLACEHOLDER/$NAME/" .claude/commands/$NAME.md
    ;;
  model) echo "Switching model to $2 (store this in .model_pref)" ;;
  *)
    echo "Usage: ccdk-cli {agents|commands|install-agent <name>|install-command <name>|model <name>}"
    exit 1
esac
