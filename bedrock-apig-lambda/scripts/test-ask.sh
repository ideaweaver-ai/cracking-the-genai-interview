#!/usr/bin/env bash
# Smoke-test the deployed API Gateway → Lambda → Bedrock Mantle endpoint.
#
# Usage:
#   export API_URL="https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/ask"
#   ./scripts/test-ask.sh
#   ./scripts/test-ask.sh "What is Amazon Bedrock Mantle?"

set -euo pipefail

if [[ -z "${API_URL:-}" ]]; then
  echo "Set API_URL to your API Gateway invoke URL, e.g.:"
  echo '  export API_URL="https://xxxx.execute-api.us-east-1.amazonaws.com/dev/ask"'
  exit 1
fi

QUESTION="${1:-What is Amazon Bedrock Mantle?}"

curl -sS -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg q "$QUESTION" '{question: $q}')" \
  | jq .
