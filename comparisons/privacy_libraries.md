## Overview

| Feature | heal (built-in) | detect-secrets | presidio | priv-masker | datafog | faker |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Emails** | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| **Phone numbers** | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| **API keys** | ✅ | ✅ | — | — | — | — |
| **Private keys (PEM/SSH)** | ✅ | ✅ | — | — | — | — |
| **JWT tokens** | ✅ | ✅ | — | — | — | — |
| **AWS keys** | ✅ | ✅ | — | — | — | — |
| **GitHub tokens** | ✅ | ✅ | — | — | — | — |
| **DB connection strings** | ✅ | ✅ | — | — | — | — |
| **Personal names** | — | — | ✅ | ✅ | ✅ | ✅ |
| **Addresses** | — | — | ✅ | ✅ | — | ✅ |
| **PESEL / national IDs** | ✅ | — | ✅ | ✅ | — | ✅ |
| **Credit cards** | ✅ | — | ✅ | — | — | ✅ |
| **SSN** | ✅ | — | ✅ | — | ✅ | ✅ |
| **IP addresses** | ✅ | — | ✅ | — | — | — |
| **Dates** | — | — | ✅ | ✅ | — | ✅ |
| **Multilingual** | — | — | ✅ | PL only | — | ✅ |
| **Fake data replacement** | — | — | — | — | — | ✅ |
| **No dependencies** | ✅ | — | — | — | — | — |
| **Install size** | 0 KB | ~2 MB | ~50 MB | ~200 MB | ~2 MB | ~5 MB |

## Why heal combines multiple backends

No single library covers all categories. heal layers them:

```
Shell output
  │
  ├─ 1. Built-in regex ──── emails, phones, IDs, API keys, tokens, IPs
  ├─ 2. detect-secrets ──── high-entropy strings, cloud keys, PEM
  ├─ 3. presidio ────────── NLP-based PII (names, addresses, dates)
  ├─ 4. priv-masker ─────── Polish-specific NLP
  └─ 5. Cleaned text → LLM
```

## detect-secrets

**By:** Yelp / open source  
**Install:** `pip install detect-secrets`  
**PyPI:** [pypi.org/project/detect-secrets](https://pypi.org/project/detect-secrets/)  
**GitHub:** [github.com/Yelp/detect-secrets](https://github.com/Yelp/detect-secrets)

**Strengths:**
- Best-in-class secret detection (API keys, tokens, private keys)
- Entropy-based scanning catches unknown secret formats
- Widely used in CI/CD pipelines
- CLI-friendly: `detect-secrets scan file.txt`

**Weaknesses:**
- Does not detect PII (names, emails, addresses)
- Cannot mask inline — detection only, not replacement
- Focused on files, not streaming text

**In heal:** Used as secondary scanner for secrets that regex patterns miss.

## presidio-analyzer

**By:** Microsoft  
**Install:** `pip install presidio-analyzer`  
**PyPI:** [pypi.org/project/presidio-analyzer](https://pypi.org/project/presidio-analyzer/)  
**GitHub:** [github.com/microsoft/presidio](https://github.com/microsoft/presidio)

**Strengths:**
- Enterprise-grade PII detection
- Multilingual support (EN, DE, ES, IT, PT, FR, etc.)
- NLP-based — detects names, addresses, dates contextually
- Extensible with custom recognizers
- Active Microsoft maintenance

**Weaknesses:**
- Heavy dependency (~50 MB+ with SpaCy models)
- Slow on large texts
- Does not detect secrets/API keys
- Requires SpaCy language models

**In heal:** Used for contextual PII detection (names, addresses) when installed.

## priv-masker

**By:** Polish open source community  
**Install:** `pip install priv-masker` + `python -m spacy download pl_nask-0.0.5`  
**PyPI:** [pypi.org/project/priv-masker](https://pypi.org/project/priv-masker/)

**Strengths:**
- Polish NLP-native (PESEL, Polish names, addresses)
- Tailored for RODO/GDPR compliance in Poland
- Integrated pipeline with SpaCy

**Weaknesses:**
- Polish language only
- Requires large SpaCy model (~200 MB)
- Smaller community, fewer updates
- No secrets detection

**In heal:** Used for Polish-specific NLP anonymization.

## datafog

**By:** DataFog  
**Install:** `pip install datafog`  
**PyPI:** [pypi.org/project/datafog](https://pypi.org/project/datafog/)  
**GitHub:** [github.com/datafog/datafog-python](https://github.com/datafog/datafog-python)

**Strengths:**
- Very lightweight (<2 MB)
- Fast pattern-based detection
- CLI: `datafog anonymize input.txt`
- Suitable for embedded/IoT (Raspberry Pi)

**Weaknesses:**
- Limited entity types
- No NLP-based detection
- Smaller community
- No secrets detection

**In heal:** Available as lightweight alternative to presidio.

## faker

**By:** joke2k  
**Install:** `pip install faker`  
**PyPI:** [pypi.org/project/Faker](https://pypi.org/project/Faker/)  
**GitHub:** [github.com/joke2k/faker](https://github.com/joke2k/faker)

**Strengths:**
- Generates realistic fake data (names, addresses, emails, etc.)
- 60+ locales including Polish
- Great for test data generation
- Can replace PII with believable fakes (not just `[MASKED]`)

**Weaknesses:**
- Not a detection tool — only generates replacements
- Needs to be combined with a detector
- No secrets handling

**In heal:** Can generate realistic fake data replacements instead of `[PLACEHOLDER]` tags.

# + Secret scanning
pip install heal detect-secrets

# + PII detection (English/multilingual)
pip install heal presidio-analyzer

# + Polish NLP
pip install heal priv-masker spacy
python -m spacy download pl_nask-0.0.5

# + Fake data generation
pip install heal faker

# Everything
pip install heal[privacy]
```

## Choosing the Right Setup

| Use Case | Recommended |
|----------|-------------|
| Quick & light | Built-in regex only |
| DevOps / CI/CD | + detect-secrets |
| GDPR compliance (EN) | + presidio |
| RODO compliance (PL) | + priv-masker |
| Test data generation | + faker |
| Embedded / Raspberry Pi | + datafog |
| Maximum protection | All of the above |
