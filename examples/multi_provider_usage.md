# Multi-Provider Usage Guide

Heal supports multiple LLM providers and makes it easy to switch between them. This guide shows you how to use different providers and models.

## How Provider Prefixes Work

Heal automatically handles provider-specific model formatting for litellm compatibility:

### OpenRouter
- **Stored as:** `openai/gpt-5.4-mini` or `arcee-ai/trinity-large-preview:free`
- **Sent to litellm as:** `openrouter/openai/gpt-5.4-mini` or `openrouter/arcee-ai/trinity-large-preview:free`
- **Why:** OpenRouter requires the `openrouter/` prefix to route requests correctly

### OpenAI
- **Stored as:** `gpt-5.4-mini`
- **Sent to litellm as:** `gpt-5.4-mini` (no prefix)
- **Why:** OpenAI is the default provider in litellm

### Anthropic
- **Stored as:** `claude-3-5-sonnet-20241022`
- **Sent to litellm as:** `claude-3-5-sonnet-20241022` (no prefix)
- **Why:** Anthropic models are recognized by name

### Google AI
- **Stored as:** `gemini-pro`
- **Sent to litellm as:** `gemini/gemini-pro`
- **Why:** Google models need the `gemini/` prefix

### Method 1: Using `heal config`

The easiest way to switch providers:

```bash
heal config
```

This will show your current configuration and ask if you want to reconfigure:

```
⚙️  Heal Configuration

Current settings:
  Provider: OpenRouter
  Model: openai/gpt-5.4-mini

Do you want to reconfigure? [y/N]: y
```

Then select a new provider and model.

### Method 2: Manual Configuration

Edit `~/.heal/.env` directly:

```bash
# Switch to OpenAI
HEAL_PROVIDER=openai
HEAL_API_KEY=sk-xxxxxxxxxxxxx
HEAL_MODEL=gpt-4o

# Switch to Anthropic
HEAL_PROVIDER=anthropic
HEAL_API_KEY=sk-ant-xxxxxxxxxxxxx
HEAL_MODEL=claude-3-5-sonnet-20241022

# Switch to Google
HEAL_PROVIDER=google
HEAL_API_KEY=xxxxxxxxxxxxx
HEAL_MODEL=gemini-pro

# Switch to OpenRouter
HEAL_PROVIDER=openrouter
HEAL_API_KEY=sk-or-v1-xxxxxxxxxxxxx
HEAL_MODEL=anthropic/claude-3.5-sonnet
HEAL_BASE_URL=https://openrouter.ai/api/v1
```

### Scenario: Different Models for Different Tasks

You can quickly switch models for different use cases:

## Testing Different Providers

After switching, always test:

```bash
heal test
```

Example output with OpenRouter:

```
🧪 Testing heal configuration...

✓ Provider: OpenRouter
✓ Model: arcee-ai/trinity-large-preview:free
  (litellm format: openrouter/arcee-ai/trinity-large-preview:free)
✓ API Key: ********************tput

📝 Simulating error:
   Command: python app.py
   Error: ModuleNotFoundError: No module named 'flask'

🤖 Asking LLM for solution...

💡 LLM Response:
────────────────────────────────────────────────────────────
Install Flask: pip install flask
────────────────────────────────────────────────────────────

✅ Test successful! Heal is working correctly.
```

### OpenRouter (Recommended)
**Pros:**
- One API key for all models
- Access to 100+ models from all providers
- Easy to switch between models
- Often cheaper than direct provider access
- Free tier models available

**Cons:**
- Slight latency overhead
- Requires internet connection

**Best for:** Most users, especially those who want flexibility

### OpenAI
**Pros:**
- Direct access to GPT models
- Lowest latency for OpenAI models
- Official support

**Cons:**
- Only OpenAI models
- Can be expensive
- Requires separate API key

**Best for:** Users committed to OpenAI models only

### Anthropic
**Pros:**
- Direct access to Claude models
- Excellent for code analysis
- Strong reasoning capabilities

**Cons:**
- Only Claude models
- Requires separate API key
- Can be expensive

**Best for:** Users who prefer Claude's reasoning style

### Google AI
**Pros:**
- Free tier available
- Very long context windows
- Multimodal capabilities

**Cons:**
- Only Gemini models
- Requires separate API key
- Less mature than OpenAI/Anthropic

**Best for:** Users who need long context or free tier

### OpenRouter Custom Models

You can use any model from [openrouter.ai/models](https://openrouter.ai/models):

```bash
heal config
# Enter: meta-llama/llama-3.3-70b-instruct
```

Heal will automatically add the `openrouter/` prefix.

### Provider-Specific Models

For other providers, check their documentation:
- OpenAI: [platform.openai.com/docs/models](https://platform.openai.com/docs/models)
- Anthropic: [docs.anthropic.com/claude/docs/models-overview](https://docs.anthropic.com/claude/docs/models-overview)
- Google: [ai.google.dev/models/gemini](https://ai.google.dev/models/gemini)

### "LLM Provider NOT provided" Error

This means the model name format is incorrect for litellm. Heal should handle this automatically, but if you see this:

1. Run `heal config` to reconfigure
2. Or check your `~/.heal/.env` file
3. Make sure `HEAL_PROVIDER` matches your model

### Model Not Found

If you get a "model not found" error:

1. Verify the model name is correct
2. Check you have access to that model
3. For OpenRouter, visit [openrouter.ai/models](https://openrouter.ai/models) to see available models
4. Run `heal test` to verify

### API Key Issues

If you're switching providers, make sure to update your API key:

```bash
heal config
# OpenRouter with free models
HEAL_PROVIDER=openrouter
HEAL_MODEL=arcee-ai/trinity-large-preview:free
```

# OpenRouter with GPT-4o-mini
HEAL_PROVIDER=openrouter
HEAL_MODEL=openai/gpt-5.4-mini
```

# OpenRouter with Claude 3.5 Sonnet
HEAL_PROVIDER=openrouter
HEAL_MODEL=anthropic/claude-3.5-sonnet
```

# Use heal
your_command
heal
```

## Provider URLs

- **OpenRouter:** [openrouter.ai](https://openrouter.ai)
- **OpenAI:** [platform.openai.com](https://platform.openai.com)
- **Anthropic:** [console.anthropic.com](https://console.anthropic.com)
- **Google AI:** [aistudio.google.com](https://aistudio.google.com)

## Supported by litellm

Heal uses [litellm](https://github.com/BerriAI/litellm) which supports 100+ LLM providers. See the full list at [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers).
