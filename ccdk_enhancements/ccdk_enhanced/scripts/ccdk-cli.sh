#!/usr/bin/env bash
set -e
COMMAND=$1
case "$COMMAND" in
  agents)
    echo "Available agents:"
    ls .claude/agents | sed 's/\.md$//' | sort
    ;;
  commands)
    echo "Available commands:"
    ls .claude/commands | sed 's/\.md$//' | sort
    ;;
  model)
    echo "Switching model to $2 (not implemented)"
    ;;
  *)
    echo "Usage: ccdk-cli {agents|commands|model <name>}"
    exit 1
    ;;
esac
