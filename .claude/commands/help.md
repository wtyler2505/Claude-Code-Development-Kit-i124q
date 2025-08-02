---
name: help
description: Display help information about available Claude commands
instructions: |
  Show the user a comprehensive list of all available commands and their descriptions.
  Group commands by their enhancement kit for better organization.
---

Display the following help information:

# 🚀 Claude Code Development Kit - Enhanced Edition

## 📋 Available Commands

### Core Extensions (Kit 1)
- `/help` - Display this help message
- `/security-audit` - Run comprehensive security audit on codebase
- `/run-tests` - Execute test suite with detailed reporting
- `/git-create-pr` - Create GitHub pull request with AI-generated description
- `/context-frontend` - Load frontend-specific context (React, Vue, Angular)

### Dependency & Performance (Kit 2)
- `/update-dependencies` - Update all project dependencies safely
- `/accessibility-review` - Check accessibility compliance
- `/profile-performance` - Profile code performance and identify bottlenecks
- `/scaffold-*` - Various scaffolding commands for quick setup

### Hive Mind & Memory (Kit 3)
- `/hive-start <session>` - Start persistent memory session
- Memory automatically persists between sessions via SQLite

### Analytics & Swarm (Kit 4)
- `/swarm-run <task>` - Execute task with parallel agent swarm
- Analytics dashboard available at http://localhost:5005

### CI/CD & Docs (Kit 5)
- `/deploy-preview` - Deploy preview environment
- MkDocs documentation site

### Web UI & Streaming (Kit 6)
- `/webui-start` - Launch web dashboard (http://localhost:7000)
- Real-time streaming context injection

## 🤖 Available Agents
- `@backend-architect` - System design and architecture
- `@python-engineer` - Python development expert
- `@ui-designer` - UI/UX design specialist
- `@security-auditor` - Security analysis
- `@data-scientist` - Data analysis and ML
- `@devops-troubleshooter` - DevOps and infrastructure
- `@performance-engineer` - Performance optimization
- `@project-task-planner` - Project planning
- `@auto-pr-reviewer` - Automated PR reviews

## 🔧 Key Features
- Persistent memory across sessions
- Real-time analytics tracking
- Automated CI/CD integration
- Voice notifications (TTS)
- Web-based dashboard
- Parallel task execution

## 📚 Documentation
- Full guide: `.claude/docs/CLAUDE_KITS_GUIDE.md`
- Integration test log: `.claude/docs/integration-test-log.md`
- Test plans: `.claude/docs/MASTER_TEST_PLAN.md`

Type any command to get started!