#!/usr/bin/env bash
# Smoke-test the deployed model through a port-forward to its Service.
#
# Env overrides: LOCAL_PORT (default 18000), REQUEST_TIMEOUT seconds (default 180).
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

LOCAL_PORT="${LOCAL_PORT:-18000}"
REQUEST_TIMEOUT="${REQUEST_TIMEOUT:-180}"
BASE_URL="http://127.0.0.1:$LOCAL_PORT"

command -v jq >/dev/null || die "jq is required; run scripts/00-check-prereqs.sh"

PASSED=0
FAILED=0
pass() { log "PASS: $*"; PASSED=$((PASSED + 1)); }
fail() { log "FAIL: $*"; FAILED=$((FAILED + 1)); }

ready="$(kubectl get deployment "$APP_NAME" -n "$NAMESPACE" -o jsonpath='{.status.readyReplicas}' 2>/dev/null || true)"
[[ "${ready:-0}" -gt 0 ]] || die "deployment $APP_NAME has no ready replicas; run scripts/02-run-model.sh"
pass "deployment $APP_NAME has $ready ready replica(s)"

kubectl port-forward -n "$NAMESPACE" "svc/$APP_NAME" "$LOCAL_PORT:$SERVICE_PORT" >/dev/null 2>&1 &
PF_PID=$!
trap 'kill $PF_PID 2>/dev/null || true' EXIT
for _ in $(seq 1 20); do
  curl -s -o /dev/null "$BASE_URL/health" && break
  sleep 0.5
done

# Usage: request METHOD PATH [JSON_BODY]; sets HTTP_CODE, BODY and ELAPSED.
request() {
  local out args=(-s --max-time "$REQUEST_TIMEOUT" -X "$1" "$BASE_URL$2"
    -H 'Content-Type: application/json' -w '\n%{http_code} %{time_total}')
  [[ $# -ge 3 ]] && args+=(-d "$3")
  out="$(curl "${args[@]}")" || { HTTP_CODE=000; BODY=""; ELAPSED=0; return; }
  BODY="$(sed '$d' <<<"$out")"
  read -r HTTP_CODE ELAPSED <<<"$(tail -1 <<<"$out")"
}

# Prints "<tokens> tokens in <s>s (<tok/s> tok/s)" from a response with usage.
throughput() {
  jq -r --arg t "$ELAPSED" \
    '.usage.completion_tokens as $n | "\($n) tokens in \($t)s (\(($n / ($t | tonumber)) * 10 | floor / 10) tok/s)"' <<<"$BODY"
}

# --- health -------------------------------------------------------------------
request GET /health
[[ "$HTTP_CODE" == 200 ]] && pass "/health returned 200" || fail "/health returned $HTTP_CODE"

# --- model list ---------------------------------------------------------------
request GET /v1/models
if [[ "$HTTP_CODE" == 200 ]] && jq -e --arg m "$SERVED_MODEL_NAME" '.data[] | select(.id == $m)' <<<"$BODY" >/dev/null; then
  pass "/v1/models lists $SERVED_MODEL_NAME (max_model_len $(jq -r '.data[0].max_model_len' <<<"$BODY"))"
else
  fail "/v1/models does not list $SERVED_MODEL_NAME (HTTP $HTTP_CODE): $BODY"
fi

# --- completion ---------------------------------------------------------------
request POST /v1/completions "$(jq -nc --arg m "$SERVED_MODEL_NAME" '{
  model: $m, prompt: "Question: What is the capital of France?\nAnswer:",
  max_tokens: 32, temperature: 0 }')"
text="$(jq -r '.choices[0].text // empty' <<<"$BODY" 2>/dev/null || true)"
if [[ "$HTTP_CODE" == 200 && -n "${text// }" ]]; then
  pass "/v1/completions: $(throughput)"
  log "  answer: $(tr '\n' ' ' <<<"$text" | cut -c1-120)"
  grep -qi paris <<<"$text" || log "  note: answer doesn't mention Paris; check output quality"
else
  fail "/v1/completions (HTTP $HTTP_CODE): $BODY"
fi

# --- chat completion ----------------------------------------------------------
request POST /v1/chat/completions "$(jq -nc --arg m "$SERVED_MODEL_NAME" '{
  model: $m, messages: [{ role: "user", content: "Name three primary colors." }],
  max_tokens: 48, temperature: 0 }')"
content="$(jq -r '.choices[0].message.content // empty' <<<"$BODY" 2>/dev/null || true)"
if [[ "$HTTP_CODE" == 200 && -n "${content// }" ]]; then
  pass "/v1/chat/completions: $(throughput)"
  log "  answer: $(tr '\n' ' ' <<<"$content" | cut -c1-120)"
else
  fail "/v1/chat/completions (HTTP $HTTP_CODE): $BODY"
fi

# --- streaming ----------------------------------------------------------------
stream="$(curl -sN --max-time "$REQUEST_TIMEOUT" "$BASE_URL/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg m "$SERVED_MODEL_NAME" '{
    model: $m, messages: [{ role: "user", content: "Count from 1 to 5." }],
    max_tokens: 24, temperature: 0, stream: true }')" || true)"
chunks="$(grep -c '^data: {' <<<"$stream" || true)"
if [[ "$chunks" -gt 1 ]] && grep -q '^data: \[DONE\]' <<<"$stream"; then
  pass "streaming returned $chunks chunks and [DONE]"
else
  fail "streaming returned $chunks chunks; output: $(head -c 300 <<<"$stream")"
fi

# --- error handling -----------------------------------------------------------
request POST /v1/completions '{"model": "does-not-exist", "prompt": "hi", "max_tokens": 1}'
[[ "$HTTP_CODE" == 404 ]] && pass "unknown model rejected with 404" \
  || fail "unknown model returned HTTP $HTTP_CODE, expected 404"

echo
log "$PASSED passed, $FAILED failed"
[[ "$FAILED" -eq 0 ]]
