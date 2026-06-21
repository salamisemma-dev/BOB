#!/usr/bin/env bash
# Make the BOB gate ENFORCING (not advisory) by requiring its CI check before merge.
# This is the one step BOB can't do for you in code — it's a GitHub admin setting.
#
# Prereqs: gh CLI installed and authenticated (`gh auth login`) with admin on the repo.
# Usage:   ./enable-branch-protection.sh <owner/repo> <branch> <required-check-name>
# Example: ./enable-branch-protection.sh salamisemma-dev/Salamis main bob-governance
set -euo pipefail

REPO="${1:?owner/repo}"; BRANCH="${2:-main}"; CHECK="${3:-bob-governance}"

gh api -X PUT "repos/${REPO}/branches/${BRANCH}/protection" \
  -H "Accept: application/vnd.github+json" \
  -f "required_status_checks[strict]=true" \
  -f "required_status_checks[contexts][]=${CHECK}" \
  -F "enforce_admins=true" \
  -F "required_pull_request_reviews[required_approving_review_count]=1" \
  -F "restrictions=null"

echo "Branch protection on ${REPO}@${BRANCH}: '${CHECK}' is now a required check."
echo "A red BOB gate now blocks merge. That closes the last anti-vibe gap."
