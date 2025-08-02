# Claude Authentication Guide for CCDK i124q

## Important Clarification: Claude.ai vs Anthropic API

There are **two completely separate** Claude services:

### 1. **Claude.ai (Web Interface)**
- What you're using right now
- Subscription-based (Free, Pro, Team plans)
- Web-only interface at claude.ai
- **CANNOT be used programmatically**
- No API access

### 2. **Anthropic API**
- Separate developer service
- Requires API key from [console.anthropic.com](https://console.anthropic.com)
- Pay-per-token pricing
- Used by ThinkChain, Claude SDK, and other tools
- **Required for programmatic access**

## Authentication Methods for CCDK i124q

### Method 1: Bridge Mode (No API Key Required) ✅
CCDK i124q's innovation - use many features without an API key:

```bash
# Available without API key:
- Local tool execution
- File operations
- MCP server management
- Tool discovery
- Project configuration
- All installer features
```

### Method 2: Environment Variable
For tools that require the Anthropic API:

```bash
# Set in your shell profile
export ANTHROPIC_API_KEY="sk-ant-..."

# Or in project .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Method 3: Cloud Provider Integration
Use Claude through cloud providers:

```bash
# AWS Bedrock
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
gcloud auth login
```

## What Works Without API Key

### ✅ Full CCDK i124q Installation
- Ultimate installer (`install-ultimate.sh`)
- Project detection and configuration
- CLAUDE.PROJECT markers
- All configuration interfaces

### ✅ TaskMaster AI (Partial)
- Project structure creation
- Configuration files
- Rule profiles
- Local task management
- ❌ AI-powered task generation (needs API)

### ✅ SuperClaude Framework (Partial)
- Command structure
- Configuration
- Hooks system
- ❌ AI personas (needs API)

### ✅ ThinkChain Bridge Mode
- Local Python tools
- File operations
- Web scraping (local)
- MCP server management
- ❌ Claude thinking streams (needs API)

## Getting an API Key (If Needed)

### Option 1: Direct from Anthropic
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account (separate from Claude.ai)
3. Add payment method
4. Generate API key
5. $5 free credits for new accounts

### Option 2: API Proxy Services
Cost-effective alternatives:
- Services like laozhang.ai
- 70% cost savings
- $10 free credits
- Same API interface

### Option 3: Cloud Providers
- AWS Bedrock
- Google Vertex AI
- Azure (coming soon)

## Configuration in CCDK i124q

### For ThinkChain
```bash
# Run installer
bash install-ultimate.sh

# Navigate to ThinkChain config
tc → 2 (Configure API Key)

# Or set manually
echo "ANTHROPIC_API_KEY=sk-ant-..." > /c/Users/wtyle/thinkchain/.env
```

### For TaskMaster AI with API
```bash
# In your MCP configuration
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",
    "OPENROUTER_API_KEY": "sk-or-...",
    "PERPLEXITY_API_KEY": "pplx-..."
  }
}
```

## Frequently Asked Questions

### Q: Can I use my Claude.ai Pro/Team subscription for the API?
**A: No.** Claude.ai subscriptions and Anthropic API are completely separate services. Your Claude.ai subscription doesn't provide API access.

### Q: Do I need an API key to use CCDK i124q?
**A: No.** Most CCDK i124q features work without an API key thanks to Bridge Mode. You only need an API key for:
- AI-powered task generation in TaskMaster
- Claude thinking streams in ThinkChain
- AI personas in SuperClaude

### Q: What's the cheapest way to get API access?
**A: Options ranked by cost:**
1. Bridge Mode (free, no API needed)
2. API proxy services (~70% cheaper)
3. Direct Anthropic API ($5 free credits)
4. Cloud providers (enterprise pricing)

### Q: Can I share API keys between projects?
**A: Yes.** Set `ANTHROPIC_API_KEY` as a system environment variable to use across all projects.

## Security Best Practices

1. **Never commit API keys to Git**
   ```bash
   # Add to .gitignore
   .env
   *.key
   ```

2. **Use environment variables**
   ```bash
   # Not in code files
   api_key = os.getenv("ANTHROPIC_API_KEY")
   ```

3. **Rotate keys regularly**
   - Generate new keys monthly
   - Delete unused keys
   - Monitor usage

4. **Use project-specific keys**
   - Different keys for different projects
   - Easier to track usage
   - Better security isolation

## Summary

- **Claude.ai ≠ Anthropic API** - They're separate services
- **CCDK i124q works mostly without API keys** thanks to Bridge Mode
- **API keys only needed for AI features** like thinking streams
- **Multiple authentication options** available if needed
- **Security first** - Never expose keys in code

---

For more information:
- [CCDK i124q Documentation](https://github.com/wtyler2505/Claude-Code-Development-Kit-i124q)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude.ai](https://claude.ai) (Web interface)