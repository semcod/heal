"""
Tests for the privacy module.

Tests cover:
- Built-in regex masking (emails, phones, IDs, secrets, IPs, etc.)
- PrivacyMasker class initialization and methods
- anonymize_shell_output convenience function
- get_privacy_status reporting
- Edge cases: empty text, no matches, overlapping patterns
- Selective masking (enable/disable specific categories)
"""

from heal.privacy import (
    PrivacyMasker,
    anonymize_shell_output,
    get_privacy_status,
)


# -----------------------------------------------------------------------
# Built-in regex: Email masking
# -----------------------------------------------------------------------


class TestEmailMasking:
    def test_simple_email(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Contact john@example.com for details")
        assert "[EMAIL]" in result
        assert "john@example.com" not in result

    def test_multiple_emails(self) -> None:
        masker = PrivacyMasker()
        text = "From: alice@test.org To: bob@company.co.uk"
        result = masker.anonymize(text)
        assert result.count("[EMAIL]") == 2
        assert "alice@test.org" not in result
        assert "bob@company.co.uk" not in result

    def test_email_with_plus(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("user+tag@gmail.com")
        assert "[EMAIL]" in result

    def test_email_with_dots(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("first.last@example.com")
        assert "[EMAIL]" in result

    def test_no_email(self) -> None:
        masker = PrivacyMasker()
        text = "No email addresses here"
        result = masker.anonymize(text)
        assert "[EMAIL]" not in result
        assert result == text


# -----------------------------------------------------------------------
# Built-in regex: Phone masking
# -----------------------------------------------------------------------


class TestPhoneMasking:
    def test_polish_phone(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Call +48 123 456 789")
        assert "[PHONE]" in result
        assert "123 456 789" not in result

    def test_polish_phone_no_prefix(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Call 123 456 789")
        assert "[PHONE]" in result

    def test_us_phone(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Call 555-123-4567")
        assert "[PHONE]" in result

    def test_phone_with_dashes(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Phone: 123-456-789")
        assert "[PHONE]" in result


# -----------------------------------------------------------------------
# Built-in regex: ID number masking
# -----------------------------------------------------------------------


class TestIDMasking:
    def test_pesel(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("PESEL: 92010112345")
        assert "[ID_NUMBER]" in result
        assert "92010112345" not in result

    def test_credit_card(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Card: 4111 1111 1111 1111")
        assert "[CARD_NUMBER]" in result
        assert "4111" not in result

    def test_credit_card_no_spaces(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Card: 4111111111111111")
        assert "[CARD_NUMBER]" in result

    def test_ssn(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("SSN: 123-45-6789")
        assert "[SSN]" in result
        assert "123-45-6789" not in result


# -----------------------------------------------------------------------
# Built-in regex: IP address masking
# -----------------------------------------------------------------------


class TestIPMasking:
    def test_ipv4(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Server at 192.168.1.100")
        assert "[IP_ADDRESS]" in result
        assert "192.168.1.100" not in result

    def test_localhost(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Connect to 127.0.0.1:5432")
        assert "[IP_ADDRESS]" in result


# -----------------------------------------------------------------------
# Built-in regex: Secret / credential masking
# -----------------------------------------------------------------------


class TestSecretMasking:
    def test_aws_key(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("AWS_KEY=AKIAIOSFODNN7EXAMPLE")
        assert "[AWS_KEY]" in result
        assert "AKIAIOSFODNN7EXAMPLE" not in result

    def test_github_token(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn")
        assert "[GITHUB_TOKEN]" in result

    def test_bearer_token(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc.def")
        assert "[BEARER_TOKEN]" in result or "[JWT_TOKEN]" in result

    def test_private_key_pem(self) -> None:
        masker = PrivacyMasker()
        pem = "-----BEGIN RSA PRIVATE KEY-----\nMIIBogIBAAJ...\n-----END RSA PRIVATE KEY-----"
        result = masker.anonymize(pem)
        assert "[PRIVATE_KEY]" in result
        assert "MIIBogIBAAJ" not in result

    def test_jwt_token(self) -> None:
        masker = PrivacyMasker()
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
        result = masker.anonymize(jwt)
        assert "[JWT_TOKEN]" in result

    def test_ssh_key(self) -> None:
        masker = PrivacyMasker()
        ssh = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7FAKEKEYDATA1234567890abcdefgh user@host"
        result = masker.anonymize(ssh)
        assert "[SSH_KEY]" in result

    def test_generic_api_key(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("api_key=sk_test_fake_key_1234567890abcdef")
        assert "[SECRET]" in result

    def test_password_in_env(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("password=MyVerySecretPassword123!")
        assert "[SECRET]" in result
        assert "MyVerySecretPassword123" not in result

    def test_db_connection_string(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize(
            "postgresql://admin:s3cret_pass@db.host.com:5432/mydb"
        )
        assert "[DB_PASSWORD]" in result
        assert "s3cret_pass" not in result

    def test_mysql_connection(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("mysql://root:password123@localhost/db")
        assert "[DB_PASSWORD]" in result

    def test_redis_connection(self) -> None:
        masker = PrivacyMasker()
        result = masker.anonymize("redis://user:authpass@redis.host:6379")
        assert "[DB_PASSWORD]" in result


# -----------------------------------------------------------------------
# Combined / realistic scenarios
# -----------------------------------------------------------------------


class TestRealisticScenarios:
    def test_python_error_with_email(self) -> None:
        masker = PrivacyMasker()
        text = """Traceback (most recent call last):
  File "app.py", line 42, in send_notification
    smtp.sendmail("admin@company.com", "user@example.org", msg)
SMTPAuthenticationError: (535, 'Authentication failed for admin@company.com')"""
        result = masker.anonymize(text)
        assert "admin@company.com" not in result
        assert "user@example.org" not in result
        assert "Traceback" in result
        assert "SMTPAuthenticationError" in result

    def test_docker_error_with_ip(self) -> None:
        masker = PrivacyMasker()
        text = """Error: connect ECONNREFUSED 192.168.1.50:5432
    at TCPConnectWrap.afterConnect [as oncomplete]
Connection to database at 10.0.0.15 failed"""
        result = masker.anonymize(text)
        assert "192.168.1.50" not in result
        assert "10.0.0.15" not in result
        assert "ECONNREFUSED" in result

    def test_git_error_with_token(self) -> None:
        masker = PrivacyMasker()
        text = """remote: Invalid username or password.
fatal: Authentication failed for 'https://ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn@github.com/user/repo.git'"""
        result = masker.anonymize(text)
        assert "ghp_ABCDEF" not in result

    def test_env_file_leak(self) -> None:
        masker = PrivacyMasker()
        text = """Error loading .env:
API_KEY=sk_test_fake_key_abcdef1234567890abcdef12
DATABASE_URL=postgresql://admin:supersecret@db.prod.com:5432/app
SMTP_PASSWORD=mysecretpassword123"""
        result = masker.anonymize(text)
        assert "sk_test_fake_key" not in result
        assert "supersecret" not in result
        assert "mysecretpassword123" not in result

    def test_shell_log_with_mixed_pii(self) -> None:
        masker = PrivacyMasker()
        text = """[ERROR] User jan.kowalski@firma.pl (PESEL: 92010112345)
failed login from 10.20.30.40. Card ending 4111 1111 1111 1111."""
        result = masker.anonymize(text)
        assert "jan.kowalski@firma.pl" not in result
        assert "92010112345" not in result
        assert "10.20.30.40" not in result
        assert "4111" not in result


# -----------------------------------------------------------------------
# Selective masking (enable/disable categories)
# -----------------------------------------------------------------------


class TestSelectiveMasking:
    def test_disable_contacts(self) -> None:
        masker = PrivacyMasker()
        text = "Email: user@test.com, PESEL: 12345678901"
        result = masker.anonymize(text, mask_contacts=False, mask_pii=True)
        # With mask_contacts=False, email should still be there
        # (the _mask_pii skips EMAIL when mask_contacts=False)
        assert "user@test.com" in result
        assert "12345678901" not in result

    def test_disable_ids(self) -> None:
        masker = PrivacyMasker()
        text = "Email: user@test.com, PESEL: 12345678901"
        result = masker.anonymize(text, mask_ids=False)
        assert "user@test.com" not in result
        assert "12345678901" in result

    def test_disable_secrets(self) -> None:
        masker = PrivacyMasker()
        text = "api_key=sk_test_fake_key_1234567890abcdef email: a@b.com"
        result = masker.anonymize(text, mask_secrets=False)
        # Secret should remain but email should be masked
        assert "sk_test_fake_key" in result
        assert "a@b.com" not in result

    def test_disable_all_pii(self) -> None:
        masker = PrivacyMasker()
        text = "user@test.com 123-456-7890"
        result = masker.anonymize(text, mask_pii=False, mask_secrets=False)
        assert result == text


# -----------------------------------------------------------------------
# Edge cases
# -----------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_text(self) -> None:
        masker = PrivacyMasker()
        assert masker.anonymize("") == ""

    def test_no_sensitive_data(self) -> None:
        masker = PrivacyMasker()
        text = "make: *** [Makefile:10: build] Error 1"
        result = masker.anonymize(text)
        assert result == text

    def test_whitespace_only(self) -> None:
        masker = PrivacyMasker()
        assert masker.anonymize("   \n\n  ") == "   \n\n  "

    def test_unicode_text(self) -> None:
        masker = PrivacyMasker()
        text = "Błąd: użytkownik jan@example.com nie znaleziony"
        result = masker.anonymize(text)
        assert "[EMAIL]" in result
        assert "Błąd" in result

    def test_very_long_text(self) -> None:
        masker = PrivacyMasker()
        text = "Error: " + "x" * 10000 + " user@test.com"
        result = masker.anonymize(text)
        assert "[EMAIL]" in result

    def test_multiple_same_email(self) -> None:
        masker = PrivacyMasker()
        text = "From: a@b.com To: a@b.com CC: a@b.com"
        result = masker.anonymize(text)
        assert "a@b.com" not in result
        assert result.count("[EMAIL]") == 3


# -----------------------------------------------------------------------
# PrivacyMasker class API
# -----------------------------------------------------------------------


class TestPrivacyMaskerAPI:
    def test_is_available(self) -> None:
        masker = PrivacyMasker()
        assert masker.is_available() is True

    def test_available_backends_always_has_builtin(self) -> None:
        masker = PrivacyMasker()
        backends = masker.available_backends()
        assert "builtin_regex" in backends
        assert isinstance(backends, list)

    def test_get_install_instructions_is_string(self) -> None:
        result = PrivacyMasker.get_install_instructions()
        assert isinstance(result, str)

    def test_init_default_language(self) -> None:
        masker = PrivacyMasker()
        assert masker.language == "pl"

    def test_init_custom_language(self) -> None:
        masker = PrivacyMasker(language="en")
        assert masker.language == "en"

    def test_init_faker_disabled_by_default(self) -> None:
        masker = PrivacyMasker()
        assert masker.use_faker is False


# -----------------------------------------------------------------------
# Module-level functions
# -----------------------------------------------------------------------


class TestModuleFunctions:
    def test_anonymize_shell_output_disabled(self) -> None:
        text = "user@test.com"
        result = anonymize_shell_output(text, enable_privacy=False)
        assert result == text

    def test_anonymize_shell_output_enabled(self) -> None:
        text = "Error for user@test.com"
        result = anonymize_shell_output(text, enable_privacy=True)
        assert "[EMAIL]" in result
        assert "user@test.com" not in result

    def test_anonymize_shell_output_with_options(self) -> None:
        text = "user@test.com PESEL: 12345678901"
        result = anonymize_shell_output(text, enable_privacy=True, mask_ids=False)
        assert "[EMAIL]" in result
        assert "12345678901" in result

    def test_get_privacy_status_keys(self) -> None:
        status = get_privacy_status()
        assert "available" in status
        assert "backends" in status
        assert "detect_secrets_installed" in status
        assert "presidio_installed" in status
        assert "priv_masker_installed" in status
        assert "datafog_installed" in status
        assert "faker_installed" in status
        assert "install_instructions" in status

    def test_get_privacy_status_available_is_true(self) -> None:
        status = get_privacy_status()
        assert status["available"] is True

    def test_get_privacy_status_backends_list(self) -> None:
        status = get_privacy_status()
        assert isinstance(status["backends"], list)
        assert "builtin_regex" in status["backends"]


# -----------------------------------------------------------------------
# Static method tests
# -----------------------------------------------------------------------


class TestStaticMethods:
    def test_mask_secrets_static(self) -> None:
        result = PrivacyMasker._mask_secrets("AKIAIOSFODNN7EXAMPLE")
        assert "[AWS_KEY]" in result

    def test_mask_pii_static(self) -> None:
        result = PrivacyMasker._mask_pii(
            "user@test.com", mask_contacts=True, mask_ids=True
        )
        assert "[EMAIL]" in result

    def test_mask_pii_contacts_disabled(self) -> None:
        result = PrivacyMasker._mask_pii(
            "user@test.com", mask_contacts=False, mask_ids=True
        )
        assert "user@test.com" in result

    def test_mask_pii_ids_disabled(self) -> None:
        result = PrivacyMasker._mask_pii(
            "PESEL: 12345678901", mask_contacts=True, mask_ids=False
        )
        assert "12345678901" in result
