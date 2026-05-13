# Privacy Protection Guide

How to anonymize sensitive data before sending to LLM.

## Why Privacy Protection?

When using heal to fix errors, your shell output may contain sensitive information:
- **Personal names** (PERSNAME)
- **Email addresses and phone numbers** (CONTACT)
- **Home/work addresses** (ADDRESS)
- **ID numbers** (PESEL, credit cards, etc.)
- **Dates** (DATE)
- **Monetary amounts** (AMOUNT)

The `--anonymize` flag masks this data before sending it to the LLM provider.

### Basic Installation (Regex-based masking)

Heal includes basic regex-based masking by default:
```bash
pip install heal
```

This provides basic protection for:
- Email addresses → `[EMAIL]`
- Phone numbers → `[PHONE]`
- ID numbers (11 digits) → `[ID_NUMBER]`
- Credit card numbers → `[CARD_NUMBER]`

### Full Installation (Advanced masking with priv-masker)

For comprehensive privacy protection using Polish NLP:
```bash
# Install with privacy extras
pip install heal[privacy]

# Download Polish SpaCy model
python -m spacy download pl_nask-0.0.5
```

This provides advanced masking for:
- Personal names
- Addresses
- Dates
- Contact information
- ID numbers
- Monetary amounts

### Basic Usage

Add the `--anonymize` flag to any heal command:

```bash
# Pipe errors with anonymization
your_command 2>&1 | heal --anonymize

# Or with fix command explicitly
your_command 2>&1 | heal fix --anonymize

# With bash integration
your_failing_command
heal --anonymize
```

### Check Privacy Status

See what privacy protection is available:

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

Or if not fully installed:
```
🔒 Privacy Masking Status

Available: ✗
priv-masker installed: ✗
SpaCy model loaded: ✗

Privacy masking not available. Install with:
    pip install heal[privacy]
    python -m spacy download pl_nask-0.0.5
```

### Example 1: Masking Email in Error Output

**Original error:**
```bash
$ python send_email.py
Error: Failed to send email to john.doe@example.com
SMTP authentication failed for user john.doe@example.com
```

**With anonymization:**
```bash
$ python send_email.py 2>&1 | heal --anonymize

🔒 Anonymizing sensitive data...

# LLM receives:
Error: Failed to send email to [EMAIL]
SMTP authentication failed for user [EMAIL]
```

### Example 2: Masking Phone Numbers

**Original error:**
```bash
$ python sms_service.py
Failed to send SMS to +48 123 456 789
Invalid phone format: 123-456-789
```

**With anonymization:**
```bash
$ python sms_service.py 2>&1 | heal --anonymize

# LLM receives:
Failed to send SMS to [PHONE]
Invalid phone format: [PHONE]
```

### Example 3: Masking Personal Names (Advanced)

**Original error:**
```bash
$ python process_data.py
Processing record for Jan Kowalski
Address: ul. Marszałkowska 1, Warszawa
PESEL: 92010112345
```

**With full privacy protection:**
```bash
$ python process_data.py 2>&1 | heal --anonymize

🔒 Anonymizing sensitive data...

# LLM receives:
Processing record for [PERSNAME]
Address: [ADDRESS]
PESEL: [ID_NUMBER]
```

### Example 4: Database Connection Errors

**Original error:**
```bash
$ python db_connect.py
Connection failed: postgresql://admin:secret123@db.company.com:5432/production
Error: Authentication failed for user admin@company.com
```

**With anonymization:**
```bash
$ python db_connect.py 2>&1 | heal --anonymize

# LLM receives:
Connection failed: postgresql://admin:secret123@db.company.com:5432/production
Error: Authentication failed for user [EMAIL]
```

Note: Passwords in connection strings are NOT automatically masked. Be careful with connection strings!

### With Basic Masking (Default)

| Type | Pattern | Replacement |
|------|---------|-------------|
| Email | `user@domain.com` | `[EMAIL]` |
| Phone (PL) | `+48 123 456 789` | `[PHONE]` |
| Phone (US) | `123-456-7890` | `[PHONE]` |
| PESEL | `92010112345` (11 digits) | `[ID_NUMBER]` |
| Credit Card | `1234 5678 9012 3456` | `[CARD_NUMBER]` |

### With Full Privacy Protection (priv-masker)

| Type | Example | Replacement |
|------|---------|-------------|
| Personal Name | `Jan Kowalski` | `[PERSNAME]` |
| Date | `2024-02-21` | `[DATE]` |
| Address | `ul. Marszałkowska 1` | `[ADDRESS]` |
| Email | `user@domain.com` | `[CONTACT]` |
| Phone | `+48 123 456 789` | `[CONTACT]` |
| PESEL | `92010112345` | `[ID_NUMBER]` |
| Amount | `1000 PLN` | `[AMOUNT]` |

## Configuration Options

You can customize what gets masked by modifying the code in `heal/privacy.py`:

```python
# In heal/cli.py, fix command
error_output = anonymize_shell_output(
    error_output,
    enable_privacy=True,
    mask_names=True,        # Mask personal names
    mask_dates=False,       # Keep dates (useful for debugging)
    mask_contacts=True,     # Mask email/phone
    mask_addresses=True,    # Mask addresses
    mask_ids=True,          # Mask ID numbers
    mask_amounts=False,     # Keep amounts (useful for debugging)
)
```

# Production errors - always anonymize
production_script.py 2>&1 | heal --anonymize
```

### 2. Check Before Sending

If you want to see what will be sent to the LLM:

```bash
# Run with anonymization and save output
your_command 2>&1 | tee error.log
cat error.log | heal --anonymize
```

### 3. Use with Bash Integration

Set up an alias for automatic anonymization:

```bash
# Add to ~/.bashrc
alias healp='heal --anonymize'

# Use it
your_command
healp
```

### 4. Verify Privacy Status

Before working with sensitive data:

```bash
heal fix --privacy-check
```

### 5. Be Aware of Limitations

Anonymization is NOT perfect. Always review:
- **Connection strings** - may contain passwords
- **API keys** - not automatically detected
- **Custom sensitive data** - domain-specific secrets

### What Anonymization Does

✅ Masks common PII patterns
✅ Removes personal names, emails, phones
✅ Protects ID numbers
✅ Hides addresses

### What Anonymization Does NOT Do

❌ Does not mask API keys or tokens
❌ Does not detect custom sensitive data
❌ Does not mask passwords in connection strings
❌ Does not prevent all data leakage

### Additional Protection

For maximum security:

1. **Review before sending:**
   ```bash
   # Save anonymized output first
   your_command 2>&1 > error.log
   cat error.log | heal --anonymize > anonymized.log
   # Review anonymized.log before sending
   ```

2. **Use environment variables:**
   ```bash
   # Instead of hardcoding secrets
   export DB_PASSWORD="secret"
   # Use in code: os.getenv("DB_PASSWORD")
   ```

3. **Sanitize connection strings:**
   ```bash
   # Before: postgresql://user:pass@host/db
   # Manually replace: postgresql://user:****@host/db
   ```

4. **Use local LLM providers:**
   ```bash
   # Configure heal with local provider
   heal config
   # Select a local/on-premise LLM
   ```

### "Privacy masking not available"

**Cause:** priv-masker not installed

**Solution:**
```bash
pip install heal[privacy]
python -m spacy download pl_nask-0.0.5
```

### "Using basic regex-based masking as fallback"

**Cause:** SpaCy model not loaded

**Solution:**
```bash
python -m spacy download pl_nask-0.0.5
```

### "Model 'pl_nask' not found"

**Cause:** Wrong model name or version

**Solution:**
```bash
# Try specific version
python -m spacy download pl_nask-0.0.5

# Or check available models
python -m spacy info
```

### Anonymization Too Aggressive

**Cause:** Masking removes useful debugging info

**Solution:** Customize masking options in code:
```python
# Keep dates and amounts for debugging
mask_dates=False,
mask_amounts=False,
```

### Some Data Not Masked

**Cause:** Pattern not recognized

**Solution:** 
1. Use full privacy protection (priv-masker)
2. Report the pattern for future improvement
3. Manually redact before sending

## Performance Impact

Anonymization adds minimal overhead:

- **Basic masking:** ~1ms (regex)
- **Full masking:** ~100-500ms (NLP processing)

For most use cases, this is negligible.

## Privacy Policy Compliance

Using `--anonymize` helps comply with:

- **GDPR** - Minimizes personal data sent to third parties
- **RODO** (Polish GDPR) - Protects Polish citizens' data
- **Company policies** - Prevents accidental data leakage

Always check your organization's data handling policies.

## Alternative: Local LLM

For maximum privacy, use a local LLM provider:

```bash
# No data leaves your machine
your_command 2>&1 | heal
```

# Check privacy status
heal fix --privacy-check

# With bash integration
your_command
heal --anonymize

# Install full privacy protection
pip install heal[privacy]
python -m spacy download pl_nask-0.0.5

# Create alias for convenience
alias healp='heal --anonymize'
```

## Summary

Privacy protection in heal:
- ✅ Easy to use with `--anonymize` flag
- ✅ Basic protection included by default
- ✅ Advanced protection with optional dependency
- ✅ Transparent - see what's being masked
- ✅ Customizable - control what gets masked
- ⚠️ Not perfect - always review sensitive data
- 💡 Best used with local LLM for maximum privacy
