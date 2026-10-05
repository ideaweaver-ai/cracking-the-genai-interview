#!/usr/bin/env bash
# Create the vLLM EKS cluster on g4dn.xlarge GPU nodes, falling back to
# t3.large CPU nodes when g4dn.xlarge can't be launched (not offered in the
# region, insufficient vCPU quota, or node group creation fails).
set -euo pipefail

CLUSTER_NAME="${CLUSTER_NAME:-vllm-cluster}"
REGION="${REGION:-us-west-2}"
AZS="${AZS:-us-west-2a us-west-2b us-west-2c}"
NODES="${NODES:-2}"
PRIMARY_TYPE="${PRIMARY_TYPE:-g4dn.xlarge}"
# t3.medium (4 GiB) is too small for vLLM's CPU backend with this model.
FALLBACK_TYPE="${FALLBACK_TYPE:-t3.large}"
# Set FORCE_TYPE to skip detection, e.g. FORCE_TYPE=t3.large.
FORCE_TYPE="${FORCE_TYPE:-}"
# Set DRY_RUN=1 to only pick the instance type and render the config.

# EC2 vCPU quota codes.
GPU_QUOTA_CODE="L-DB2E81BA"      # Running On-Demand G and VT instances
STANDARD_QUOTA_CODE="L-1216C47A" # Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$ROOT_DIR/eks/cluster.yaml.tmpl"
GENERATED_DIR="$ROOT_DIR/eks/generated"

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }

for bin in aws eksctl kubectl; do
  command -v "$bin" >/dev/null || die "$bin is not installed"
done

instance_vcpus() {
  aws ec2 describe-instance-types --region "$REGION" --instance-types "$1" \
    --query 'InstanceTypes[0].VCpuInfo.DefaultVCpus' --output text
}

quota_value() {
  aws service-quotas get-service-quota --region "$REGION" --service-code ec2 \
    --quota-code "$1" --query 'Quota.Value' --output text
}

# Sum of vCPUs of pending/running instances whose type matches the given
# wildcard patterns (e.g. "g*" "vt*").
used_vcpus() {
  aws ec2 describe-instances --region "$REGION" \
    --filters "Name=instance-state-name,Values=pending,running" \
              "Name=instance-type,Values=$(IFS=,; echo "$*")" \
    --query 'Reservations[].Instances[].[CpuOptions.CoreCount,CpuOptions.ThreadsPerCore]' \
    --output text | awk '{ s += $1 * $2 } END { print s + 0 }'
}

offered_in_all_azs() {
  local type="$1" az offered
  offered="$(aws ec2 describe-instance-type-offerings --region "$REGION" \
    --location-type availability-zone \
    --filters "Name=instance-type,Values=$type" \
    --query 'InstanceTypeOfferings[].Location' --output text)"
  for az in $AZS; do
    if ! grep -qw "$az" <<<"$offered"; then
      log "$type is not offered in $az"
      return 1
    fi
  done
}

# Returns 0 if NODES instances of the given type fit in the remaining quota.
quota_allows() {
  local type="$1" quota_code="$2"; shift 2
  local per_node need quota used
  per_node="$(instance_vcpus "$type")"
  need=$(( per_node * NODES ))
  quota="$(quota_value "$quota_code")"
  if [[ $# -gt 0 ]]; then used="$(used_vcpus "$@")"; else used=0; fi
  log "$type: need $need vCPUs, quota $quota, in use $used"
  awk -v q="$quota" -v u="$used" -v n="$need" 'BEGIN { exit !(q - u >= n) }'
}

gpu_available() {
  offered_in_all_azs "$PRIMARY_TYPE" || return 1
  quota_allows "$PRIMARY_TYPE" "$GPU_QUOTA_CODE" "g*" "vt*" || {
    log "insufficient G/VT vCPU quota for $PRIMARY_TYPE"
    return 1
  }
}

fallback_available() {
  offered_in_all_azs "$FALLBACK_TYPE" || return 1
  # Standard-family usage spans many instance families, so only the quota
  # ceiling is checked here.
  quota_allows "$FALLBACK_TYPE" "$STANDARD_QUOTA_CODE" || {
    log "insufficient standard vCPU quota for $FALLBACK_TYPE"
    return 1
  }
}

# Writes the rendered config for an instance type and prints its path.
render_config() {
  local type="$1" ng accel out azs_yaml
  ng="$(nodegroup_name "$type")"
  if [[ "$type" == g* ]]; then accel="nvidia-t4"; else accel="none"; fi
  azs_yaml="$(printf '"%s", ' $AZS)"; azs_yaml="${azs_yaml%, }"
  mkdir -p "$GENERATED_DIR"
  out="$GENERATED_DIR/cluster-$type.yaml"
  sed -e "s|__CLUSTER_NAME__|$CLUSTER_NAME|g" \
      -e "s|__REGION__|$REGION|g" \
      -e "s|__AZS__|$azs_yaml|g" \
      -e "s|__NODEGROUP_NAME__|$ng|g" \
      -e "s|__INSTANCE_TYPE__|$type|g" \
      -e "s|__NODES__|$NODES|g" \
      -e "s|__ACCELERATOR__|$accel|g" \
      "$TEMPLATE" > "$out"
  echo "$out"
}

# e.g. g4dn.xlarge -> gpu-g4dn-xlarge, t3.large -> cpu-t3-large. Including the
# type lets a replacement node group coexist with the old one during a swap.
nodegroup_name() {
  local prefix=cpu
  [[ "$1" == g* ]] && prefix=gpu
  echo "$prefix-${1//./-}"
}

cluster_exists() {
  aws eks describe-cluster --region "$REGION" --name "$CLUSTER_NAME" >/dev/null 2>&1
}

nodegroup_exists() {
  aws eks describe-nodegroup --region "$REGION" --cluster-name "$CLUSTER_NAME" \
    --nodegroup-name "$1" >/dev/null 2>&1
}

create_nodegroup() {
  local type="$1" config ng
  config="$(render_config "$type")"
  ng="$(nodegroup_name "$type")"
  if nodegroup_exists "$ng"; then
    log "node group $ng already exists; skipping"
    return 0
  fi
  log "creating node group $ng ($NODES x $type)"
  eksctl create nodegroup -f "$config" --include "$ng"
}

# --- choose instance type ---------------------------------------------------
if [[ -n "$FORCE_TYPE" ]]; then
  SELECTED="$FORCE_TYPE"
  log "FORCE_TYPE set; using $SELECTED"
elif gpu_available; then
  SELECTED="$PRIMARY_TYPE"
  log "$PRIMARY_TYPE is available"
elif fallback_available; then
  SELECTED="$FALLBACK_TYPE"
  log "falling back to $FALLBACK_TYPE"
else
  die "neither $PRIMARY_TYPE nor $FALLBACK_TYPE can be launched in $REGION"
fi

if [[ -n "${DRY_RUN:-}" ]]; then
  log "DRY_RUN set; rendered $(render_config "$SELECTED") and stopping"
  exit 0
fi

# --- control plane ------------------------------------------------------------
if cluster_exists; then
  log "cluster $CLUSTER_NAME already exists; skipping control plane creation"
  aws eks update-kubeconfig --region "$REGION" --name "$CLUSTER_NAME" >/dev/null
else
  log "creating control plane for $CLUSTER_NAME (15-20 minutes)"
  eksctl create cluster -f "$(render_config "$SELECTED")" --without-nodegroup
fi

# --- nodes --------------------------------------------------------------------
# Quota checks can't detect a capacity shortage, so a failed GPU node group
# still falls back to the CPU type.
if ! create_nodegroup "$SELECTED"; then
  if [[ "$SELECTED" == "$PRIMARY_TYPE" && -z "$FORCE_TYPE" ]]; then
    log "$PRIMARY_TYPE node group failed; cleaning up and falling back to $FALLBACK_TYPE"
    eksctl delete nodegroup --region "$REGION" --cluster "$CLUSTER_NAME" \
      --name "$(nodegroup_name "$PRIMARY_TYPE")" --wait || true
    SELECTED="$FALLBACK_TYPE"
    create_nodegroup "$SELECTED"
  else
    die "node group creation failed for $SELECTED"
  fi
fi

log "cluster ready with $NODES x $SELECTED nodes"
kubectl get nodes -L node.kubernetes.io/instance-type,accelerator
