# TODO

## High Priority

- [ ] Add support for reading from clipboard (for GUI terminal users)
- [ ] Implement `heal history` command to show past fixes and solutions
- [ ] Create shell completion scripts (bash, zsh, fish)
- [ ] Add support for custom prompts/templates

## Features

- [ ] Add `heal explain` command for explaining errors without fixing
- [ ] Implement `heal suggest` for proactive suggestions based on command
- [ ] Create `heal learn` to save successful fixes for future reference
- [ ] Add `heal stats` to show usage statistics
- [ ] Implement rate limiting and caching for API calls
- [ ] Add support for local LLM models (ollama, llama.cpp)

## Privacy & Security

- [ ] Add `--anonymize` as default behavior (opt-out instead of opt-in)
- [ ] Custom regex patterns from user config
- [ ] Implement secure API key storage (keyring integration)
- [ ] Implement audit logging
- [ ] Create security policy document

## Improvements

- [ ] Better error message formatting and syntax highlighting
- [ ] Add progress indicators for LLM API calls
- [ ] Implement retry logic with exponential backoff
- [ ] Add support for streaming responses
- [ ] Improve shell hook to work with zsh, fish, and other shells
- [ ] Add context awareness (git repo, project type detection)
- [ ] Implement smart error categorization

## Documentation

- [ ] Create video tutorial/demo
- [ ] Create FAQ section
- [ ] Add contributing guidelines
- [ ] Create architecture documentation

## Testing

- [ ] Add integration tests for different error scenarios
- [ ] Create mock LLM responses for testing
- [ ] Add performance benchmarks
- [ ] Test with different shell environments
- [ ] Add CI/CD pipeline improvements

## DevOps

- [ ] Set up automated releases
- [ ] Add code coverage reporting
- [ ] Implement semantic versioning automation
- [ ] Add pre-commit hooks

## Community

- [ ] Create Discord/Slack community
- [ ] Add issue templates
- [ ] Create pull request template
- [ ] Add code of conduct
- [ ] Create roadmap document

## Performance

- [ ] Optimize prompt size to reduce token usage
- [ ] Implement response caching
- [ ] Add offline mode with cached solutions
- [ ] Reduce startup time
- [ ] Optimize shell hook performance

## Integrations

- [ ] VS Code extension
- [ ] JetBrains IDE plugin
- [ ] GitHub Actions integration
- [ ] GitLab CI integration
- [ ] Slack/Discord bot for team usage
- [ ] Web dashboard for team analytics

## Nice to Have

- [ ] Add ASCII art logo
- [ ] Implement fun easter eggs
- [ ] Add motivational messages
- [ ] Create heal mascot/branding
- [ ] Add sound effects (optional, configurable)

## Discovered

- Track remaining CLI interface work and surface actionable items (multiple docs/feat commits reference CLI improvements)
- Continue/refine config module refactor and finalize core configuration behaviors (refactor(config) commits)
- Add/update examples for the configuration management system (refactor(examples))
- Integrate and document the deep code analysis engine added under config (chore(config))
- Update tests to reflect refactored test modules and new CLI behaviors (refactor(tests))


## Done (moved to CHANGELOG)

- [x] Add `heal config` command to manage configuration interactively
- [x] Add support for multiple LLM providers configuration
- [x] Built-in regex masking (emails, phones, IPs, API keys, JWT, PEM, DB passwords)
- [x] detect-secrets integration (high-entropy strings, cloud keys)
- [x] presidio-analyzer integration (NLP-based PII)
- [x] priv-masker integration (Polish NLP)
- [x] datafog integration (lightweight PII)
- [x] faker integration (fake data replacement)
- [x] Add troubleshooting guide
- [x] Add security best practices guide
- [x] Comparisons with competitors (thefuck, shellcheck, aichat, sgpt)
- [x] Privacy libraries comparison (detect-secrets, presidio, etc.)
- [x] Privacy module tests (57 test cases)
- [x] Docker environment for e2e tests
- [x] E2e bash test script
- [x] Create Docker image for testing
- [x] Create docker-compose.yml for test suites
