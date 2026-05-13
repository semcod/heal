# Configuration Guide

This guide shows you how to configure heal with different providers.

## Quick Start - Recommended Setup (OpenRouter)

OpenRouter is recommended because it gives you access to **all models** with a single API key.

### Step 1: Run heal for the first time

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
```

### Step 2: Get your API key

```bash
🔑 Get your OpenRouter API key here:
   https://openrouter.ai/keys

Enter your API key: sk-or-v1-xxxxxxxxxxxxx
```

**How to get OpenRouter API key:**
1. Visit [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign in with Google, GitHub, or email
3. Click "Create Key"
4. Copy the key (starts with `sk-or-v1-`)
5. Paste it into heal

### Step 3: Choose your model

```bash
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

**Model recommendations:**
- **Option 1** (gpt-5.4-mini) - Best for most users, fast and cheap
- **Option 2** (gpt-4o) - Most capable, use for complex errors
- **Option 3** (claude-3.5-sonnet) - Excellent for code analysis
- **Option 7** (Custom) - Enter any model from [openrouter.ai/models](https://openrouter.ai/models)

### Done! 🎉

Your configuration is saved in `~/.heal/.env` and you're ready to use heal!

```bash
# Try it out
python broken_script.py 2>&1 | heal
```

---

### OpenAI Setup

If you prefer to use OpenAI directly:

```bash
$ heal config

⚙️  Heal Configuration

Available providers:
  1. OpenRouter (recommended)
  2. OpenAI
  3. Anthropic
  4. Google AI

Select provider [1]: 2

🔑 Get your OpenAI API key here:
   https://platform.openai.com/api-keys

Enter your API key: sk-xxxxxxxxxxxxx

🤖 Select a model from OpenAI:

  1. gpt-5.4-mini
     GPT-4o Mini (fast, cheap, recommended)
  2. gpt-4o
     GPT-4o (most capable)
  3. gpt-4-turbo
     GPT-4 Turbo (previous generation)
  4. gpt-3.5-turbo
     GPT-3.5 Turbo (legacy, cheap)
  5. Custom (enter model name manually)

Select model [1]: 1

✅ Configuration saved successfully!
```

**Get OpenAI API key:**
1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste it into heal

### Anthropic Setup

For Claude models:

```bash
$ heal config

Select provider [1]: 3

🔑 Get your Anthropic API key here:
   https://console.anthropic.com/settings/keys

Enter your API key: sk-ant-xxxxxxxxxxxxx

🤖 Select a model from Anthropic:

  1. claude-3-5-sonnet-20241022
     Claude 3.5 Sonnet (recommended)
  2. claude-3-opus-20240229
     Claude 3 Opus (most capable)
  3. claude-3-haiku-20240307
     Claude 3 Haiku (fast, cheap)
  4. Custom (enter model name manually)

Select model [1]: 1
```

**Get Anthropic API key:**
1. Visit [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Sign in to your account
3. Click "Create Key"
4. Copy the key (starts with `sk-ant-`)
5. Paste it into heal

### Google AI Setup

For Gemini models:

```bash
$ heal config

Select provider [1]: 4

🔑 Get your Google AI API key here:
   https://aistudio.google.com/app/apikey

Enter your API key: xxxxxxxxxxxxx

🤖 Select a model from Google AI:

  1. gemini-pro
     Gemini Pro (recommended)
  2. gemini-pro-vision
     Gemini Pro Vision (multimodal)
  3. Custom (enter model name manually)

Select model [1]: 1
```

**Get Google AI API key:**
1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the key
5. Paste it into heal

---

## Reconfiguring

Change your settings anytime with:

```bash
heal config
```

This will show your current configuration and ask if you want to change it:

```bash
⚙️  Heal Configuration

Current settings:
  Provider: OpenRouter
  Model: openai/gpt-5.4-mini

Do you want to reconfigure? [y/N]: y
```

---

## Manual Configuration

You can also edit `~/.heal/.env` directly:

### OpenRouter
```bash
HEAL_PROVIDER=openrouter
HEAL_API_KEY=sk-or-v1-xxxxxxxxxxxxx
HEAL_MODEL=openai/gpt-5.4-mini
HEAL_BASE_URL=https://openrouter.ai/api/v1
```

### OpenAI
```bash
HEAL_PROVIDER=openai
HEAL_API_KEY=sk-xxxxxxxxxxxxx
HEAL_MODEL=gpt-5.4-mini
```

### Anthropic
```bash
HEAL_PROVIDER=anthropic
HEAL_API_KEY=sk-ant-xxxxxxxxxxxxx
HEAL_MODEL=claude-3-5-sonnet-20241022
```

### Google AI
```bash
HEAL_PROVIDER=google
HEAL_API_KEY=xxxxxxxxxxxxx
HEAL_MODEL=gemini-pro
```

---

### "Error calling LLM: ..."

**Check your API key:**
```bash
cat ~/.heal/.env
```

Make sure:
- API key is correct and not expired
- You have credits/billing enabled for your provider
- The model name is correct

**Reconfigure:**
```bash
heal config
```

### "No module named 'litellm'"

Install dependencies:
```bash
pip install heal
# or
pip install -e ".[dev]"
```

### Change model without reconfiguring everything

Edit `~/.heal/.env` and change just the `HEAL_MODEL` line:

```bash
# Before
HEAL_MODEL=openai/gpt-5.4-mini

# After
HEAL_MODEL=anthropic/claude-3.5-sonnet
```

---

### Cheapest Options

1. **OpenRouter + gpt-5.4-mini** - ~$0.15 per 1M tokens
2. **OpenRouter + claude-3-haiku** - ~$0.25 per 1M tokens
3. **OpenRouter + llama-3.1-70b** - ~$0.50 per 1M tokens (open source)

### Most Capable

1. **OpenRouter + gpt-4o** - Best overall
2. **OpenRouter + claude-3-opus** - Best for code
3. **Anthropic + claude-3-5-sonnet** - Best reasoning

### Best Value

**OpenRouter + gpt-5.4-mini** (recommended) - Excellent quality at low cost

---

## FAQ

**Q: Why OpenRouter as default?**
A: One API key gives you access to 100+ models from all providers. You can switch models without getting new API keys.

**Q: Can I use local models?**
A: Not yet, but it's on the roadmap. See [TODO.md](../TODO.md).

**Q: How do I see available models?**
A: Visit [openrouter.ai/models](https://openrouter.ai/models) for the full list.

**Q: Is my API key secure?**
A: It's stored in `~/.heal/.env` with file permissions 600 (only you can read it). Never commit this file to git.

**Q: Can I use different models for different projects?**
A: Currently no, but you can quickly switch with `heal config`.
