# Shared settings and helpers for the vLLM scripts. Source, don't execute.

CLUSTER_NAME="${CLUSTER_NAME:-vllm-cluster}"
REGION="${REGION:-us-west-2}"
NAMESPACE="${NAMESPACE:-vllm}"

MODEL_ID="${MODEL_ID:-andresnowak/Qwen3-0.6B-instruction-finetuned}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-qwen3-0.6b}"
# The model was fine-tuned with a 2048-token limit.
MAX_MODEL_LEN="${MAX_MODEL_LEN:-2048}"

VLLM_VERSION="${VLLM_VERSION:-v0.30.0}"
VLLM_GPU_IMAGE="${VLLM_GPU_IMAGE:-vllm/vllm-openai:$VLLM_VERSION}"
VLLM_CPU_IMAGE="${VLLM_CPU_IMAGE:-vllm/vllm-openai-cpu:$VLLM_VERSION-x86_64}"

APP_NAME="${APP_NAME:-vllm-qwen3}"
SERVICE_PORT="${SERVICE_PORT:-8000}"
# Written by 01-install-vllm.sh, read by the later scripts.
INSTALL_CONFIGMAP="vllm-install"

log()  { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }
warn() { log "WARN: $*"; }
die()  { log "ERROR: $*"; exit 1; }

# Prints "gpu" if any Ready node advertises nvidia.com/gpu, else "cpu".
detect_mode() {
  local gpus
  gpus="$(kubectl get nodes -o jsonpath='{range .items[*]}{.status.allocatable.nvidia\.com/gpu}{"\n"}{end}' \
    | awk '$1 > 0 { n += $1 } END { print n + 0 }')"
  if [[ "$gpus" -gt 0 ]]; then echo gpu; else echo cpu; fi
}

# Reads a key from the install ConfigMap.
install_config() {
  kubectl get configmap "$INSTALL_CONFIGMAP" -n "$NAMESPACE" -o "jsonpath={.data.$1}" 2>/dev/null
}
