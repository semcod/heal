"""
Privacy module for anonymizing sensitive data before sending to LLM.

Supports multiple anonymization backends:
- Built-in regex (always available) - emails, phones, IDs, API keys, tokens
- detect-secrets - API keys, tokens, private keys, high-entropy strings
- presidio-analyzer - Microsoft's PII detection (multilingual)
- datafog - lightweight PII detection
- priv-masker - Polish NLP-based anonymization
- faker - generate realistic fake data replacements

Usage:
    from heal.privacy import PrivacyMasker, anonymize_shell_output

    masker = PrivacyMasker()
    clean = masker.anonymize("Error for user john@example.com")
    # => "Error for user [EMAIL]"
"""

import re
import os
import tempfile
from typing import Dict, Any, List, Set

# ---------------------------------------------------------------------------
# Optional backend availability detection
# ---------------------------------------------------------------------------

PRIV_MASKER_AVAILABLE = False
try:
    import spacy
    from priv_masker import add_pipeline, analyse_text

    PRIV_MASKER_AVAILABLE = True
except ImportError:
    pass

DETECT_SECRETS_AVAILABLE = False
try:
    from detect_secrets import main as ds_main  # noqa: F401
    from detect_secrets.settings import default_settings

    DETECT_SECRETS_AVAILABLE = True
except ImportError:
    pass

PRESIDIO_AVAILABLE = False
try:
    from presidio_analyzer import AnalyzerEngine

    PRESIDIO_AVAILABLE = True
except ImportError:
    pass

DATAFOG_AVAILABLE = False
try:
    import datafog  # noqa: F401

    DATAFOG_AVAILABLE = True
except ImportError:
    pass

FAKER_AVAILABLE = False
try:
    from faker import Faker

    FAKER_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Regex patterns for built-in masking
# ---------------------------------------------------------------------------

# Secrets / credentials
_SECRET_PATTERNS = [
    # AWS keys
    (r"(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}", "[AWS_KEY]"),
    # GitHub tokens
    (r"gh[pousr]_[A-Za-z0-9_]{36,255}", "[GITHUB_TOKEN]"),
    # Generic API keys / passwords (preceded by key-like words, 12+ chars)
    (
        r'(?i)(?:api[_-]?key|apikey|secret[_-]?key|token|password|passwd|auth[_-]?token|auth)\s*[:=]\s*["\']?([A-Za-z0-9_\-\.!@#$%^&*]{12,})["\']?',
        "[SECRET]",
    ),
    # Bearer tokens
    (r"Bearer\s+[A-Za-z0-9_\-\.]+", "[BEARER_TOKEN]"),
    # Private keys (PEM)
    (
        r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        "[PRIVATE_KEY]",
    ),
    # JWT tokens
    (
        r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "[JWT_TOKEN]",
    ),
    # SSH keys in authorized_keys format
    (r"ssh-(?:rsa|ed25519|ecdsa)\s+[A-Za-z0-9+/=]{40,}", "[SSH_KEY]"),
    # Connection strings with passwords
    (
        r"(?i)((?:postgresql|mysql|mongodb|redis|amqp)://[^:]+:)([^@]+)(@)",
        r"\1[DB_PASSWORD]\3",
    ),
]

# PII patterns
_PII_PATTERNS = [
    # Emails
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
    # Phone numbers (PL)
    (r"\b(?:\+?48)?[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b", "[PHONE]"),
    # Phone numbers (US/intl)
    (r"\b\d{3}[-\s]?\d{3}[-\s]?\d{4}\b", "[PHONE]"),
    # IP addresses (v4)
    (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "[IP_ADDRESS]"),
    # PESEL (Polish national ID, 11 digits)
    (r"\b\d{11}\b", "[ID_NUMBER]"),
    # Credit card numbers
    (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CARD_NUMBER]"),
    # SSN (US)
    (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),
]


class PrivacyMasker:
    """Multi-backend anonymizer for shell output before sending to LLM.

    Combines multiple detection strategies:
    1. Built-in regex patterns (always available) - secrets + PII
    2. detect-secrets for API keys / tokens / private keys
    3. presidio-analyzer for multilingual PII
    4. priv-masker for Polish NLP
    5. datafog for lightweight PII
    6. faker for generating realistic replacements
    """

    def __init__(self, language: str = "pl", use_faker: bool = False):
        self.language = language
        self.use_faker = use_faker and FAKER_AVAILABLE
        self.fake = Faker(language) if self.use_faker else None

        # priv-masker
        self.nlp = None
        self._priv_masker_ready = False
        if PRIV_MASKER_AVAILABLE:
            try:
                if language == "pl":
                    self.nlp = spacy.load("pl_nask")
                    add_pipeline(self.nlp)
                    self._priv_masker_ready = True
            except OSError:
                pass

        # presidio
        self._presidio_engine = None
        if PRESIDIO_AVAILABLE:
            try:
                self._presidio_engine = AnalyzerEngine()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return True - built-in regex backend is always available."""
        return True

    def available_backends(self) -> List[str]:
        """Return list of available backend names."""
        backends = ["builtin_regex"]
        if DETECT_SECRETS_AVAILABLE:
            backends.append("detect_secrets")
        if PRESIDIO_AVAILABLE and self._presidio_engine:
            backends.append("presidio")
        if self._priv_masker_ready:
            backends.append("priv_masker")
        if DATAFOG_AVAILABLE:
            backends.append("datafog")
        if self.use_faker:
            backends.append("faker")
        return backends

    @staticmethod
    def get_install_instructions() -> str:
        """Return install hints for missing backends."""
        lines = []
        if not DETECT_SECRETS_AVAILABLE:
            lines.append(
                "  pip install detect-secrets        # API keys, tokens, private keys"
            )
        if not PRESIDIO_AVAILABLE:
            lines.append(
                "  pip install presidio-analyzer     # Microsoft PII detection"
            )
        if not PRIV_MASKER_AVAILABLE:
            lines.append("  pip install priv-masker spacy     # Polish NLP masking")
            lines.append("  python -m spacy download pl_nask-0.0.5")
        if not DATAFOG_AVAILABLE:
            lines.append(
                "  pip install datafog               # Lightweight PII detection"
            )
        if not FAKER_AVAILABLE:
            lines.append("  pip install faker                 # Fake data generation")
        if not lines:
            return ""
        return "Install additional privacy backends:\n" + "\n".join(lines)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def anonymize(
        self,
        text: str,
        mask_secrets: bool = True,
        mask_pii: bool = True,
        mask_names: bool = True,
        mask_dates: bool = False,
        mask_contacts: bool = True,
        mask_addresses: bool = True,
        mask_ids: bool = True,
        mask_amounts: bool = False,
    ) -> str:
        """Run all available backends to anonymize *text*.

        Order: secrets -> PII regex -> detect-secrets -> presidio -> priv-masker.
        Each layer works on the result of the previous one so overlapping
        detections do not clash.
        """
        result = text

        # 1. Built-in secret patterns
        if mask_secrets:
            result = self._mask_secrets(result)

        # 2. Built-in PII patterns
        if mask_pii:
            result = self._mask_pii(result, mask_contacts, mask_ids)

        # 3. detect-secrets
        if mask_secrets and DETECT_SECRETS_AVAILABLE:
            result = self._detect_secrets_scan(result)

        # 4. presidio
        if mask_pii and self._presidio_engine:
            result = self._presidio_scan(result)

        # 5. priv-masker (Polish NLP)
        if self._priv_masker_ready:
            result = self._priv_masker_scan(
                result,
                mask_names=mask_names,
                mask_dates=mask_dates,
                mask_contacts=mask_contacts,
                mask_addresses=mask_addresses,
                mask_ids=mask_ids,
                mask_amounts=mask_amounts,
            )

        return result

    # ------------------------------------------------------------------
    # Built-in regex backends
    # ------------------------------------------------------------------

    @staticmethod
    def _mask_secrets(text: str) -> str:
        """Mask secrets / credentials using built-in regex patterns."""
        result = text
        for pattern, replacement in _SECRET_PATTERNS:
            result = re.sub(pattern, replacement, result)
        return result

    @staticmethod
    def _mask_pii(text: str, mask_contacts: bool = True, mask_ids: bool = True) -> str:
        """Mask PII using built-in regex patterns."""
        result = text
        for pattern, replacement in _PII_PATTERNS:
            if not mask_contacts and replacement in ("[EMAIL]", "[PHONE]"):
                continue
            if not mask_ids and replacement in (
                "[ID_NUMBER]",
                "[CARD_NUMBER]",
                "[SSN]",
            ):
                continue
            result = re.sub(pattern, replacement, result)
        return result

    # ------------------------------------------------------------------
    # detect-secrets backend
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_secrets_scan(text: str) -> str:
        """Use detect-secrets to find and mask additional secrets."""
        if not DETECT_SECRETS_AVAILABLE:
            return text
        try:
            tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
            tmp.write(text)
            tmp.close()

            from detect_secrets.core.scan import scan_file

            with default_settings():
                secrets = scan_file(tmp.name)

            lines = text.splitlines(True)
            masked_lines: Set[int] = set()
            for secret in secrets:
                line_num = secret.line_number - 1
                if 0 <= line_num < len(lines) and line_num not in masked_lines:
                    raw = secret.secret_value or ""
                    if raw and raw in lines[line_num]:
                        lines[line_num] = lines[line_num].replace(
                            raw, "[DETECTED_SECRET]"
                        )
                    masked_lines.add(line_num)

            os.unlink(tmp.name)
            return "".join(lines)
        except Exception:
            return text

    # ------------------------------------------------------------------
    # presidio backend
    # ------------------------------------------------------------------

    def _presidio_scan(self, text: str) -> str:
        """Use presidio-analyzer to detect and mask PII entities."""
        if not self._presidio_engine:
            return text
        try:
            results = self._presidio_engine.analyze(
                text=text,
                language="en",
                score_threshold=0.5,
            )
            # Sort by start descending so replacements don't shift indices
            results = sorted(results, key=lambda r: r.start, reverse=True)
            result = text
            for r in results:
                tag = f"[{r.entity_type}]"
                result = result[: r.start] + tag + result[r.end :]
            return result
        except Exception:
            return text

    # ------------------------------------------------------------------
    # priv-masker backend (Polish NLP)
    # ------------------------------------------------------------------

    def _priv_masker_scan(self, text: str, **mask_options) -> str:
        """Use priv-masker with Polish SpaCy model."""
        if not self._priv_masker_ready:
            return text
        try:
            masked_components = {
                "persname_mask": mask_options.get("mask_names", True),
                "date_mask": mask_options.get("mask_dates", True),
                "contact_mask": mask_options.get("mask_contacts", True),
                "address_mask": mask_options.get("mask_addresses", True),
                "id_numbers_mask": mask_options.get("mask_ids", True),
                "amount_mask": mask_options.get("mask_amounts", False),
            }
            doc = self.nlp(text)
            return analyse_text(doc, masked_components)
        except Exception:
            return text


# ---------------------------------------------------------------------------
# Module-level convenience functions
# ---------------------------------------------------------------------------


def anonymize_shell_output(
    output: str,
    enable_privacy: bool = False,
    **mask_options,
) -> str:
    """Anonymize shell output before sending to LLM.

    Args:
        output: Shell command output
        enable_privacy: Whether to enable privacy masking
        **mask_options: Forwarded to ``PrivacyMasker.anonymize``

    Returns:
        Anonymized output or original if privacy is disabled
    """
    if not enable_privacy:
        return output
    masker = PrivacyMasker()
    return masker.anonymize(output, **mask_options)


def get_privacy_status() -> Dict[str, Any]:
    """Return a dict describing which backends are available."""
    masker = PrivacyMasker()
    backends = masker.available_backends()
    return {
        "available": True,
        "backends": backends,
        "detect_secrets_installed": DETECT_SECRETS_AVAILABLE,
        "presidio_installed": PRESIDIO_AVAILABLE,
        "priv_masker_installed": PRIV_MASKER_AVAILABLE,
        "datafog_installed": DATAFOG_AVAILABLE,
        "faker_installed": FAKER_AVAILABLE,
        "install_instructions": masker.get_install_instructions() or None,
    }
