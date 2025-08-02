# Agent Selection Guide

*Created by Tyler Walker (@wtyler2505) & Claude*

## Quick Agent Picker

### 🔧 **claude-coder** - General Development
**Use when:** Writing code, debugging, refactoring
- ✅ Multi-language support
- ✅ Code analysis & optimization
- ✅ Bug fixing & testing
- ✅ Documentation generation

### 🎨 **cursor-composer** - UI/UX Development  
**Use when:** Building interfaces, styling, user experience
- ✅ React/Vue/Angular components
- ✅ CSS/Tailwind styling
- ✅ Responsive design
- ✅ Accessibility compliance

### 📊 **data-analyst** - Data Processing
**Use when:** Working with data, analytics, reporting
- ✅ CSV/JSON processing
- ✅ Data visualization
- ✅ Statistical analysis
- ✅ Report generation

### 🚀 **devops-engineer** - Infrastructure
**Use when:** Deployment, CI/CD, server management
- ✅ Docker/containerization
- ✅ Cloud deployment
- ✅ CI/CD pipelines
- ✅ Environment setup

## Decision Matrix

| Task Type | Primary Agent | Backup Agent |
|-----------|---------------|--------------|
| API Development | claude-coder | devops-engineer |
| Frontend UI | cursor-composer | claude-coder |
| Database Work | data-analyst | claude-coder |
| Testing | claude-coder | devops-engineer |
| Deployment | devops-engineer | claude-coder |
| Analytics | data-analyst | claude-coder |
| Documentation | claude-coder | cursor-composer |

## Agent Capabilities

### Performance Tiers
- **High Performance:** claude-coder, cursor-composer
- **Specialized:** data-analyst, devops-engineer
- **Universal Fallback:** claude-coder

### Resource Usage
- **Light:** data-analyst
- **Medium:** cursor-composer, devops-engineer  
- **Heavy:** claude-coder (full feature set)

## Quick Start Commands

```bash
# Start most versatile agent
ccdk agent start claude-coder

# Start for UI work
ccdk agent start cursor-composer

# Start for data tasks
ccdk agent start data-analyst

# Start for deployment
ccdk agent start devops-engineer
```