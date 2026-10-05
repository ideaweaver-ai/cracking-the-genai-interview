#!/usr/bin/env bash
# Deploy the model behind vLLM's OpenAI-compatible server, using the mode and
# image recorded by 01-install-vllm.sh.
#
# Env overrides: MODEL_ID, SERVED_MODEL_NAME, MAX_MODEL_LEN, REPLICAS,
# CPU_KVCACHE_MIB (CPU mode, default 1024), GPU_MEMORY_UTILIZATION (GPU mode,
# default 0.90), ROLLOUT_TIMEOUT (default 20m).
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

ROLLOUT_TIMEOUT="${ROLLOUT_TIMEOUT:-20m}"
CPU_KVCACHE_MIB="${CPU_KVCACHE_MIB:-1024}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.90}"
TEMPLATE_CONFIGMAP="$APP_NAME-chat-template"

# Converts a kubectl-style duration (e.g. 20m, 90s, 1h) to seconds.
timeout_seconds() {
  local n="${1%[smh]}"
  case "$1" in
    *h) echo $(( n * 3600 )) ;;
    *m) echo $(( n * 60 )) ;;
    *)  echo "$n" ;;
  esac
}

MODE="$(install_config mode)"
IMAGE="$(install_config image)"
NODE_LABEL="$(install_config node_label)"
[[ -n "$MODE" && -n "$IMAGE" ]] || die "vLLM is not installed; run scripts/01-install-vllm.sh first"

TARGET_NODES="$(kubectl get nodes -l "accelerator=$NODE_LABEL" --no-headers | wc -l | tr -d ' ')"

# Mode-specific pieces of the pod spec.
if [[ "$MODE" == gpu ]]; then
  REPLICAS="${REPLICAS:-$TARGET_NODES}"
  # T4 GPUs don't support bfloat16.
  EXTRA_ARGS="
            - --dtype=half
            - --gpu-memory-utilization=$GPU_MEMORY_UTILIZATION"
  EXTRA_ENV=""
  RESOURCES="
            requests:
              cpu: \"2\"
              memory: 8Gi
              nvidia.com/gpu: 1
            limits:
              memory: 12Gi
              nvidia.com/gpu: 1"
  SHM_SIZE="1Gi"
else
  REPLICAS="${REPLICAS:-$TARGET_NODES}"
  # Give the pod the node's memory minus headroom for system pods. The API
  # server and engine processes (~2.2 GiB), weights (1.1 GiB) and KV cache must fit.
  NODE_MEM_MIB="$(kubectl get nodes -l "accelerator=$NODE_LABEL" \
    -o jsonpath='{range .items[*]}{.status.allocatable.memory}{"\n"}{end}' \
    | sed 's/Ki$//' | sort -n | head -1 | awk '{ print int($1 / 1024) }')"
  POD_MEM_MIB=$(( NODE_MEM_MIB - 1024 ))
  NEEDED_MIB=$(( 3584 + CPU_KVCACHE_MIB ))
  [[ "$POD_MEM_MIB" -ge "$NEEDED_MIB" ]] \
    || die "CPU nodes leave ${POD_MEM_MIB}Mi for vLLM but it needs ${NEEDED_MIB}Mi; use t3.large or bigger"
  # torch.compile on a 2-vCPU node is slow and memory-hungry; the uni executor
  # keeps the worker inside the engine process instead of spawning another.
  EXTRA_ARGS="
            - --max-num-seqs=4
            - --enforce-eager
            - --distributed-executor-backend=uni
            - --kv-cache-memory-bytes=$(( CPU_KVCACHE_MIB * 1024 * 1024 ))"
  EXTRA_ENV=""
  RESOURCES="
            requests:
              cpu: 1500m
              memory: ${POD_MEM_MIB}Mi
            limits:
              memory: ${POD_MEM_MIB}Mi"
  SHM_SIZE="256Mi"
fi

# The model was fine-tuned on plain-text prompts without a chat template, so
# chat messages are rendered as a simple Question/Answer transcript.
CHAT_TEMPLATE='{%- for m in messages -%}{%- if m["role"] == "system" -%}{{ m["content"] + "\n\n" }}{%- elif m["role"] == "user" -%}{{ "Question: " + m["content"] + "\n" }}{%- elif m["role"] == "assistant" -%}{{ "Answer: " + m["content"] + eos_token + "\n" }}{%- endif -%}{%- endfor -%}{%- if add_generation_prompt -%}{{ "Answer:" }}{%- endif -%}'

kubectl create configmap "$TEMPLATE_CONFIGMAP" -n "$NAMESPACE" \
  --from-literal=chat.jinja="$CHAT_TEMPLATE" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null
TEMPLATE_HASH="$(printf '%s' "$CHAT_TEMPLATE" | cksum | awk '{ print $1 }')"

log "deploying $MODEL_ID as '$SERVED_MODEL_NAME' ($MODE mode, $REPLICAS replica(s), image $IMAGE)"
kubectl apply -f - >/dev/null <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $APP_NAME
  namespace: $NAMESPACE
  labels:
    app: $APP_NAME
spec:
  replicas: $REPLICAS
  progressDeadlineSeconds: $(timeout_seconds "$ROLLOUT_TIMEOUT")
  selector:
    matchLabels:
      app: $APP_NAME
  # Nodes can't fit two replicas, so replace pods one at a time.
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: $APP_NAME
      annotations:
        vllm/chat-template-hash: "$TEMPLATE_HASH"
    spec:
      # Service env vars like VLLM_QWEN3_PORT trip vLLM's unknown-variable warnings.
      enableServiceLinks: false
      nodeSelector:
        accelerator: $NODE_LABEL
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: $APP_NAME
              topologyKey: kubernetes.io/hostname
      containers:
        - name: vllm
          image: $IMAGE
          imagePullPolicy: IfNotPresent
          command: ["vllm", "serve"]
          args:
            - $MODEL_ID
            - --served-model-name=$SERVED_MODEL_NAME
            - --max-model-len=$MAX_MODEL_LEN
            - --chat-template=/templates/chat.jinja
            - --host=0.0.0.0
            - --port=$SERVICE_PORT$EXTRA_ARGS
          env:
            - name: HF_HOME
              value: /cache/huggingface$EXTRA_ENV
          ports:
            - name: http
              containerPort: $SERVICE_PORT
          resources:$RESOURCES
          startupProbe:
            httpGet:
              path: /health
              port: http
            periodSeconds: 10
            failureThreshold: 90
          readinessProbe:
            httpGet:
              path: /health
              port: http
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: http
            periodSeconds: 30
            failureThreshold: 3
          volumeMounts:
            - name: cache
              mountPath: /cache
            - name: chat-template
              mountPath: /templates
            # vLLM's engine processes talk over /dev/shm; the 64 MiB default is too small.
            - name: dshm
              mountPath: /dev/shm
      volumes:
        - name: cache
          emptyDir: {}
        - name: chat-template
          configMap:
            name: $TEMPLATE_CONFIGMAP
        - name: dshm
          emptyDir:
            medium: Memory
            sizeLimit: $SHM_SIZE
---
apiVersion: v1
kind: Service
metadata:
  name: $APP_NAME
  namespace: $NAMESPACE
  labels:
    app: $APP_NAME
spec:
  selector:
    app: $APP_NAME
  ports:
    - name: http
      port: $SERVICE_PORT
      targetPort: http
EOF

log "waiting for the model server to become ready (up to $ROLLOUT_TIMEOUT)"
if ! kubectl rollout status deployment/"$APP_NAME" -n "$NAMESPACE" --timeout="$ROLLOUT_TIMEOUT"; then
  kubectl get pods -n "$NAMESPACE" -l app="$APP_NAME" -o wide >&2
  pod="$(kubectl get pods -n "$NAMESPACE" -l app="$APP_NAME" -o name | head -1)"
  if [[ -n "$pod" ]]; then
    kubectl describe -n "$NAMESPACE" "$pod" | sed -n '/^Events:/,$p' >&2
    kubectl logs -n "$NAMESPACE" "$pod" --tail=40 >&2 || true
  fi
  die "model server did not become ready"
fi

log "model is being served at http://$APP_NAME.$NAMESPACE.svc.cluster.local:$SERVICE_PORT"
log "next run scripts/03-test-model.sh"
