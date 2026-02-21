#!/usr/bin/env bash
# End-to-end tests for heal CLI
set -euo pipefail

PASS=0
FAIL=0
TOTAL=0

pass() { ((PASS++)); ((TOTAL++)); echo "  ✓ $1"; }
fail() { ((FAIL++)); ((TOTAL++)); echo "  ✗ $1"; }

echo "═══════════════════════════════════════════"
echo "  Heal CLI - End-to-End Tests"
echo "═══════════════════════════════════════════"
echo ""

# -------------------------------------------------------------------
echo "▸ heal --help"
if heal --help 2>&1 | grep -q "Heal - LLM-powered"; then
    pass "Shows help text"
else
    fail "Help text missing"
fi

# -------------------------------------------------------------------
echo "▸ heal fix --help"
if heal fix --help 2>&1 | grep -q "Fix shell errors"; then
    pass "fix --help works"
else
    fail "fix --help broken"
fi

# -------------------------------------------------------------------
echo "▸ heal test --help"
if heal test --help 2>&1 | grep -q "Test heal"; then
    pass "test --help works"
else
    fail "test --help broken"
fi

# -------------------------------------------------------------------
echo "▸ heal init --help"
if heal init --help 2>&1 | grep -q "Initialize bash"; then
    pass "init --help works"
else
    fail "init --help broken"
fi

# -------------------------------------------------------------------
echo "▸ heal config --help"
if heal config --help 2>&1 | grep -q "Configure"; then
    pass "config --help works"
else
    fail "config --help broken"
fi

# -------------------------------------------------------------------
echo "▸ heal fix --privacy-check"
if heal fix --privacy-check 2>&1 | grep -q "Privacy Masking Status"; then
    pass "privacy-check shows status"
else
    fail "privacy-check broken"
fi

if heal fix --privacy-check 2>&1 | grep -q "builtin_regex"; then
    pass "builtin_regex backend present"
else
    fail "builtin_regex backend missing"
fi

# -------------------------------------------------------------------
echo "▸ Piping errors to heal fix (no LLM key)"
OUTPUT=$(echo "ModuleNotFoundError: No module named 'flask'" | heal fix 2>&1 || true)
if echo "$OUTPUT" | grep -qiE "config|API key|provider|error"; then
    pass "Handles piped input (config prompt or error)"
else
    fail "Piped input not handled"
fi

# -------------------------------------------------------------------
echo "▸ Privacy anonymization via pipe"
OUTPUT=$(echo "Error: user@example.com failed, PESEL 92010112345" | python -c "
from heal.privacy import anonymize_shell_output
import sys
text = sys.stdin.read()
print(anonymize_shell_output(text, enable_privacy=True))
")
if echo "$OUTPUT" | grep -q "\[EMAIL\]"; then
    pass "Email anonymized"
else
    fail "Email not anonymized"
fi
if echo "$OUTPUT" | grep -q "\[ID_NUMBER\]"; then
    pass "ID number anonymized"
else
    fail "ID number not anonymized"
fi

# -------------------------------------------------------------------
echo "▸ Secret masking via Python"
OUTPUT=$(python -c "
from heal.privacy import PrivacyMasker
m = PrivacyMasker()
print(m.anonymize('api_key=sk_test_fake_key_1234567890abcdef'))
")
if echo "$OUTPUT" | grep -q "\[SECRET\]"; then
    pass "API key secret masked"
else
    fail "API key secret not masked"
fi

OUTPUT=$(python -c "
from heal.privacy import PrivacyMasker
m = PrivacyMasker()
print(m.anonymize('postgresql://admin:s3cret@db.com:5432/app'))
")
if echo "$OUTPUT" | grep -q "\[DB_PASSWORD\]"; then
    pass "DB password masked"
else
    fail "DB password not masked"
fi

# -------------------------------------------------------------------
echo "▸ Unit tests via pytest"
if python -m pytest tests/ -v --tb=short -q 2>&1 | tail -1 | grep -q "passed"; then
    pass "All pytest tests pass"
else
    fail "Some pytest tests failed"
fi

# -------------------------------------------------------------------
echo ""
echo "═══════════════════════════════════════════"
echo "  Results: $PASS passed, $FAIL failed (total $TOTAL)"
echo "═══════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
