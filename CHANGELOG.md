## [0.1.24] - 2026-02-21

### Summary

feat(docs): CLI interface improvements

### Docs

- docs: update QUICK_START.md
- docs: update README
- docs: update privacy_quick_start.md

### Other

- update heal/cli.py


## [0.1.23] - 2026-02-21

### Summary

refactor(tests): test module improvements

### Test

- scripts: update e2e_test.sh
- update tests/test_main.py
- update tests/test_privacy.py


## [0.1.22] - 2026-02-21

### Summary

docs(docs): CLI interface improvements

### Docs

- docs: update README
- docs: update llm_cli_tools.md
- docs: update privacy_libraries.md


## [0.1.21] - 2026-02-21

### Summary

fix(docs): CLI interface improvements

### Docs

- docs: update README
- docs: update TODO.md
- docs: update README
- docs: update llm_cli_tools.md
- docs: update privacy_libraries.md
- docs: update shell_error_fixers.md

### Test

- scripts: update e2e_test.sh
- update tests/test_main.py
- update tests/test_privacy.py

### Build

- update pyproject.toml

### Other

- update Dockerfile.e2e
- update heal/cli.py
- update heal/privacy.py


## [0.1.20] - 2026-02-21

### Summary

refactor(examples): configuration management system

### Docs

- docs: update getting_started.md
- docs: update privacy_protection.md
- docs: update privacy_quick_start.md
- docs: update troubleshooting.md

### Build

- update pyproject.toml

### Other

- update heal/privacy.py


## [0.1.19] - 2026-02-21

### Summary

feat(docs): CLI interface improvements

### Docs

- docs: update QUICK_START.md
- docs: update README
- docs: update configuration_guide.md
- docs: update privacy_protection.md
- docs: update privacy_quick_start.md

### Test

- update tests/test_main.py

### Build

- update pyproject.toml

### Other

- update heal/cli.py
- update heal/privacy.py


## [0.1.18] - 2026-02-21

### Summary

fix(docs): CLI interface improvements

### Docs

- docs: update error_recovery.md

### Test

- update tests/test_main.py

### Other

- update heal/cli.py


## [Unreleased]

### Added

- **Multi-backend privacy module** — 6 anonymization backends:
  - `builtin_regex` — emails, phones, IPs, API keys, JWT, PEM, SSH keys, DB passwords, SSN (always available)
  - `detect-secrets` — high-entropy strings, cloud keys (Yelp)
  - `presidio-analyzer` — NLP-based PII detection, multilingual (Microsoft)
  - `priv-masker` — Polish NLP anonymization (PESEL, names, addresses)
  - `datafog` — lightweight PII detection
  - `faker` — realistic fake data replacement
- **`--anonymize` flag** on `heal fix` to mask sensitive data before sending to LLM
- **`--privacy-check` flag** to show all backend availability
- **57 privacy test cases** — emails, phones, IDs, secrets, IPs, PEM keys, JWT, DB connections, edge cases
- **Docker environment** for e2e testing (`Dockerfile`, `Dockerfile.e2e`, `docker-compose.yml`)
- **E2e bash test script** (`tests/e2e_test.sh`) — CLI, privacy, piping tests
- **Comparisons directory** — heal vs thefuck, shellcheck, aichat, sgpt, privacy libs
- **Interactive reconfiguration menu** — `heal test` offers specific options on errors
- **Step-by-step problem diagnosis** on configuration errors

### Changed

- **Privacy module rewritten** from single-backend to multi-backend architecture
- **Improved error recovery flow** — more granular options for fixing configuration issues
- **README** — added badges, documentation menu, privacy table, Docker section, comparisons links
- **TODO.md** — updated with completed items, added Privacy & Security section

### Documentation

- Added privacy libraries comparison (detect-secrets, presidio, priv-masker, datafog, faker)
- Added shell error fixers comparison (heal vs thefuck, shellcheck, explainshell)
- Added LLM CLI tools comparison (heal vs aichat, sgpt, llm)
- Added GDPR/RODO compliance information
- Added security considerations for sensitive data

## [0.1.17] - 2026-02-21

### Summary

feat(docs): CLI interface improvements

### Docs

- docs: update troubleshooting.md

### Test

- update tests/test_main.py

### Other

- update heal/cli.py


## [0.1.16] - 2026-02-21

### Summary

feat(docs): CLI interface improvements

### Docs

- docs: update multi_provider_usage.md

### Test

- update tests/test_main.py

### Other

- update heal/cli.py


## [0.1.15] - 2026-02-21

### Summary

refactor(docs): CLI interface improvements

### Docs

- docs: update QUICK_START.md
- docs: update README
- docs: update TODO.md
- docs: update README
- docs: update configuration_guide.md
- docs: update docker_errors.md
- docs: update getting_started.md
- docs: update git_errors.md
- docs: update nodejs_errors.md
- docs: update python_errors.md

### Test

- update tests/test_cli.py
- update tests/test_main.py

### Other

- update heal/cli.py


## [Unreleased]

### Added

- **Automatic provider prefix handling** for litellm compatibility
- **Multi-provider model support** - easily switch between OpenRouter, OpenAI, Anthropic, Google models
- **`heal test` command** to verify configuration with simulated error
- **`heal init` command** for automatic bash integration setup
- **Automatic command and output capture** via bash buffer system
- **Helper commands**: `heal-last` (show last command), `heal-output` (show last output)
- **Auto-install to ~/.bashrc** with confirmation prompt
- **Exit code tracking** for better error context
- Trinity Large model added to OpenRouter options (free tier)
- **Interactive provider selection** with OpenRouter as default (recommended)
- **Numbered model selection menus** for easy configuration
- **Direct API key links** for each provider (OpenRouter, OpenAI, Anthropic, Google AI)
- **`heal config` command** to reconfigure settings anytime
- Support for multiple LLM providers: OpenRouter, OpenAI, Anthropic, Google AI
- Default `heal` command now runs fix automatically (no need to type `heal fix`)
- Comprehensive usage examples for different IT scenarios in README
- Examples for Python, Node.js, Docker, Git, Build Systems, Databases, System Admin, and Package Management
- Manual configuration documentation
- TODO.md with 60+ planned improvements
- Examples directory with real-world error scenarios
- Configuration guide with step-by-step setup for all providers

### Changed

- **Configuration UX completely redesigned** with interactive numbered menus
- CLI behavior: `heal` without arguments now invokes fix command
- `heal --help`, `heal -h`, or `heal help` shows help message
- Enhanced README with emojis and better structure
- Improved feature descriptions and quick start guide
- Provider-specific API key handling for better compatibility

### Fixed

- **OpenRouter authentication** - fixed API key passing to litellm (now passes both env var and explicit api_key parameter)
- **Interactive error recovery** - `heal test` now offers to reconfigure on authentication errors
- **OpenRouter model compatibility** - automatically adds `openrouter/` prefix for litellm
- **Google Gemini support** - automatically adds `gemini/` prefix when needed
- Model format handling across different providers
- Better error messages with specific troubleshooting for auth, rate limit, and quota errors

### Documentation

- Added interactive configuration flow examples
- Added 4 provider sections with API key links
- Added 8 categories of real-world usage examples
- Added manual configuration section
- Added supported models documentation
- Improved quick start instructions
- Created comprehensive examples directory
- Added getting started guide with step-by-step setup

## [0.1.14] - 2026-02-21

### Summary

refactor(config): core module improvements

### Build

- update pyproject.toml

### Other

- update heal/__init__.py


## [0.1.13] - 2026-02-21

### Summary

refactor(config): config module improvements

### Test

- update tests/test_main.py

### Build

- update pyproject.toml


## [0.1.12] - 2026-02-21

### Summary

refactor(tests): test module improvements

### Test

- update tests/test_main.py


## [0.1.11] - 2026-02-21

### Summary

refactor(config): config module improvements

### Test

- update tests/test_main.py

### Build

- update pyproject.toml


## [0.1.10] - 2026-02-21

### Summary

refactor(config): config module improvements

### Test

- update tests/test_main.py

### Build

- update pyproject.toml


## [0.1.9] - 2026-02-21

### Summary

chore(config): deep code analysis engine

### Build

- update pyproject.toml


## [0.1.8] - 2026-02-21

### Summary

chore(config): deep code analysis engine

### Build

- update pyproject.toml


## [0.1.7] - 2026-02-21

### Summary

chore(config): config module improvements

### Build

- update pyproject.toml


## [0.1.6] - 2026-02-21

### Summary

chore(config): config module improvements

### Build

- update pyproject.toml


## [0.1.5] - 2026-02-21

### Summary

chore(config): config module improvements

### Build

- update pyproject.toml


## [0.1.4] - 2026-02-21

### Summary

refactor(config): config module improvements

### Test

- update tests/test_main.py

### Build

- update pyproject.toml


## [0.1.3] - 2026-02-21

### Summary

feat(tests): CLI interface improvements

### Test

- update tests/test_cli.py
- update tests/test_main.py

### Build

- update pyproject.toml


## [0.1.2] - 2026-02-21

### Summary

refactor(tests): CLI interface improvements

### Test

- update tests/__init__.py
- update tests/test_cli.py
- update tests/test_main.py

### Build

- update pyproject.toml

### Ci

- config: update publish.yml

### Config

- config: update goal.yaml

### Other

- build: update Makefile
- update pytest.ini


## [0.1.1] - 2026-02-21

### Summary

refactor(goal): CLI interface improvements

### Docs

- docs: update README

### Test

- update tests/test_heal.py

### Build

- update pyproject.toml
- update setup.py

### Config

- config: update goal.yaml

### Other

- update heal/__init__.py
- update heal/cli.py
- update heal/main.py
- scripts: update project.sh


