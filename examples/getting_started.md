# Getting Started with Heal

Complete guide to setting up and using heal for the first time.

## Installation

```bash
pip install heal
```

### Step 1: Configure Your Provider

Run the configuration wizard:

```bash
heal config
```

You'll see:

```
🔧 First-time setup - Let's configure your LLM provider

Available providers:
  1. OpenRouter (recommended)
  2. OpenAI
  3. Anthropic
  4. Google AI

💡 Tip: OpenRouter gives you access to all models with one API key

Select provider [1]: 
```

**Recommendation:** Choose option 1 (OpenRouter) for access to all models.

### Step 2: Get Your API Key

The wizard will show you where to get your API key:

```
🔑 Get your OpenRouter API key here:
   https://openrouter.ai/keys

Enter your API key: 
```

1. Click the link (or visit it in your browser)
2. Sign up/login
3. Create an API key
4. Copy and paste it into heal

### Step 3: Select Your Model

Choose from popular models:

```
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

Select model [1]: 
```

**Recommendation:** Choose option 1 for best value.

### Step 4: Test Your Configuration

Verify everything works:

```bash
heal test
```

You'll see:

```
🧪 Testing heal configuration...

✓ Provider: OpenRouter
✓ Model: openai/gpt-5.4-mini
✓ API Key: ********************abc1

📝 Simulating error:
   Command: python app.py
   Error: ModuleNotFoundError: No module named 'flask'

🤖 Asking LLM for solution...

💡 LLM Response:
────────────────────────────────────────────────────────────
The error indicates Flask is not installed. Install it with:
pip install flask

If using a virtual environment, activate it first:
source venv/bin/activate
────────────────────────────────────────────────────────────

✅ Test successful! Heal is working correctly.
   You can now use: command 2>&1 | heal
```

### Step 5: Initialize Bash Integration (Optional but Recommended)

Set up automatic command capture:

```bash
heal init
```

This will:

```
✅ Heal bash integration created!

📄 Hook file: /home/user/.heal/heal.bash

📝 To activate, add this line to your ~/.bashrc:
   source /home/user/.heal/heal.bash

   Add to ~/.bashrc automatically? [Y/n]: y
   ✅ Added to ~/.bashrc

🔄 To activate now, run:
   source ~/.bashrc

📚 Usage after activation:
   1. Run any command (it will be captured automatically)
   2. If it fails, just run: heal
   3. Heal will analyze the error and suggest fixes

💡 Helper commands:
   heal-last    - Show last captured command
   heal-output  - Show last captured output
```

Press `y` to automatically add to your `.bashrc`.

### Step 6: Activate the Integration

```bash
source ~/.bashrc
```

### Basic Usage (Without Init)

Pipe errors directly to heal:

```bash
python broken_script.py 2>&1 | heal
```

### With Bash Integration (After Init)

Just run your command, then heal:

```bash
# Run a failing command
npm install some-package

# Fix it with heal
heal
```

Heal will automatically see the last command and its output!

### Using Helper Commands

Check what was captured:

```bash
### Debugging Python Errors

```bash
python app.py
heal
```

### Fixing npm Issues

```bash
npm install
heal
```

### Docker Build Problems

```bash
docker build .
heal
```

### Git Conflicts

```bash
git merge feature-branch
heal
```

### 1. Use heal test Regularly

Test your configuration anytime:

```bash
heal test
```

### 2. Reconfigure Easily

Switch providers or models:

```bash
heal config
```

### 3. Check Captured Data

Before running heal, verify what was captured:

```bash
heal-last     # Shows the command
heal-output   # Shows the output
```

### 4. Pipe Specific Errors

For commands that don't fail but have warnings:

```bash
make build 2>&1 | heal
```

### 5. Save Solutions

Copy heal's suggestions to a file:

```bash
heal > solution.txt
```

### "heal: command not found"

Make sure heal is installed:

```bash
pip install heal
# or
pip install --user heal
```

Add to PATH if needed:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### "No error input detected"

If you haven't run `heal init`, you need to pipe errors:

```bash
your_command 2>&1 | heal
```

Or run `heal init` to enable automatic capture.

### "Error calling LLM: ..."

Check your configuration:

```bash
heal config
```

Verify:
- API key is correct
- You have credits/billing enabled
- Internet connection is working

### Helper Commands Not Working

Make sure you've activated the bash integration:

```bash
source ~/.bashrc
```

Or run `heal init` if you haven't yet.

## Next Steps

- Read [Configuration Guide](configuration_guide.md) for advanced setup
- Check [Examples](README.md) for real-world error scenarios
- See [TODO.md](../TODO.md) for upcoming features

# Setup
heal config          # Configure provider and model
heal test           # Test configuration
heal init           # Setup bash integration

# Usage
heal                # Fix last error (with init)
command 2>&1 | heal # Fix piped error
heal < error.log    # Fix from file

# Helpers
heal-last           # Show last command
heal-output         # Show last output

# Management
heal config         # Reconfigure
heal uninstall      # Remove integration
```

## Getting Help

```bash
heal --help
```

For specific command help:

```bash
heal init --help
heal test --help
heal config --help
```
