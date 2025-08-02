# CCDK i124q Components Reference

*Created by Tyler Walker (@wtyler2505) & Claude*

This document provides a comprehensive reference for all commands, agents, and hooks available in CCDK i124q.

## Table of Contents
- [Commands](#commands)
- [Agents](#agents)
- [Hooks](#hooks)

---

## Commands

### Original CCDK Commands

#### `/full-context`
**Purpose**: Comprehensive context gathering and analysis  
**Source**: Original CCDK  
**Usage**: `/full-context "analyze authentication implementation"`  
**Description**: Auto-loads project documentation and spawns specialized agents to provide comprehensive analysis of the specified topic.

#### `/code-review`
**Purpose**: Multi-perspective code analysis  
**Source**: Original CCDK  
**Usage**: `/code-review "review the API endpoints"`  
**Description**: Analyzes code from security, performance, architectural, and integration perspectives.

#### `/update-docs`
**Purpose**: Documentation synchronization  
**Source**: Original CCDK  
**Usage**: `/update-docs "document authentication changes"`  
**Description**: Updates affected documentation files across all tiers, maintaining currency with implementation.

#### `/create-docs`
**Purpose**: Initial documentation generation  
**Source**: Original CCDK  
**Usage**: `/create-docs "backend/auth/CONTEXT.md"`  
**Description**: Creates new component or feature-level documentation files.

#### `/refactor`
**Purpose**: Intelligent code restructuring  
**Source**: Original CCDK  
**Usage**: `/refactor "improve error handling in API layer"`  
**Description**: Analyzes and refactors code while maintaining functionality.

#### `/handoff`
**Purpose**: Session context preservation  
**Source**: Original CCDK  
**Usage**: `/handoff`  
**Description**: Creates a comprehensive summary for session continuity.

#### `/gemini-consult`
**Purpose**: Deep architectural consultation  
**Source**: Original CCDK (v2.1.0)  
**Usage**: `/gemini-consult "design a caching strategy"`  
**Description**: Initiates iterative conversation with Gemini MCP for complex problem-solving.

### Enhancement Kit 1 Commands

#### `/security-audit`
**Purpose**: Security vulnerability scanning  
**Source**: Kit 1  
**Usage**: `/security-audit .`  
**Description**: Performs comprehensive security analysis of the codebase.

#### `/run-tests`
**Purpose**: Test execution and analysis  
**Source**: Kit 1  
**Usage**: `/run-tests`  
**Description**: Runs test suite and provides detailed analysis of results.

#### `/git-create-pr`
**Purpose**: Automated PR creation  
**Source**: Kit 1  
**Usage**: `/git-create-pr "feat: add user authentication"`  
**Description**: Creates GitHub pull request with proper formatting.

#### `/context-frontend`
**Purpose**: Frontend-specific context loading  
**Source**: Kit 1  
**Usage**: `/context-frontend`  
**Description**: Loads frontend-specific documentation and patterns.

### Enhancement Kit 2 Commands

#### `/update-dependencies`
**Purpose**: Dependency management  
**Source**: Kit 2  
**Usage**: `/update-dependencies`  
**Description**: Analyzes and updates project dependencies safely.

#### `/accessibility-review`
**Purpose**: WCAG compliance checking  
**Source**: Kit 2  
**Usage**: `/accessibility-review`  
**Description**: Reviews UI components for accessibility compliance.

#### `/profile-performance`
**Purpose**: Performance analysis  
**Source**: Kit 2  
**Usage**: `/profile-performance "api/users endpoint"`  
**Description**: Profiles code performance and suggests optimizations.

#### `/scaffold-agent`
**Purpose**: Agent template creation  
**Source**: Kit 2  
**Usage**: `/scaffold-agent "database-specialist"`  
**Description**: Creates new agent template with standard structure.

#### `/scaffold-command`
**Purpose**: Command template creation  
**Source**: Kit 2  
**Usage**: `/scaffold-command "analyze-database"`  
**Description**: Creates new command template.

### Enhancement Kit 3 Commands

#### `/hive-start`
**Purpose**: Start persistent hive session  
**Source**: Kit 3  
**Usage**: `/hive-start mysession`  
**Description**: Initiates Queen coordinator with default workers.

#### `/hive-status`
**Purpose**: Check hive session status  
**Source**: Kit 3  
**Usage**: `/hive-status`  
**Description**: Shows current hive session information.

#### `/hive-stop`
**Purpose**: Stop hive session  
**Source**: Kit 3  
**Usage**: `/hive-stop`  
**Description**: Terminates active hive session.

### Enhancement Kit 4 Commands

#### `/swarm-run`
**Purpose**: Parallel multi-agent execution  
**Source**: Kit 4  
**Usage**: `/swarm-run "implement login feature"`  
**Description**: Spawns transient swarm of specialists for single task.

### Enhancement Kit 5 Commands

#### `/deploy-preview`
**Purpose**: Deploy preview environment  
**Source**: Kit 5  
**Usage**: `/deploy-preview`  
**Description**: Creates preview deployment for testing.

#### `/generate-changelog`
**Purpose**: Automated changelog generation  
**Source**: Kit 5  
**Usage**: `/generate-changelog`  
**Description**: Generates changelog from commit history.

### Enhancement Kit 6 Commands

#### `/webui-start`
**Purpose**: Start web dashboard  
**Source**: Kit 6  
**Usage**: `/webui-start`  
**Description**: Launches interactive web UI on http://localhost:7000.

### Utility Commands

#### `/echo`
**Purpose**: Simple echo test  
**Usage**: `/echo "test message"`  
**Description**: Tests command system functionality.

#### `/help`
**Purpose**: Display available commands  
**Usage**: `/help`  
**Description**: Shows list of all available commands.

---

## Agents

### Kit 1 Agents

#### `backend-architect`
**Specialization**: Scalable backend architectures, API contracts, data models  
**Tools**: bash, python  
**Best For**: High-level design, technology selection, microservice boundaries

#### `python-engineer`
**Specialization**: Idiomatic Python code with type hints and tests  
**Tools**: bash, python  
**Best For**: Python implementation, testing, optimization

#### `ui-designer`
**Specialization**: Accessible, responsive interfaces with modern frameworks  
**Tools**: All available tools  
**Best For**: Frontend architecture, component design, UX patterns

#### `security-auditor`
**Specialization**: Security reviews covering OWASP Top 10 and supply chain risks  
**Tools**: bash, python  
**Best For**: Vulnerability assessment, security best practices

### Kit 2 Agents

#### `data-scientist`
**Specialization**: SQL & analytics for data insights and visualizations  
**Tools**: bash, python  
**Best For**: Data analysis, visualization, ML model development

#### `devops-troubleshooter`
**Specialization**: Debug CI/CD pipelines, analyze logs, fix deployment issues  
**Tools**: All available tools  
**Best For**: Infrastructure problems, deployment failures, monitoring

#### `performance-engineer`
**Specialization**: Profile applications, optimize code paths and DB queries  
**Tools**: bash, python  
**Best For**: Performance bottlenecks, optimization strategies

#### `project-task-planner`
**Specialization**: Break down epics into tasks with priorities and estimations  
**Tools**: All available tools  
**Best For**: Project planning, task decomposition, timeline estimation

### Kit 3 Agents

#### `ai-engineer`
**Specialization**: Build RAG pipelines, model serving, and prompt engineering  
**Tools**: All available tools  
**Best For**: AI/ML integration, prompt optimization, model deployment

#### `accessibility-specialist`
**Specialization**: Ensure WCAG compliance and usability for assistive technologies  
**Tools**: All available tools  
**Best For**: Accessibility audits, ARIA implementation, screen reader optimization

#### `blockchain-developer`
**Specialization**: Design and implement smart contracts, audits, and tests  
**Tools**: All available tools  
**Best For**: Smart contract development, Web3 integration, DApp architecture

### Kit 6 Agents

#### `auto-pr-reviewer`
**Specialization**: Automatically review GitHub PRs using review guidelines  
**Tools**: bash  
**Best For**: Automated PR reviews, code quality checks  
**Activation**: Include `@agent-auto-pr-reviewer please review` in PR description

---

## Hooks

### Session Management Hooks

#### `session-start-load-memory.ts`
**Trigger**: Session start  
**Purpose**: Load persistent memory from SQLite database  
**Source**: Kit 1

#### `session-end-save-memory.ts`
**Trigger**: Session end  
**Purpose**: Save session memory to SQLite database  
**Source**: Kit 1

#### `session-start-persist.ts`
**Trigger**: Session start  
**Purpose**: Initialize SQLite memory database  
**Source**: Kit 1

### Code Quality Hooks

#### `post-tool-lint.ts`
**Trigger**: After tool execution  
**Purpose**: Run linting on modified files  
**Source**: Kit 2

#### `postEdit-ci.ts`
**Trigger**: After file edit  
**Purpose**: Trigger CI/CD workflows  
**Source**: Kit 5

### Analytics & Monitoring Hooks

#### `postToolUse-analytics.ts`
**Trigger**: After any tool use  
**Purpose**: Log tool usage for analytics  
**Source**: Kit 4

#### `pre-search-logger.ts`
**Trigger**: Before search operations  
**Purpose**: Log search patterns and queries  
**Source**: Kit 1

#### `post-task-summary.ts`
**Trigger**: After task completion  
**Purpose**: Generate task completion summary  
**Source**: Kit 1

### Notification Hooks

#### `notification-tts.ts`
**Trigger**: Configurable events  
**Purpose**: Text-to-speech notifications  
**Source**: Kit 4

#### `subagent-stop-notify.ts`
**Trigger**: Sub-agent completion  
**Purpose**: Notify when sub-agents finish  
**Source**: Kit 2

### Context Enhancement Hooks

#### `postToolUse-streamInject.ts`
**Trigger**: After tool output  
**Purpose**: Inject tool output into AI context stream  
**Source**: Kit 6

#### `pre-compact-summary.ts`
**Trigger**: Before context compaction  
**Purpose**: Create summary before context reduction  
**Source**: Kit 2

### Infrastructure Hooks

#### `hook-wrapper.js`
**Purpose**: Fault-tolerant wrapper for all hooks  
**Description**: Ensures graceful degradation on hook failures  
**Source**: Kit 3

#### `test-runner.js`
**Purpose**: Hook testing infrastructure  
**Description**: Validates hook functionality  
**Source**: Kit 3

#### `lib.ts`
**Purpose**: Shared hook utilities  
**Description**: Common functions for all hooks  
**Source**: Kit 1

---

## Usage Patterns

### Multi-Agent Workflows
```bash
# Complex feature implementation
/swarm-run "implement OAuth2 authentication"

# Comprehensive analysis
/full-context "analyze database performance issues"
```

### Quality Assurance
```bash
# Security review
/security-audit .

# Performance analysis
/profile-performance "critical API endpoints"

# Accessibility check
/accessibility-review
```

### Project Management
```bash
# Start hive session
/hive-start feature-development

# Check progress
/hive-status

# Generate documentation
/update-docs "document new features"
```

### Development Workflow
```bash
# Update dependencies safely
/update-dependencies

# Create PR with proper format
/git-create-pr "feat: add caching layer"

# Deploy preview
/deploy-preview
```

---

*This reference is maintained by Tyler Walker (@wtyler2505) & Claude as part of CCDK i124q*