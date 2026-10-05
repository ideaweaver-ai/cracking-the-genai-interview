#!/usr/bin/env bash
# Delete the vLLM deployment and the EKS cluster, including its node groups,
# VPC, NAT gateway and CloudFormation stacks.
#
# Usage: scripts/delete-cluster.sh [--yes] [--dry-run]
#   --yes      skip the confirmation prompt
#   --dry-run  list what would be deleted without deleting anything
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

ASSUME_YES=false
DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --yes)     ASSUME_YES=true ;;
    --dry-run) DRY_RUN=true ;;
    -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
    *)         die "unknown argument: $arg" ;;
  esac
done

for bin in aws eksctl kubectl; do
  command -v "$bin" >/dev/null || die "$bin is not installed; run scripts/00-check-prereqs.sh"
done

cluster_stacks() {
  aws cloudformation list-stacks --region "$REGION" \
    --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE ROLLBACK_COMPLETE DELETE_FAILED \
    --query "StackSummaries[?starts_with(StackName, 'eksctl-$CLUSTER_NAME-')].StackName" \
    --output text
}

if ! aws eks describe-cluster --region "$REGION" --name "$CLUSTER_NAME" >/dev/null 2>&1; then
  stacks="$(cluster_stacks)"
  [[ -z "$stacks" ]] && { log "cluster $CLUSTER_NAME does not exist in $REGION; nothing to delete"; exit 0; }
  warn "cluster $CLUSTER_NAME is gone but these stacks remain: $stacks"
  $DRY_RUN && exit 0
  for stack in $stacks; do
    log "deleting leftover stack $stack"
    aws cloudformation delete-stack --region "$REGION" --stack-name "$stack"
  done
  exit 0
fi

nodegroups="$(aws eks list-nodegroups --region "$REGION" --cluster-name "$CLUSTER_NAME" \
  --query nodegroups --output text)"
log "cluster:     $CLUSTER_NAME ($REGION)"
log "node groups: ${nodegroups:-none}"
log "stacks:      $(cluster_stacks | tr '\t' ' ')"

if $DRY_RUN; then
  log "dry run; nothing deleted"
  exit 0
fi

if ! $ASSUME_YES; then
  printf 'This permanently deletes cluster %s and everything running on it.\nType the cluster name to confirm: ' "$CLUSTER_NAME" >&2
  read -r answer
  [[ "$answer" == "$CLUSTER_NAME" ]] || die "confirmation did not match; aborting"
fi

aws eks update-kubeconfig --region "$REGION" --name "$CLUSTER_NAME" >/dev/null
# Deleting workloads first lets any cloud resources they own (e.g. load
# balancers from LoadBalancer Services) be released before the VPC goes away.
if kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
  log "deleting namespace $NAMESPACE"
  kubectl delete namespace "$NAMESPACE" --timeout=5m
fi

log "deleting cluster $CLUSTER_NAME (10-15 minutes)"
eksctl delete cluster --region "$REGION" --name "$CLUSTER_NAME" --wait

leftover="$(cluster_stacks)"
if [[ -n "$leftover" ]]; then
  warn "these CloudFormation stacks still exist; check them in the console: $leftover"
  exit 1
fi

rm -rf "$(dirname "$0")/../eks/generated"
log "cluster $CLUSTER_NAME deleted"
