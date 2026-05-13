# Heal - Quick Start Guide

Get started with heal in 5 minutes! 🚀

## Installation

```bash
pip install heal
```

### 1. Configure

```bash
heal config
```

Choose OpenRouter (recommended) → Get API key → Select model

### 2. Test

```bash
heal test
```

Verify your configuration works

### 3. Initialize

```bash
heal init
```

Enable automatic command capture

### After `heal init`

Just run any command, then heal:

```bash
python app.py
heal
```

### Without init

Pipe errors to heal:

```bash
python app.py 2>&1 | heal
```

## That's it! 🎉

For more details, see:
- [Getting Started Guide](examples/getting_started.md)
- [Configuration Guide](examples/configuration_guide.md)
- [Examples](examples/README.md)

## Quick Commands

```bash
heal              # Fix last error
heal test         # Test configuration
heal config       # Change settings
heal init         # Setup bash integration
heal-last         # Show last command
heal-output       # Show last output

# Privacy options
heal -a           # Fix with anonymization
heal --anonymize  # Same as above (long form)
heal --no-anonymize  # Disable anonymization
```
