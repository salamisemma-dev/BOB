#!/usr/bin/env bash
# Make the BOB gate ENFORCING (not advisory) by requiring its CI check before merge.
# Requires GitHub CLI auth with repository administration permission.
set -euo pipefail

repo="${1:?usage: enable-branch-protection.sh owner/repo [branch] [required-check]}"
branch="${2:-main}"
check="${3:-bob-validate}"

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI is required. Install GitHub CLI and run: gh auth login" >&2
  exit 1
fi

gh api --method PUT "repos/${repo}/branches/${branch}/protection" \
  --field required_status_checks.strict=true \
  --raw-field "required_status_checks.contexts[]=${check}" \
  --field enforce_admins=true \
  --field required_pull_request_reviews.required_approving_review_count=1 \
  --field required_pull_request_reviews.dismiss_stale_reviews=true \
  --field required_pull_request_reviews.require_code_owner_reviews=false \
  --field restrictions=null \
  --field required_linear_history=false \
  --field allow_force_pushes=false \
  --field allow_deletions=false \
  --field required_conversation_resolution=true

echo "Enabled branch protection for ${repo}:${branch}; required check: ${check}"
echo "A red BOB gate now blocks merge. That closes the last code-level anti-vibe gap."
