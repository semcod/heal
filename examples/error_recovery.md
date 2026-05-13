# Error Recovery Guide

How heal helps you fix configuration problems interactively.

## Interactive Error Recovery

When `heal test` encounters an error, it doesn't just show you an error message - it guides you through fixing it step by step.

### Scenario: Invalid API Key

```bash
$ heal test

🧪 Testing heal configuration...

✓ Provider: OpenRouter
✓ Model: arcee-ai/trinity-large-preview:free
✓ API Key: ********************tput

📝 Simulating error:
   Command: python app.py
   Error: ModuleNotFoundError: No module named 'flask'

🤖 Asking LLM for solution...

❌ Test failed!

💡 Error Details:
────────────────────────────────────────────────────────────
Authentication failed - your API key appears to be invalid.

Possible causes:
  • API key is incorrect or expired
  • API key doesn't have proper permissions
  • Wrong provider selected for this API key

Let's reconfigure your settings step by step:

What would you like to do?
  1. Change provider and API key
  2. Just update API key (keep current provider)
  3. Try a different model (keep provider and key)
  4. Cancel

Select option [1]:
```

### Option 1: Change Provider and API Key

**When to use:** You want to switch to a different LLM provider entirely.

```bash
Select option [1]: 1

🔧 Full reconfiguration

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

Enter your API key: sk-or-v1-xxxxxxxxxxxxx

🤖 Select a model from OpenRouter:

  1. openai/gpt-5.4-mini
     GPT-4o Mini (fast, cheap, recommended)
  2. openai/gpt-4o
     GPT-4o (most capable)
  3. anthropic/claude-3.5-sonnet
     Claude 3.5 Sonnet (excellent reasoning)
  ...

Select model [1]: 1

✅ Reconfigured! Try running 'heal test' again.
```

### Option 2: Just Update API Key

**When to use:** You want to keep the same provider but use a different API key (e.g., new key, different account).

```bash
Select option [1]: 2

🔑 Update API key

Provider: OpenRouter
Get your API key: https://openrouter.ai/keys

Enter your new API key: sk-or-v1-yyyyyyyyyyyyyy

✅ API key updated! Try running 'heal test' again.
```

### Option 3: Try a Different Model

**When to use:** Your API key works but the current model might not be available or working.

```bash
Select option [1]: 3

🤖 Select a different model

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
  7. arcee-ai/trinity-large-preview:free
     Trinity Large (free, fast)
  8. Custom (enter model name manually)

Select model [1]: 7

✅ Model changed to: arcee-ai/trinity-large-preview:free
Try running 'heal test' again.
```

### Option 4: Cancel

**When to use:** You want to fix the issue manually.

```bash
Select option [1]: 4

Run 'heal config' when ready to fix your configuration.
```

## Generic Errors

For other types of errors, heal offers different options:

```bash
❌ Test failed!

💡 Error Details:
────────────────────────────────────────────────────────────
Error calling LLM: <some error>

Troubleshooting:
  1. Verify your API key is valid
  2. Check you have credits/billing enabled
  3. Ensure the model name is correct
  4. Try a different model

Would you like to reconfigure? [y/N]: y

What would you like to do?
  1. Full reconfiguration (provider, API key, model)
  2. Just change the model
  3. Cancel

Select option [2]:
```

### Option 1: Full Reconfiguration

Starts from scratch - removes all configuration and asks for everything again.

### Option 2: Just Change the Model

Quick way to try a different model without changing provider or API key:

```bash
Select option [2]: 2

🤖 Select a different model from OpenRouter:

  1. openai/gpt-5.4-mini
     GPT-4o Mini (fast, cheap, recommended)
  2. openai/gpt-4o
     GPT-4o (most capable)
  ...

Select model [1]: 1

✅ Model changed to: openai/gpt-5.4-mini
Try running 'heal test' again.
```

## Rate Limit Errors

For rate limit errors, heal provides specific guidance:

```bash
❌ Test failed!

💡 Error Details:
────────────────────────────────────────────────────────────
Rate limit exceeded - you're making too many requests.

Solutions:
  • Wait a few minutes and try again
  • Check your provider's rate limits
  • Consider upgrading your plan
────────────────────────────────────────────────────────────
```

No reconfiguration needed - just wait and retry.

## Quota/Credits Errors

For quota or credit issues:

```bash
❌ Test failed!

💡 Error Details:
────────────────────────────────────────────────────────────
Insufficient credits or quota exceeded.

Solutions:
  • Add credits to your account
  • Enable billing if not already enabled
  • Check your usage limits
────────────────────────────────────────────────────────────
```

## Decision Tree

Use this to decide which option to choose:

```
Authentication Error?
├─ Wrong provider? → Option 1: Change provider and API key
├─ Need new API key? → Option 2: Just update API key
├─ Model not working? → Option 3: Try a different model
└─ Not sure? → Option 1: Change provider and API key

Generic Error?
├─ Want to start fresh? → Option 1: Full reconfiguration
├─ Just try different model? → Option 2: Just change the model
└─ Want to fix manually? → Option 3: Cancel

Rate Limit?
└─ Wait 60 seconds and retry

Quota/Credits?
└─ Add credits to your account
```

### 1. Start with the Least Disruptive Option

- Try changing the model first (Option 3 or 2)
- Then try updating just the API key (Option 2)
- Full reconfiguration as last resort (Option 1)

### 2. Keep Your API Keys Handy

Have your API keys ready before running `heal test`:
- OpenRouter: [openrouter.ai/keys](https://openrouter.ai/keys)
- OpenAI: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Anthropic: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- Google: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 3. Test After Each Change

Always run `heal test` after reconfiguring to verify it works.

### 4. Use Free Models for Testing

When trying different models, start with free options:
- `arcee-ai/trinity-large-preview:free` (OpenRouter)
- `gpt-5.4-mini` (cheap on OpenAI/OpenRouter)

### 5. Document Your Working Configuration

Once you find a working setup, save it:

```bash
cat ~/.heal/.env
# Select: arcee-ai/trinity-large-preview:free (free model)
heal test  # Verify it works
```

# Enter new API key
heal test  # Verify it works
```

# Select a different model from the list
heal test  # Verify it works
```

# Select model
heal test  # Verify it works
```

# No reconfiguration needed
heal test  # Should work after adding credits
```

## Manual Configuration

If you prefer to configure manually:

```bash
## Getting Help

If interactive recovery doesn't work:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Try manual configuration: `heal config`
3. Delete config and start fresh: `rm ~/.heal/.env && heal config`
4. Report an issue with the output of `heal test`

## Summary

Heal's interactive error recovery:
- ✅ Asks specific questions about what to fix
- ✅ Offers multiple options based on the error
- ✅ Guides you step-by-step through reconfiguration
- ✅ Provides direct links to get API keys
- ✅ Shows you exactly what changed
- ✅ Tells you what to do next

No more guessing what went wrong - heal helps you fix it!
