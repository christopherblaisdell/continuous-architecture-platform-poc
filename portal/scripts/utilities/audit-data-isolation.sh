#!/usr/bin/env bash
# =============================================================================
# Data Isolation Audit Script
# =============================================================================
# Run this before every commit to check for corporate data leakage.
# This workspace must contain ONLY synthetic/fictional data (NovaTrek domain).
#
# Usage:
#   ./scripts/audit-data-isolation.sh          # audit all tracked + staged files
#   ./scripts/audit-data-isolation.sh --staged  # audit only staged files
# =============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

VIOLATIONS=0

# Determine which files to scan
if [[ "${1:-}" == "--staged" ]]; then
  FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(md|yaml|yml|json|py|java|puml|ts|js)$' || true)
  SCOPE="staged files"
else
  FILES=$(git ls-files | grep -E '\.(md|yaml|yml|json|py|java|puml|ts|js)$' || true)
  SCOPE="all tracked files"
fi

if [[ -z "$FILES" ]]; then
  echo -e "${GREEN}✓ No files to audit${NC}"
  exit 0
fi

echo "════════════════════════════════════════════════════════════"
echo " Data Isolation Audit — scanning ${SCOPE}"
echo "════════════════════════════════════════════════════════════"

# ---------------------------------------------------------------------------
# Pattern groups to check
# ---------------------------------------------------------------------------

check_pattern() {
  local label="$1"
  local pattern="$2"
  local matches

  matches=$(echo "$FILES" | xargs grep -rn -i "$pattern" 2>/dev/null | grep -v "audit-data-isolation.sh" | grep -v "grep -ri" || true)

  if [[ -n "$matches" ]]; then
    echo ""
    echo -e "${RED}✗ VIOLATION: ${label}${NC}"
    echo "$matches" | head -10
    count=$(echo "$matches" | wc -l | xargs)
    if [[ "$count" -gt 10 ]]; then
      echo "  ... and $((count - 10)) more"
    fi
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
}

# Real organization names
check_pattern "Organization names (UDX, UPR, NBCUniversal, Comcast)" \
  '\bUDX\b\|UPR\b\|\bNBCU\b\|nbcuniversal\|comcast'

# Real company context
check_pattern "Company context (Universal Destinations, theme park, resort)" \
  'Universal Destinations\|theme park operations\|entertainment company'

# Real internal tools
check_pattern "Internal tool names (VSFlow, real tool names)" \
  '\bVSFlow\b'

# Real service names (ms-xxx pattern from corporate repos)
check_pattern "Real microservice names (ms-acp, ms-hotel, ms-checkout, etc.)" \
  'ms-acp\|ms-hotel\|ms-checkout\|ms-guest\|ms-orders\|ms-biometrics\|ms-ohip\|ms-presence\|ms-entitlements'

# Real ticket ID patterns (use word boundary to prevent matching DEEP-RESEARCH-1 etc.)
check_pattern "Real ticket IDs (UPT-, ARCH- prefixes)" \
  '\bUPT-[0-9]\|\bARCH-[0-9]'

# Real infrastructure URLs
check_pattern "Internal URLs (nbcu-ot, atlassian internal, gitlab internal, ucdp)" \
  'nbcu-ot\|\.atlassian\.\|gitlab\.use\|ucdp\.net'

# Real repo names
check_pattern "Internal repo names (upr-services, etc.)" \
  '\bupr-services\b\|upr-diagrams'

# Real people (add names as needed — keep this list updated)
# check_pattern "Real people names" \
#   'specific-name-1\|specific-name-2'

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

echo ""
echo "════════════════════════════════════════════════════════════"
if [[ "$VIOLATIONS" -gt 0 ]]; then
  echo -e "${RED}  FAILED: ${VIOLATIONS} violation(s) found${NC}"
  echo "  Fix the above before committing."
  echo "════════════════════════════════════════════════════════════"
  exit 1
else
  echo -e "${GREEN}  PASSED: No corporate data detected in ${SCOPE}${NC}"
  echo "════════════════════════════════════════════════════════════"
  exit 0
fi
