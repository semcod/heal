# Troubleshooting Guide

Common issues and how to fix them.

### Error: "Missing Authentication header" or "401"

**What it means:** Your API key is not being accepted by the provider.

**Solutions:**

1. **Run heal test to diagnose:**
   ```bash
   heal test
   ```
   
   If you see an authentication error, heal will automatically offer to reconfigure:
   ```
   ❌ Test failed!
   
   💡 Error Details:
   ────────────────────────────────────────────────────────────
   Authentication failed - your API key appears to be invalid.
   
   Possible causes:
     • API key is incorrect or expired
     • API key doesn't have proper permissions
     • Wrong provider selected for this API key
   
   Would you like to reconfigure your API key? [Y/n]:
   ```

2. **Manually reconfigure:**
   ```bash
   heal config
   ```

3. **Check your API key:**
   - OpenRouter: Visit [openrouter.ai/keys](https://openrouter.ai/keys)
   - OpenAI: Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Anthropic: Visit [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
   - Google: Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

4. **Verify the key format:**
   - OpenRouter: `sk-or-v1-...`
   - OpenAI: `sk-...`
   - Anthropic: `sk-ant-...`
   - Google: varies

5. **Check provider/key match:**
   ```bash
   cat ~/.heal/.env
   ```
   
   Make sure `HEAL_PROVIDER` matches your API key source.

### Error: "rate_limit_exceeded"

**What it means:** You're making too many requests.

**Solutions:**

1. **Wait and retry:**
   ```bash
   # Wait 1 minute
   sleep 60
   heal test
   ```

2. **Check your rate limits:**
   - OpenRouter: [openrouter.ai/docs/limits](https://openrouter.ai/docs/limits)
   - OpenAI: [platform.openai.com/docs/guides/rate-limits](https://platform.openai.com/docs/guides/rate-limits)

3. **Upgrade your plan** if you need higher limits

4. **Use a different model** (some have higher limits)

### Error: "insufficient_quota" or "quota exceeded"

**What it means:** You've run out of credits or exceeded your usage limit.

**Solutions:**

1. **Add credits:**
   - OpenRouter: [openrouter.ai/credits](https://openrouter.ai/credits)
   - OpenAI: [platform.openai.com/account/billing](https://platform.openai.com/account/billing)

2. **Enable billing** if not already enabled

3. **Check your usage:**
   - OpenRouter: [openrouter.ai/activity](https://openrouter.ai/activity)
   - OpenAI: [platform.openai.com/usage](https://platform.openai.com/usage)

4. **Use free tier models:**
   ```bash
   heal config
   # Select: OpenRouter → arcee-ai/trinity-large-preview:free
   ```

### Error: "model not found" or "invalid model"

**What it means:** The model name is incorrect or you don't have access.

**Solutions:**

1. **Check available models:**
   - OpenRouter: [openrouter.ai/models](https://openrouter.ai/models)
   - OpenAI: [platform.openai.com/docs/models](https://platform.openai.com/docs/models)

2. **Reconfigure with a known model:**
   ```bash
   heal config
   ```

3. **Verify model name format:**
   ```bash
   cat ~/.heal/.env
   ```
   
   For OpenRouter, model should be like: `openai/gpt-5.4-mini` (without the `openrouter/` prefix - heal adds it automatically)

### "Heal is not configured yet"

**Solution:**
```bash
heal config
```

Or run `heal test` which will offer to configure automatically.

### Configuration file corrupted

**Solution:**
```bash
# Backup old config
cp ~/.heal/.env ~/.heal/.env.backup

# Remove and reconfigure
rm ~/.heal/.env
heal config
```

### Can't find configuration

**Check location:**
```bash
ls -la ~/.heal/
cat ~/.heal/.env
```

**Expected location:** `~/.heal/.env`

### "No error input detected"

**Cause:** Heal can't see the error output.

**Solutions:**

1. **Use heal init:**
   ```bash
   heal init
   source ~/.bashrc
   ```

2. **Pipe errors manually:**
   ```bash
   your_command 2>&1 | heal
   ```

3. **Check if bash integration is active:**
   ```bash
   heal-last    # Should show last command
   heal-output  # Should show last output
   ```

### Helper commands not working

**Cause:** Bash integration not loaded.

**Solution:**
```bash
source ~/.bashrc
# or
source ~/.heal/heal.bash
```

**Verify it's in bashrc:**
```bash
grep heal ~/.bashrc
```

Should show:
```
source /home/user/.heal/heal.bash
```

### Error: "Connection refused" or "timeout"

**Solutions:**

1. **Check internet connection:**
   ```bash
   ping openrouter.ai
   ```

2. **Check firewall/proxy settings**

3. **Try a different network**

4. **Verify provider status:**
   - OpenRouter: [status.openrouter.ai](https://status.openrouter.ai)
   - OpenAI: [status.openai.com](https://status.openai.com)

### "heal: command not found"

**Solutions:**

1. **Check if installed:**
   ```bash
   pip list | grep heal
   ```

2. **Reinstall:**
   ```bash
   pip install --upgrade heal
   ```

3. **Check PATH:**
   ```bash
   which heal
   # or
   python -m heal.cli --help
   ```

4. **Use full path:**
   ```bash
   ~/.local/bin/heal
   ```

### Import errors

**Solution:**
```bash
pip install --upgrade heal
# or
pip install -e ".[dev]"
```

### OpenRouter

**Issue:** "LLM Provider NOT provided"

**Solution:** This is now fixed automatically. If you still see it:
```bash
heal config
# Reconfigure to ensure proper setup
```

**Issue:** Model not available

**Check:** [openrouter.ai/models](https://openrouter.ai/models) for available models

### OpenAI

**Issue:** "This model is not available"

**Solution:** Some models require special access. Use `gpt-5.4-mini` or `gpt-3.5-turbo` which are generally available.

### Anthropic

**Issue:** "Invalid API key"

**Solution:** Anthropic keys start with `sk-ant-`. Make sure you're using the correct key format.

### Google AI

**Issue:** "API key not valid"

**Solution:** Google AI keys don't have a prefix. Make sure you copied the entire key from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

### Enable debug mode

For litellm debugging, you can add to your Python code:
```python
import litellm
litellm.set_verbose = True
```

### Check logs

View heal configuration:
```bash
cat ~/.heal/.env
```

View captured data:
```bash
cat ~/.heal/last_command.txt
cat ~/.heal/last_output.txt
cat ~/.heal/last_exit_code.txt
```

# Remove config
mv ~/.heal ~/.heal.backup

### Report an issue

If you've tried everything and it still doesn't work:

1. Run `heal test` and save the output
2. Check `~/.heal/.env` (remove your API key before sharing!)
3. Report at: [github.com/yourusername/heal/issues](https://github.com/yourusername/heal/issues)

Include:
- Output of `heal test`
- Your provider and model (without API key)
- Operating system
- Python version: `python --version`
- Heal version: `pip show heal`

## Quick Fixes Checklist

- [ ] Run `heal test` to diagnose
- [ ] Check API key is valid
- [ ] Verify provider matches API key
- [ ] Ensure you have credits/billing enabled
- [ ] Try a different model
- [ ] Check internet connection
- [ ] Reconfigure: `heal config`
- [ ] Reinstall: `pip install --upgrade heal`
- [ ] Check bash integration: `source ~/.bashrc`

## Common Error Messages

| Error | Likely Cause | Quick Fix |
|-------|--------------|-----------|
| "Missing Authentication header" | Invalid/missing API key | `heal config` |
| "rate_limit_exceeded" | Too many requests | Wait 60 seconds |
| "insufficient_quota" | Out of credits | Add credits to account |
| "model not found" | Wrong model name | `heal config` → select valid model |
| "No error input detected" | No piped input | Use `heal init` or pipe: `cmd 2>&1 \| heal` |
| "heal: command not found" | Not installed | `pip install heal` |
| "Connection refused" | Network issue | Check internet connection |
