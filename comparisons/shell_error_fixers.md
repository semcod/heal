## heal vs Other Error-Fixing Tools

| Feature | heal | thefuck | shellcheck | explainshell |
|---------|:---:|:---:|:---:|:---:|
| **LLM-powered** | ✅ | — | — | — |
| **Understands context** | ✅ | partial | — | ✅ |
| **Fixes any error** | ✅ | common only | shell only | — |
| **Auto-applies fix** | — | ✅ | — | — |
| **Privacy protection** | ✅ | — | — | — |
| **Offline mode** | — | ✅ | ✅ | — |
| **Shell hook** | ✅ | ✅ | — | — |
| **Multi-language errors** | ✅ | — | bash only | bash only |
| **Python errors** | ✅ | — | — | — |
| **Docker errors** | ✅ | — | — | — |
| **Git errors** | ✅ | ✅ | — | — |
| **Database errors** | ✅ | — | — | — |
| **Interactive setup** | ✅ | ✅ | — | — |
| **Free** | API costs | ✅ | ✅ | ✅ |

## heal

**What it is:** LLM-powered CLI error fixer — sends shell errors to an AI model that explains and fixes them.

**Strengths:**
- Understands virtually any error from any tool
- Provides explanations, not just fixes
- Privacy-aware (data anonymization before LLM)
- Multi-provider support (OpenRouter, OpenAI, Anthropic, Google)
- Interactive configuration

**Weaknesses:**
- Requires internet + API key
- Has per-request cost (unless using free-tier models)
- Latency: 1–5 seconds per fix
- Cannot auto-execute the fix (safety by design)

**Best for:** Developers who encounter diverse, unfamiliar errors.

## thefuck

**GitHub:** [github.com/nvbn/thefuck](https://github.com/nvbn/thefuck)  
**Install:** `pip install thefuck`

**What it is:** Rule-based corrector that fixes previous shell commands. Type `fuck` after a failed command.

**Strengths:**
- Instant (no API call)
- Works offline
- Auto-applies the corrected command
- 100+ built-in rules (git, apt, pip, docker, etc.)

**Weaknesses:**
- Limited to known patterns — cannot reason about unknown errors
- Rule-based: misses nuance
- No explanation of why the fix works
- No privacy features
- Vulgar branding (not suitable for all environments)

**Best for:** Quick typo fixes and common command mistakes.

## shellcheck

**GitHub:** [github.com/koalaman/shellcheck](https://github.com/koalaman/shellcheck)  
**Install:** `apt install shellcheck`

**What it is:** Static analysis for shell scripts. Finds bugs, syntax issues, and best-practice violations.

**Strengths:**
- Extremely fast and accurate for shell syntax
- Works offline
- Integrates with editors (VS Code, Vim)
- CI/CD friendly

**Weaknesses:**
- Shell scripts only (bash/sh/zsh)
- Cannot fix runtime errors
- No understanding of application-level errors
- No interactive guidance

**Best for:** Shell script development and code review.

## explainshell

**Website:** [explainshell.com](https://explainshell.com)  
**GitHub:** [github.com/idank/explainshell](https://github.com/idank/explainshell)

**What it is:** Web tool that explains shell commands by parsing man pages.

**Strengths:**
- Beautiful visual breakdown of commands
- Educational — great for learning
- Based on actual man pages

**Weaknesses:**
- Web-only (no CLI)
- Explains commands, doesn't fix errors
- No runtime error handling
- No privacy features

**Best for:** Learning what shell commands do.

## When to Use What

| Scenario | Best Tool |
|----------|-----------|
| Typo in git/apt command | thefuck |
| Complex Python traceback | **heal** |
| Docker build failing | **heal** |
| Shell script has bugs | shellcheck |
| Unknown error from any tool | **heal** |
| Offline environment | thefuck / shellcheck |
| Learning shell syntax | explainshell |
| Production errors with PII | **heal** (with `--anonymize`) |

# 1. Use shellcheck for shell scripts
shellcheck deploy.sh

# 3. Use heal for complex errors
make build 2>&1 | heal

# 4. Use heal with privacy for production
production_script.py 2>&1 | heal --anonymize
```
