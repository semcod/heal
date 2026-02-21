# LLM CLI Tools Comparison

## heal vs Other LLM-Powered CLI Tools

| Feature | heal | aichat | sgpt | llm (simonw) |
|---------|:---:|:---:|:---:|:---:|
| **Shell error fixing** | ✅ | partial | partial | — |
| **Auto error capture** | ✅ | — | — | — |
| **Bash hook** | ✅ | — | — | — |
| **Privacy/anonymize** | ✅ | — | — | — |
| **Multi-provider** | ✅ | ✅ | ✅ | ✅ |
| **Interactive config** | ✅ | ✅ | — | ✅ |
| **Chat mode** | — | ✅ | ✅ | ✅ |
| **General-purpose** | — | ✅ | ✅ | ✅ |
| **Code generation** | — | ✅ | ✅ | ✅ |
| **Shell execution** | — | — | ✅ | — |
| **Plugin system** | — | — | — | ✅ |
| **Streaming** | — | ✅ | ✅ | ✅ |
| **Python** | ✅ | — | ✅ | ✅ |
| **Rust** | — | ✅ | — | — |

## heal

**Focus:** Shell error diagnosis and fixing with privacy protection.

**Unique features:**
- Automatic command + output capture via bash hook
- Built-in privacy masking (6 backends) before LLM
- "Just run `heal` after any error" workflow
- Interactive reconfiguration on failures

**Best for:** Fixing errors in development/production pipelines with privacy.

## aichat

**GitHub:** [github.com/sigoden/aichat](https://github.com/sigoden/aichat)  
**Install:** `cargo install aichat`

**Focus:** General-purpose AI chat in the terminal. Rust-based.

**Unique features:**
- Extremely fast (Rust)
- Multi-model conversations
- File/image input
- Shell integration with roles
- RAG support

**Best for:** General AI chat and code generation from terminal.

## sgpt (shell-gpt)

**GitHub:** [github.com/TheR1D/shell_gpt](https://github.com/TheR1D/shell_gpt)  
**Install:** `pip install shell-gpt`

**Focus:** GPT-powered shell assistant — generate and execute commands.

**Unique features:**
- Can generate AND execute shell commands
- Code generation with syntax highlighting
- Chat persistence
- Custom roles/personas

**Best for:** Generating shell commands from natural language descriptions.

## llm (Simon Willison)

**GitHub:** [github.com/simonw/llm](https://github.com/simonw/llm)  
**Install:** `pip install llm`

**Focus:** Access LLMs from the command line. Plugin-based architecture.

**Unique features:**
- Plugin ecosystem (50+ plugins)
- Local model support (llama.cpp, etc.)
- Conversation logging to SQLite
- Template system
- Embeddings support

**Best for:** Power users who want extensible LLM access with plugins.

## Key Differences

### heal's unique value proposition:

1. **Error-focused workflow** — not a general chat tool, but a dedicated error fixer
2. **Zero-friction** — `heal` after any error, nothing more
3. **Privacy-first** — only tool with built-in data anonymization
4. **Bash integration** — automatic command capture, no manual piping needed
5. **Interactive recovery** — guides you step-by-step when config fails

### When heal + another tool makes sense:

```bash
# Use sgpt to generate a command
sgpt "create a docker compose file for postgres + redis"

# Use heal when the generated command fails
docker compose up 2>&1 | heal

# Use llm for general questions
llm "explain kubernetes pod lifecycle"

# Use heal for fixing k8s errors
kubectl apply -f deployment.yaml 2>&1 | heal --anonymize
```

## Installation Comparison

| Tool | Install | Size | Language |
|------|---------|------|----------|
| heal | `pip install fixi` | ~5 MB | Python |
| aichat | `cargo install aichat` | ~10 MB | Rust |
| sgpt | `pip install shell-gpt` | ~5 MB | Python |
| llm | `pip install llm` | ~5 MB | Python |

## Provider Support

| Provider | heal | aichat | sgpt | llm |
|----------|:---:|:---:|:---:|:---:|
| OpenRouter | ✅ | ✅ | — | via plugin |
| OpenAI | ✅ | ✅ | ✅ | ✅ |
| Anthropic | ✅ | ✅ | — | via plugin |
| Google AI | ✅ | ✅ | — | via plugin |
| Local (Ollama) | via litellm | ✅ | — | via plugin |
| Azure | via litellm | ✅ | ✅ | via plugin |
