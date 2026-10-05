#!/usr/bin/env bash
# Check the tools and access the vLLM scripts need, installing missing tools.
#
# Usage: scripts/00-check-prereqs.sh [--check-only] [--skip-cluster]
#   --check-only    report missing tools without installing them
#   --skip-cluster  skip the EKS cluster checks (e.g. before the cluster exists)
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"

CHECK_ONLY=false
SKIP_CLUSTER=false
for arg in "$@"; do
  case "$arg" in
    --check-only)   CHECK_ONLY=true ;;
    --skip-cluster) SKIP_CLUSTER=true ;;
    -h|--help)      sed -n '2,7p' "$0"; exit 0 ;;
    *)              die "unknown argument: $arg" ;;
  esac
done

# Linux installs go here; must be on PATH.
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
OS="$(uname -s)"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)  ARCH_K8S=amd64; ARCH_AWS=x86_64 ;;
  arm64|aarch64) ARCH_K8S=arm64; ARCH_AWS=aarch64 ;;
  *)             die "unsupported architecture: $ARCH" ;;
esac

FAILURES=0
pass() { log "PASS: $*"; }
fail() { log "FAIL: $*"; FAILURES=$((FAILURES + 1)); }

sudo_if_needed() {
  if [[ -w "$INSTALL_DIR" ]]; then "$@"; else sudo "$@"; fi
}

install_linux_binary() {
  local name="$1" url="$2" tmp
  tmp="$(mktemp -d)"
  curl -fsSL "$url" -o "$tmp/$name"
  chmod +x "$tmp/$name"
  sudo_if_needed mv "$tmp/$name" "$INSTALL_DIR/$name"
  rm -rf "$tmp"
}

install_tool() {
  local tool="$1" tmp
  if [[ "$OS" == Darwin ]]; then
    command -v brew >/dev/null || die "Homebrew is required to install $tool on macOS: https://brew.sh"
    case "$tool" in
      aws) brew install awscli ;;
      *)   brew install "$tool" ;;
    esac
    return
  fi

  [[ "$OS" == Linux ]] || die "automatic install of $tool is not supported on $OS"
  command -v curl >/dev/null || die "curl is required to install $tool"
  case "$tool" in
    aws)
      tmp="$(mktemp -d)"
      curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$ARCH_AWS.zip" -o "$tmp/awscli.zip"
      (cd "$tmp" && unzip -q awscli.zip && sudo ./aws/install --update)
      rm -rf "$tmp"
      ;;
    kubectl)
      install_linux_binary kubectl \
        "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/$ARCH_K8S/kubectl"
      ;;
    eksctl)
      tmp="$(mktemp -d)"
      curl -fsSL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_$ARCH_K8S.tar.gz" \
        | tar -xz -C "$tmp"
      sudo_if_needed mv "$tmp/eksctl" "$INSTALL_DIR/eksctl"
      rm -rf "$tmp"
      ;;
    jq)
      install_linux_binary jq \
        "https://github.com/jqlang/jq/releases/latest/download/jq-linux-$ARCH_K8S"
      ;;
    *)
      die "don't know how to install $tool"
      ;;
  esac
}

tool_version() {
  case "$1" in
    aws)     aws --version 2>&1 | awk '{ print $1 }' ;;
    kubectl) kubectl version --client -o json 2>/dev/null | sed -n 's/.*"gitVersion": "\(.*\)".*/\1/p' ;;
    eksctl)  eksctl version ;;
    jq)      jq --version ;;
    curl)    curl --version | awk 'NR == 1 { print $1 " " $2 }' ;;
  esac
}

# --- tools --------------------------------------------------------------------
log "checking tools"
# curl can't reliably self-install, so it's check-only.
command -v curl >/dev/null && pass "curl ($(tool_version curl))" || fail "curl is not installed"

for tool in aws kubectl eksctl jq; do
  if command -v "$tool" >/dev/null; then
    pass "$tool ($(tool_version "$tool"))"
  elif $CHECK_ONLY; then
    fail "$tool is not installed"
  else
    log "installing $tool"
    if install_tool "$tool" && command -v "$tool" >/dev/null; then
      pass "$tool installed ($(tool_version "$tool"))"
    else
      fail "could not install $tool"
    fi
  fi
done

# --- AWS access ---------------------------------------------------------------
if command -v aws >/dev/null; then
  log "checking AWS credentials"
  if identity="$(aws sts get-caller-identity --query Arn --output text 2>/dev/null)"; then
    pass "AWS credentials ($identity)"
  else
    fail "AWS credentials are missing or invalid; run 'aws configure' or set AWS_PROFILE"
  fi
fi

# --- cluster access -----------------------------------------------------------
if ! $SKIP_CLUSTER && command -v aws >/dev/null && command -v kubectl >/dev/null; then
  log "checking cluster $CLUSTER_NAME in $REGION"
  status="$(aws eks describe-cluster --region "$REGION" --name "$CLUSTER_NAME" \
    --query cluster.status --output text 2>/dev/null || true)"
  if [[ "$status" != ACTIVE ]]; then
    fail "cluster $CLUSTER_NAME is ${status:-not found}; create it with scripts/create-cluster.sh"
  else
    pass "cluster $CLUSTER_NAME is ACTIVE"
    aws eks update-kubeconfig --region "$REGION" --name "$CLUSTER_NAME" >/dev/null

    if kubectl get --raw /readyz >/dev/null 2>&1; then
      pass "kubectl can reach the API server"
    else
      fail "kubectl cannot reach the API server"
    fi

    ready="$(kubectl get nodes --no-headers 2>/dev/null | awk '$2 == "Ready"' | wc -l | tr -d ' ')"
    if [[ "$ready" -gt 0 ]]; then
      pass "$ready node(s) Ready"
    else
      fail "no Ready nodes; check the node group"
    fi

    mode="$(detect_mode)"
    if [[ "$mode" == gpu ]]; then
      pass "GPU nodes detected; vLLM will run in GPU mode"
    else
      # vLLM's CPU backend needs ~4.5 GiB for this model and a 1 GiB KV cache,
      # plus headroom for system pods.
      max_mem_kib="$(kubectl get nodes -o jsonpath='{range .items[*]}{.status.allocatable.memory}{"\n"}{end}' \
        | sed 's/Ki$//' | sort -n | tail -1)"
      if [[ "${max_mem_kib:-0}" -lt 5767168 ]]; then
        fail "no GPU nodes and the largest node has under 5.5 GiB allocatable memory (t3.large or bigger needed)"
      else
        warn "no GPU nodes; vLLM will run in CPU mode (slow, for testing only)"
      fi
    fi
  fi
fi

echo
if [[ "$FAILURES" -gt 0 ]]; then
  die "$FAILURES prerequisite check(s) failed"
fi
log "all prerequisites satisfied"
