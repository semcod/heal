# Heal 🩺

[![PyPI version](https://img.shields.io/pypi/v/heal.svg)](https://pypi.org/project/heal/)
[![Python versions](https://img.shields.io/pypi/pyversions/heal.svg)](https://pypi.org/project/heal/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/tests-71%20passed-brightgreen.svg)](#testing)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](#docker-testing)
[![Privacy](https://img.shields.io/badge/privacy-6%20backends-purple.svg)](#privacy-protection)

**LLM-powered shell error fixing** — Your AI assistant for debugging and fixing command-line errors instantly, with built-in privacy protection.

## Installation

```bash
pip install heal

# With full privacy protection (detect-secrets, presidio, faker, etc.)
pip install heal[privacy]
```

## Quick Start

### Complete Setup (Recommended)

```bash
# 1. Configure heal (first time only)
heal config

# 2. Test your configuration
heal test

# 3. Initialize bash integration
heal init

# 4. Restart your shell
source ~/.bashrc

# 5. Use heal - just run any command and then heal!
python broken_script.py
heal
```

### Simplest Usage - Just `heal`

```bash
# Run any failing command, then simply run heal
npm install
heal

# Or pipe errors directly
make build 2>&1 | heal

# From error file
heal < error.log

# With privacy protection (anonymize sensitive data)
production_script.py 2>&1 | heal --anonymize
```

### Automatic Mode (with shell integration)

```bash
# Initialize bash integration (recommended)
heal init

# This will automatically add to ~/.bashrc
# Or manually add: source ~/.heal/heal.bash

# Restart your shell
source ~/.bashrc

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

# Check which backends are active
heal fix --privacy-check
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

## Usage Examples

### Python Development

```bash
# Missing dependencies
python app.py 2>&1 | heal
# → Suggests: pip install <missing-package>

# Import errors
python -m pytest 2>&1 | heal
# → Analyzes import paths and suggests fixes

# Virtual environment issues
python script.py 2>&1 | heal
# → Detects venv problems and suggests activation
```

### Node.js / JavaScript

```bash
# NPM install failures
npm install 2>&1 | heal
# → Suggests clearing cache, fixing package.json, or using --legacy-peer-deps

# Build errors
npm run build 2>&1 | heal
# → Analyzes webpack/vite errors and suggests configuration fixes

# Module not found
node app.js 2>&1 | heal
# → Suggests installing missing packages or fixing import paths
```

### Docker & Containers

```bash
# Docker build failures
docker build . 2>&1 | heal
# → Analyzes Dockerfile errors and suggests fixes

# Container runtime errors
docker-compose up 2>&1 | heal
# → Suggests port conflicts, volume issues, or network problems

# Permission issues
docker run myimage 2>&1 | heal
# → Suggests user/group fixes or volume mount corrections
```

### Git Operations

```bash
# Merge conflicts
git merge feature-branch 2>&1 | heal
# → Suggests conflict resolution strategies

# Push/pull errors
git push origin main 2>&1 | heal
# → Analyzes authentication, branch tracking, or force push needs

# Rebase issues
git rebase main 2>&1 | heal
# → Suggests conflict resolution or rebase abort/continue
```

### Build Systems

```bash
# Make errors
make build 2>&1 | heal
# → Analyzes missing dependencies or compilation errors

# CMake configuration
cmake . 2>&1 | heal
# → Suggests missing libraries or configuration flags

# Gradle/Maven builds
./gradlew build 2>&1 | heal
# → Analyzes Java compilation or dependency errors
```

### Database Operations

```bash
# PostgreSQL connection
psql -U user -d database 2>&1 | heal
# → Suggests authentication fixes or connection string corrections

# MySQL import errors
mysql < dump.sql 2>&1 | heal
# → Analyzes syntax errors or permission issues

# MongoDB connection
mongosh mongodb://localhost:27017 2>&1 | heal
# → Suggests service status checks or authentication fixes
```

### System Administration

```bash
# Permission denied
./script.sh 2>&1 | heal
# → Suggests chmod +x or sudo usage

# Port already in use
python -m http.server 8000 2>&1 | heal
# → Suggests finding and killing the process using the port

# Disk space issues
cp large-file.zip /destination 2>&1 | heal
# → Suggests cleaning up space or alternative locations
```

### Package Management

```bash
# APT/DNF errors
sudo apt install package 2>&1 | heal
# → Suggests repository updates or alternative package names

# Homebrew issues
brew install tool 2>&1 | heal
# → Suggests tap additions or formula fixes

# pip install failures
pip install package 2>&1 | heal
# → Suggests using --user, venv, or resolving dependency conflicts
```

## Commands

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

## Configuration

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

  1. openai/gpt-4o-mini
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

### Supported Providers

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
HEAL_MODEL=openai/gpt-4o-mini
HEAL_BASE_URL=https://openrouter.ai/api/v1
```

Configuration is stored in `~/.heal/.env`.

## Testing

### Unit tests

```bash
pip install -e ".[dev]"
python -m pytest -v
```

### Privacy tests (57 test cases)

```bash
python -m pytest tests/test_privacy.py -v
```

### Docker Testing

```bash
# All unit tests
docker compose run unit-tests

# Privacy tests only
docker compose run privacy-tests

# End-to-end CLI tests
docker compose run e2e-tests

# Full privacy suite with all backends
docker compose run privacy-full
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
python -m pytest -v

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

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

Created by **Tom Sapletta** - [tom@sapletta.com](mailto:tom@sapletta.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- **PyPI:** [pypi.org/project/heal](https://pypi.org/project/heal/)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **TODO:** [TODO.md](TODO.md)
- **Comparisons:** [comparisons/](comparisons/README.md)