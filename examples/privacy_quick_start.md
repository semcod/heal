# Privacy Protection - Quick Start

Get started with privacy protection in 2 minutes.

## Installation

### Option 1: Basic Protection (Included)

```bash
pip install heal
```

Provides regex-based masking for:
- Emails → `[EMAIL]`
- Phone numbers → `[PHONE]`
- ID numbers → `[ID_NUMBER]`

### Option 2: Full Protection (Recommended for Polish)

```bash
pip install heal[privacy]
python -m spacy download pl_nask-0.0.5
```

Adds advanced NLP-based masking for:
- Personal names → `[PERSNAME]`
- Addresses → `[ADDRESS]`
- Dates → `[DATE]`
- And more...

## Usage

### Basic Usage

Add privacy flags to any heal command:

```bash
# Pipe with anonymization (short flag)
your_command 2>&1 | heal -a

# Long form (same as above)
your_command 2>&1 | heal --anonymize

# With bash integration
your_command
heal -a

# Disable anonymization (if enabled by default)
heal --no-anonymize
```

### Default Settings

Configure default anonymization behavior:

```bash
# First-time setup - will ask about privacy
heal config

# Check current settings
heal config
```

### Check Status

See what's available:

```bash
heal fix --privacy-check
```

Output:
```
🔒 Privacy Masking Status

Available: ✓
priv-masker installed: ✓
SpaCy model loaded: ✓
```

## Examples

### Example 1: Email in Error

**Before:**
```bash
$ python send.py 2>&1 | heal
# Sends: "Error: Failed to send to john@example.com"
```

**After:**
```bash
$ python send.py 2>&1 | heal --anonymize
# Sends: "Error: Failed to send to [EMAIL]"
```

### Example 2: Phone Number

**Before:**
```bash
$ python sms.py 2>&1 | heal
# Sends: "Invalid phone: +48 123 456 789"
```

**After:**
```bash
$ python sms.py 2>&1 | heal --anonymize
# Sends: "Invalid phone: [PHONE]"
```

### Example 3: Personal Data (Full Protection)

**Before:**
```bash
$ python process.py 2>&1 | heal
# Sends: "Processing Jan Kowalski, ul. Marszałkowska 1, PESEL: 92010112345"
```

**After:**
```bash
$ python process.py 2>&1 | heal --anonymize
# Sends: "Processing [PERSNAME], [ADDRESS], PESEL: [ID_NUMBER]"
```

## Create Alias

For convenience:

```bash
# Add to ~/.bashrc
alias healp='heal --anonymize'

# Use it
your_command
healp
```

## When to Use

✅ **Always use for:**
- Production data
- Customer information
- Personal data (GDPR/RODO)
- Financial data
- Health data

⚠️ **Consider using for:**
- Development with real data
- Logs with user info
- Database errors
- API errors with tokens

❌ **Not needed for:**
- Synthetic test data
- Public information
- Generic errors

## Limitations

Privacy masking does NOT protect:
- API keys in code
- Passwords in connection strings
- Custom sensitive data patterns
- Secrets in environment variables

Always review output before sending sensitive data.

## Next Steps

- Read [Full Privacy Guide](privacy_protection.md)
- Check [Security Considerations](privacy_protection.md#security-considerations)
- Learn about [GDPR Compliance](privacy_protection.md#privacy-policy-compliance)

## Quick Reference

```bash
# Install full protection
pip install heal[privacy]
python -m spacy download pl_nask-0.0.5

# Check status
heal fix --privacy-check

# Use anonymization (short and long forms)
heal -a
heal --anonymize

# Disable anonymization
heal --no-anonymize

# Configure default behavior
heal config

# Create alias for quick access
alias healp='heal -a'
```
