#!/usr/bin/env bash
# Install vLLM on the cluster: pick GPU or CPU mode from the nodes, pull the
# matching vLLM image onto every target node, verify it imports, and record the
# result in the vllm-install ConfigMap for 02-run-model.sh.
#
# Env overrides: MODE=gpu|cpu, VLLM_VERSION, VLLM_GPU_IMAGE, VLLM_CPU_IMAGE,
# PULL_TIMEOUT (default 20m).
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

PULL_TIMEOUT="${PULL_TIMEOUT:-20m}"
PREPULL_NAME="vllm-prepull"

kubectl get --raw /readyz >/dev/null 2>&1 \
  || die "cannot reach the cluster; run scripts/00-check-prereqs.sh first"

MODE="${MODE:-$(detect_mode)}"
case "$MODE" in
  gpu) IMAGE="$VLLM_GPU_IMAGE"; NODE_LABEL="nvidia-t4" ;;
  cpu) IMAGE="$VLLM_CPU_IMAGE"; NODE_LABEL="none" ;;
  *)   die "MODE must be gpu or cpu, got '$MODE'" ;;
esac

# GPU instances without allocatable GPUs mean the NVIDIA device plugin is missing.
if [[ "$MODE" == cpu ]] && kubectl get nodes -l accelerator=nvidia-t4 --no-headers 2>/dev/null | grep -q .; then
  die "GPU nodes exist but expose no nvidia.com/gpu; check the nvidia-device-plugin DaemonSet in kube-system"
fi

TARGET_NODES="$(kubectl get nodes -l "accelerator=$NODE_LABEL" --no-headers 2>/dev/null | wc -l | tr -d ' ')"
[[ "$TARGET_NODES" -gt 0 ]] || die "no nodes labelled accelerator=$NODE_LABEL"
log "mode: $MODE, image: $IMAGE, target nodes: $TARGET_NODES"

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f - >/dev/null
log "namespace $NAMESPACE ready"

# The init container pulls the image and proves vLLM imports; pause keeps the
# pod alive so rollout status reflects every node.
log "pulling $IMAGE onto $TARGET_NODES node(s); this can take several minutes"
kubectl apply -f - >/dev/null <<EOF
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: $PREPULL_NAME
  namespace: $NAMESPACE
  labels:
    app: $PREPULL_NAME
spec:
  selector:
    matchLabels:
      app: $PREPULL_NAME
  template:
    metadata:
      labels:
        app: $PREPULL_NAME
    spec:
      nodeSelector:
        accelerator: $NODE_LABEL
      tolerations:
        - operator: Exists
      initContainers:
        - name: verify-vllm
          image: $IMAGE
          imagePullPolicy: IfNotPresent
          command: ["python3", "-c", "import vllm; print(vllm.__version__)"]
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
      containers:
        - name: pause
          image: registry.k8s.io/pause:3.10
          resources:
            requests:
              cpu: 10m
              memory: 16Mi
EOF

if ! kubectl rollout status daemonset/"$PREPULL_NAME" -n "$NAMESPACE" --timeout="$PULL_TIMEOUT"; then
  kubectl get pods -n "$NAMESPACE" -l app="$PREPULL_NAME" -o wide >&2
  die "image pull or vLLM import did not finish within $PULL_TIMEOUT"
fi

VERSIONS="$(for pod in $(kubectl get pods -n "$NAMESPACE" -l app="$PREPULL_NAME" -o name); do
  kubectl logs -n "$NAMESPACE" "$pod" -c verify-vllm | tail -1
done | sort -u)"
[[ -n "$VERSIONS" ]] || die "could not read the vLLM version from the pre-pull pods"
[[ "$(wc -l <<<"$VERSIONS" | tr -d ' ')" -eq 1 ]] || die "nodes report different vLLM versions: $VERSIONS"
log "vLLM $VERSIONS imports successfully on all $TARGET_NODES node(s)"

# The image stays cached on the nodes after the DaemonSet is gone.
kubectl delete daemonset "$PREPULL_NAME" -n "$NAMESPACE" --wait=false >/dev/null

kubectl create configmap "$INSTALL_CONFIGMAP" -n "$NAMESPACE" \
  --from-literal=mode="$MODE" \
  --from-literal=image="$IMAGE" \
  --from-literal=node_label="$NODE_LABEL" \
  --from-literal=vllm_version="$VERSIONS" \
  --from-literal=installed_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null

log "vLLM installed; next run scripts/02-run-model.sh"
