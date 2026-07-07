# Heal 🩺

[![PyPI version](https://img.shields.io/pypi/v/heal.svg)](https://pypi.org/project/heal/)
[![Python versions](https://img.shields.io/pypi/pyversions/heal.svg)](https://pypi.org/project/heal/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/tests-71%20passed-brightgreen.svg)](#testing)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](#docker-testing)
[![Privacy](https://img.shields.io/badge/privacy-6%20backends-purple.svg)](#privacy-protection)


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.25-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$68.95-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-9.1h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $68.9540 (29 commits)
- 👤 **Human dev:** ~$910 (9.1h @ $100/h, 30min dedup)

Generated on 2026-07-07 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

**LLM-powered shell error fixing** — Your AI assistant for debugging and fixing command-line errors instantly, with built-in privacy protection.

## Installation

```bash
pip install heal

# With full privacy protection (detect-secrets, presidio, faker, etc.)
pip install heal[privacy]
```

# 5. Use heal - just run any command and then heal!
python broken_script.py
heal
```

# Or pipe errors directly
make build 2>&1 | heal

# With privacy protection (anonymize sensitive data)
production_script.py 2>&1 | heal -a
# or long form:
production_script.py 2>&1 | heal --anonymize
```

# Now you can run any command and heal will capture it:
your_failing_command
heal
```

## Features

- 🤖 **LLM-powered error analysis** - Uses GPT models to understand and fix shell errors
- 🔄 **Automatic command capture** - Shell hook captures last command and output
- 📥 **Multiple input methods** - Works with stdin, files, or shell hooks
- ⚙️ **Configurable models** - Support for various LLM providers via litellm
- 🔒 **Privacy protection** - 6 anonymization backends (regex, detect-secrets, presidio, priv-masker, datafog, faker)
- 🐳 **Docker-ready** - Full e2e test suite in Docker
- 🚀 **Zero-config start** - Just run `heal` after any error

## Privacy Protection

Mask sensitive data **before** it leaves your machine:

```bash
# Anonymize secrets, PII, tokens before sending to LLM
production_script.py 2>&1 | heal --anonymize
# or use the short flag:
production_script.py 2>&1 | heal -a

# Check which backends are active
heal fix --privacy-check

### Privacy Flags

| Flag | Description |
|------|-------------|
| `-a`, `--anonymize` | Force anonymization (overrides default) |
| `--no-anonymize` | Disable anonymization (overrides default) |
| `--privacy-check` | Show available privacy backends |

### Default Behavior

During first configuration (`heal config`), you'll be asked whether to enable anonymization by default. This setting can be overridden with flags:

```bash
# Disables anonymization regardless of default  
heal fix --no-anonymize
```

| Backend | What it masks | Install |
|---------|---------------|---------|
| **builtin_regex** | Emails, phones, IPs, API keys, JWT, PEM, DB passwords | included |
| **detect-secrets** | High-entropy strings, cloud keys | `pip install detect-secrets` |
| **presidio** | Names, addresses, dates (NLP, multilingual) | `pip install presidio-analyzer` |
| **priv-masker** | Polish NLP (PESEL, names, addresses) | `pip install priv-masker spacy` |
| **datafog** | Lightweight PII | `pip install datafog` |
| **faker** | Generate realistic fake replacements | `pip install faker` |

> Install all at once: `pip install heal[privacy]`

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| [Quick Start](QUICK_START.md) | Get running in 5 minutes |
| [Getting Started](examples/getting_started.md) | Full setup walkthrough |
| [Configuration Guide](examples/configuration_guide.md) | Provider & model setup |
| [Multi-Provider Usage](examples/multi_provider_usage.md) | Switch between LLM providers |
| [Privacy Protection](examples/privacy_protection.md) | Anonymization deep-dive |
| [Privacy Quick Start](examples/privacy_quick_start.md) | Privacy in 2 minutes |
| [Error Recovery](examples/error_recovery.md) | Interactive error fixing |
| [Troubleshooting](examples/troubleshooting.md) | Common issues & solutions |

### Examples

| Category | Guide |
|----------|-------|
| [Python Errors](examples/python_errors.md) | ModuleNotFoundError, ImportError, venv issues |
| [Docker Errors](examples/docker_errors.md) | Build failures, port conflicts, volumes |
| [Node.js Errors](examples/nodejs_errors.md) | npm, webpack, module resolution |
| [Git Errors](examples/git_errors.md) | Merge conflicts, auth, rebase |

### Comparisons

| Comparison | What's compared |
|------------|-----------------|
| [Privacy Libraries](comparisons/privacy_libraries.md) | detect-secrets vs presidio vs priv-masker vs datafog vs faker |
| [Shell Error Fixers](comparisons/shell_error_fixers.md) | heal vs thefuck vs shellcheck vs explainshell |
| [LLM CLI Tools](comparisons/llm_cli_tools.md) | heal vs aichat vs sgpt vs llm |

# Missing dependencies
python app.py 2>&1 | heal
# Import errors
python -m pytest 2>&1 | heal
# Virtual environment issues
python script.py 2>&1 | heal
# NPM install failures
npm install 2>&1 | heal
# Build errors
npm run build 2>&1 | heal
# Module not found
node app.js 2>&1 | heal
# Docker build failures
docker build . 2>&1 | heal
# Container runtime errors
docker-compose up 2>&1 | heal
# Permission issues
docker run myimage 2>&1 | heal
# Merge conflicts
git merge feature-branch 2>&1 | heal
# Push/pull errors
git push origin main 2>&1 | heal
# Rebase issues
git rebase main 2>&1 | heal
# Make errors
make build 2>&1 | heal
# Gradle/Maven builds
./gradlew build 2>&1 | heal
# PostgreSQL connection
psql -U user -d database 2>&1 | heal
# MySQL import errors
mysql < dump.sql 2>&1 | heal
# MongoDB connection
mongosh mongodb://localhost:27017 2>&1 | heal
# Permission denied
./script.sh 2>&1 | heal
# Port already in use
python -m http.server 8000 2>&1 | heal
# Disk space issues
cp large-file.zip /destination 2>&1 | heal
# APT/DNF errors
sudo apt install package 2>&1 | heal
# Homebrew issues
brew install tool 2>&1 | heal
# pip install failures
pip install package 2>&1 | heal
### `heal` (default)
Fix shell errors using LLM. Reads from stdin or captured output.

```bash
heal [--model MODEL] [--api-key KEY]
```

### `heal init`
Initialize bash integration for automatic command and output capture.

```bash
heal init
```

This will:
- Create `~/.heal/heal.bash` with command capture hooks
- Optionally add to your `~/.bashrc` automatically
- Enable helper commands: `heal-last`, `heal-output`

### `heal test`
Test your configuration with a simulated error.

```bash
heal test
```

This will:
- Verify your provider and API key are configured
- Send a test request to the LLM
- Show you a sample response

### `heal config`
Configure or reconfigure heal settings (provider, API key, model).

```bash
heal config
```

### `heal fix`
Explicit fix command (same as default `heal`).

```bash
heal fix [--model MODEL] [--api-key KEY]
```

### `heal install`
Legacy command (use `heal init` instead).

```bash
heal install
```

### `heal uninstall`
Remove shell hook and configuration.

```bash
heal uninstall
```

### `heal --help`
Show help message and available commands.

```bash
heal --help
```

### First-Time Setup

On first run, heal will guide you through an interactive setup:

```bash
$ heal

🔧 First-time setup - Let's configure your LLM provider

Available providers:
  1. OpenRouter (recommended)
  2. OpenAI
  3. Anthropic
  4. Google AI

💡 Tip: OpenRouter gives you access to all models with one API key

Select provider [1]: 1

🔑 Get your OpenRouter API key here:
   https://openrouter.ai/keys

Enter your API key: sk-or-...

🤖 Select a model from OpenRouter:

  1. openai/gpt-5.4-mini
     GPT-4o Mini (fast, cheap, recommended)
  2. openai/gpt-4o
     GPT-4o (most capable)
  3. anthropic/claude-3.5-sonnet
     Claude 3.5 Sonnet (excellent reasoning)
  4. google/gemini-pro-1.5
     Gemini Pro 1.5 (long context)
  5. meta-llama/llama-3.1-70b-instruct
     Llama 3.1 70B (open source)
  6. qwen/qwen-2.5-72b-instruct
     Qwen 2.5 72B (multilingual)
  7. Custom (enter model name manually)

Select model [1]: 1
```

### Reconfigure Settings

Change your provider, API key, or model anytime:

```bash
heal config
```

#### 🌐 OpenRouter (Recommended)
- **Why?** Access to all models with one API key
- **Get API key:** [openrouter.ai/keys](https://openrouter.ai/keys)
- **Models:** GPT-4, Claude, Gemini, Llama, Qwen, and 100+ more

#### 🤖 OpenAI
- **Get API key:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Models:** GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo

#### 🧠 Anthropic
- **Get API key:** [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **Models:** Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku

#### 🔍 Google AI
- **Get API key:** [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **Models:** Gemini Pro, Gemini Pro Vision

### Manual Configuration

Edit `~/.heal/.env`:

```bash
HEAL_PROVIDER=openrouter
HEAL_API_KEY=your-api-key-here
HEAL_MODEL=openai/gpt-5.4-mini
HEAL_BASE_URL=https://openrouter.ai/api/v1
```

Configuration is stored in `~/.heal/.env`.

### Unit tests

```bash
pip install -e ".[dev]"
python -m pytest -v
```

### Privacy tests (57 test cases)

```bash
python -m pytest tests/test_privacy.py -v
```

# All unit tests
docker compose run unit-tests

# Privacy tests only
docker compose run privacy-tests

# End-to-end CLI tests
docker compose run e2e-tests

# Full privacy suite with all backends
docker compose run privacy-full
```

# Install in development mode
pip install -e ".[dev]"

# Run with coverage
python -m pytest --cov=heal -v
```

## How it works

```
Command fails → heal captures output → anonymizes (optional) → LLM analyzes → suggests fix
```

1. **Command capture** — Gets last command from bash hook buffer or history
2. **Error collection** — Reads error output from stdin or captured file
3. **Privacy masking** — Optionally anonymizes sensitive data (6 backends)
4. **LLM analysis** — Sends sanitized command + error to LLM for analysis
5. **Solution proposal** — Returns concrete fix suggestions

## Limitations

- Shell processes cannot access previous process stderr without pipes
- Shell hook required for fully automatic operation
- Requires API key for LLM service (free-tier models available)

## License

Licensed under Apache-2.0.
## Author

Tom Sapletta
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **PyPI:** [pypi.org/project/heal](https://pypi.org/project/heal/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **TODO:** [TODO.md](TODO.md)
- **Comparisons:** [comparisons/](comparisons/README.md)

<!-- taskill:status:start -->

## Status

_Last updated by [taskill](https://github.com/oqlos/taskill) at 2026-04-25 13:38 UTC_

| Metric | Value |
|---|---|
| HEAD | `72de64a` |
| Coverage | — |
| Failing tests | — |
| Commits in last cycle | 26 |

> Work focused on CLI-related documentation and interface polish, plus a broad refactor of the configuration and test modules. Additional chores introduce a deep code analysis engine and example/configuration improvements.

<!-- taskill:status:end -->
