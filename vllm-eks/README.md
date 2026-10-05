# vLLM on Amazon EKS

Deploys [vLLM](https://github.com/vllm-project/vllm) on an Amazon EKS cluster and serves
[`andresnowak/Qwen3-0.6B-instruction-finetuned`](https://huggingface.co/andresnowak/Qwen3-0.6B-instruction-finetuned)
through vLLM's OpenAI-compatible API.

The cluster runs on **g4dn.xlarge** GPU nodes (NVIDIA T4) when your account can launch them, and
falls back to **t3.large** CPU nodes when it can't. The later scripts detect which kind of node
the cluster has and configure vLLM to match.

## Layout

```
eks/cluster.yaml.tmpl        eksctl ClusterConfig template (rendered into eks/generated/)
scripts/
  lib/common.sh              shared settings: cluster, region, model, vLLM version
  00-check-prereqs.sh        check and install tools, verify AWS and cluster access
  create-cluster.sh          create the EKS cluster (GPU nodes, CPU fallback)
  01-install-vllm.sh         pull and verify the vLLM image on the nodes
  02-run-model.sh            deploy the model server (Deployment + Service)
  03-test-model.sh           test the running model server
  delete-cluster.sh          delete the deployment and the cluster
```

## Step-by-step setup

You need an AWS account with credentials configured (`aws configure`) and permission to create
EKS clusters, VPCs, IAM roles and EC2 instances.

The steps below take about 30–40 minutes in total, most of it spent waiting for AWS.

### Step 0: get the code

```bash
git clone git@github.com:ideaweaver-ai/cracking-the-genai-interview.git
cd cracking-the-genai-interview/vllm-eks
```

Run every command below from this `vllm-eks/` directory.

### Step 1: check prerequisites (about 1 minute)

```bash
./scripts/00-check-prereqs.sh --skip-cluster
```

This installs any missing tools and checks your AWS credentials. Use `--skip-cluster` because
the cluster doesn't exist yet. Every line should say `PASS`.

### Step 2: create the cluster (about 20 minutes)

Preview which instance type the script will choose:

```bash
DRY_RUN=1 ./scripts/create-cluster.sh
```

If it logs `g4dn.xlarge is available`, you'll get GPU nodes. If it logs
`falling back to t3.large`, your G-instance quota is too low and you'll get CPU nodes; see
[Moving from CPU to GPU nodes](#moving-from-cpu-to-gpu-nodes) to raise it. Then create the
cluster:

```bash
./scripts/create-cluster.sh
```

It ends by listing 2 nodes with their instance type and accelerator (`nvidia-t4` or `none`).
On GPU nodes, confirm each node exposes a GPU:

```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,GPU:.status.allocatable.'nvidia\.com/gpu'
```

Each node should show `1`. `<none>` means the NVIDIA device plugin isn't running.

### Step 3: full prerequisites check (a few seconds)

```bash
./scripts/00-check-prereqs.sh
```

Look for `GPU nodes detected; vLLM will run in GPU mode`. On CPU nodes it warns that vLLM will
run in CPU mode instead.

### Step 4: install vLLM (about 2–10 minutes)

```bash
./scripts/01-install-vllm.sh
```

It logs the mode and image, for example `mode: gpu, image: vllm/vllm-openai:v0.30.0`. The GPU
image is about 10 GB, so it takes several minutes to pull; the CPU image takes about 2 minutes.
It finishes with `vLLM 0.30.0 imports successfully on all 2 node(s)`.

### Step 5: run the model (about 2–5 minutes)

```bash
./scripts/02-run-model.sh
```

It deploys one replica per node. While it waits, you can watch progress from a second terminal:

```bash
kubectl get pods -n vllm -w
kubectl logs -n vllm deploy/vllm-qwen3 -f
```

### Step 6: test (under a minute)

```bash
./scripts/03-test-model.sh
```

You should see `7 passed, 0 failed`. To try your own prompts, port-forward the Service and use
the examples in [Using the API](#using-the-api):

```bash
kubectl port-forward -n vllm svc/vllm-qwen3 8000:8000
```

### Step 7: clean up

```bash
./scripts/delete-cluster.sh --dry-run    # see what will be deleted
./scripts/delete-cluster.sh              # type the cluster name to confirm
```

The cluster costs money for as long as it runs (see [Performance and cost](#performance-and-cost)),
so delete it when you're done.

### If a step fails

- **The GPU node group fails** because AWS is out of g4dn capacity: `create-cluster.sh` falls
  back to t3.large on its own, and the remaining steps adapt.
- **You want CPU nodes anyway:** run `FORCE_TYPE=t3.large ./scripts/create-cluster.sh`.
- **A pod crash-loops:** `kubectl logs -n vllm deploy/vllm-qwen3 --previous` shows why it
  died. See also [Troubleshooting](#troubleshooting).

## Scripts

### `00-check-prereqs.sh`

Checks for `aws`, `kubectl`, `eksctl`, `jq` and `curl`, and installs any that are missing:
with Homebrew on macOS, or from the official release binaries on Linux. It then checks that
your AWS credentials work and, unless you pass `--skip-cluster`, that the cluster is `ACTIVE`,
reachable and has `Ready` nodes with enough memory. Pass `--check-only` to report problems
without installing anything. The script exits non-zero if any check fails.

### `create-cluster.sh`

Creates the EKS cluster (Kubernetes 1.35, three availability zones, nodes in private subnets)
and a managed node group of 2 nodes. It picks the instance type like this:

1. Use **g4dn.xlarge** if it's offered in every availability zone and your remaining
   "Running On-Demand G and VT instances" vCPU quota covers all the nodes (4 vCPUs each).
2. Otherwise use **t3.large**, if your standard-instance quota allows it.
3. If the GPU node group passes the checks but still fails to create (for example, AWS is out of
   g4dn capacity), delete it and create the t3.large node group instead.

Node groups are named after their instance type (`gpu-g4dn-xlarge`, `cpu-t3-large`), so a
replacement node group can run alongside the old one while you switch. Re-running the script is
safe: it skips a control plane or node group that already exists.

| Variable | Default | Purpose |
|---|---|---|
| `CLUSTER_NAME` | `vllm-cluster` | Cluster name |
| `REGION` | `us-west-2` | AWS region |
| `AZS` | `us-west-2a us-west-2b us-west-2c` | Availability zones |
| `NODES` | `2` | Number of nodes |
| `PRIMARY_TYPE` | `g4dn.xlarge` | Preferred (GPU) instance type |
| `FALLBACK_TYPE` | `t3.large` | Fallback (CPU) instance type |
| `FORCE_TYPE` | unset | Skip detection and use this instance type |
| `DRY_RUN` | unset | Set to `1` to only choose the type and render the config |

### `01-install-vllm.sh`

Sets GPU mode if any node exposes an `nvidia.com/gpu` resource, otherwise CPU mode, and picks
the matching image:

- GPU mode: `vllm/vllm-openai:<version>`
- CPU mode: `vllm/vllm-openai-cpu:<version>-x86_64`

It creates the `vllm` namespace, then runs a short-lived DaemonSet that pulls the image onto
every target node and runs `import vllm` there to prove it works. The mode, image and vLLM
version are saved in the `vllm-install` ConfigMap, which `02-run-model.sh` reads. Override the
detection with `MODE=gpu|cpu` and the version with `VLLM_VERSION` (default `v0.30.0`).

### `02-run-model.sh`

Deploys the model as the `vllm-qwen3` Deployment with a ClusterIP Service on port 8000. The model
is served under the name **`qwen3-0.6b`**, with one replica per node by default.

| | GPU mode | CPU mode |
|---|---|---|
| Precision | float16 (T4 GPUs don't support bfloat16) | bfloat16 |
| Resources | 1 GPU, 8-12 GiB memory | node memory minus 1 GiB of headroom |
| KV cache | whatever fits in 90% of GPU memory after the weights | 1 GiB |
| Other settings | | no `torch.compile`, single worker process, at most 4 concurrent sequences |

| Variable | Default | Purpose |
|---|---|---|
| `MODEL_ID` | `andresnowak/Qwen3-0.6B-instruction-finetuned` | Hugging Face model |
| `SERVED_MODEL_NAME` | `qwen3-0.6b` | Model name used in API requests |
| `MAX_MODEL_LEN` | `2048` | Context length (the length the model was fine-tuned with) |
| `REPLICAS` | number of nodes | Server replicas (one per node at most) |
| `CPU_KVCACHE_MIB` | `1024` | CPU mode KV cache size |
| `GPU_MEMORY_UTILIZATION` | `0.90` | GPU mode share of GPU memory vLLM may use |
| `ROLLOUT_TIMEOUT` | `20m` | How long to wait for the server to become ready |

### `03-test-model.sh`

Port-forwards to the Service and checks:

- `/health` returns 200
- `/v1/models` lists the model
- a completion and a chat completion each return text (the script prints the answers and the
  tokens per second)
- streaming returns chunks ending in `[DONE]`
- an unknown model name is rejected with 404

The script exits non-zero if any check fails. If requests time out, raise `REQUEST_TIMEOUT`
(seconds, default 180). If local port 18000 is in use, change `LOCAL_PORT`.

### `delete-cluster.sh`

Deletes the `vllm` namespace, then the cluster with its node groups, VPC, NAT gateway and
CloudFormation stacks, and finally checks that no stacks are left. It asks you to type the
cluster name to confirm. Pass `--yes` to skip the prompt (for automation), or `--dry-run` to
list what would be deleted.

## Using the API

The Service is internal to the cluster. To call it from your machine, port-forward it:

```bash
kubectl port-forward -n vllm svc/vllm-qwen3 8000:8000
```

```bash
curl http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-0.6b",
    "messages": [{"role": "user", "content": "Name three primary colors."}],
    "max_tokens": 64,
    "temperature": 0,
    "stop": ["\nQuestion:"]
  }'
```

Any OpenAI client works with `base_url="http://localhost:8000/v1"` and any API key.

From inside the cluster, use `http://vllm-qwen3.vllm.svc.cluster.local:8000`.

### Prompt format

The model was fine-tuned on plain-text prompts and doesn't include a chat template. The deployment
supplies one that turns chat messages into a transcript like this:

```
Question: Name three primary colors.
Answer:
```

After answering, the model tends to write another `Question: ... Answer: ...` pair. Pass
`"stop": ["\nQuestion:"]` to end its output after the first answer.

## Moving from CPU to GPU nodes

If the cluster fell back to CPU nodes because of the G-instance quota, request an increase to at
least 8 vCPUs (2 nodes × 4 vCPUs) in the Service Quotas console, or with:

```bash
aws service-quotas request-service-quota-increase --region us-west-2 \
  --service-code ec2 --quota-code L-DB2E81BA --desired-value 8
```

Once it's approved, add the GPU node group, remove the CPU one and redeploy:

```bash
FORCE_TYPE=g4dn.xlarge ./scripts/create-cluster.sh
eksctl delete nodegroup --cluster vllm-cluster --region us-west-2 --name cpu-t3-large
./scripts/01-install-vllm.sh && ./scripts/02-run-model.sh && ./scripts/03-test-model.sh
```

## Performance and cost

Measured on 2 × t3.large nodes in CPU mode: about **4.5 tokens per second** per request, and each
replica uses about 5.4 GiB of memory. The first request after startup is slower (about 35
seconds) while the server warms up. A T4 GPU should be much faster.

Approximate on-demand prices in us-west-2:

| Setup | Cost per hour |
|---|---|
| EKS control plane + NAT gateway | ~$0.15 |
| 2 × t3.large | ~$0.17 |
| 2 × g4dn.xlarge | ~$1.05 |

## Troubleshooting

- **The pod is `OOMKilled`.** The node doesn't have enough memory. vLLM's CPU backend needs
  about 4.5 GiB for this model, so t3.medium (about 3.2 GiB usable) can't run it. Use t3.large
  or larger. `00-check-prereqs.sh` and `02-run-model.sh` both refuse to continue on nodes that
  are too small.
- **The log says `check_shm_free_space` or `Engine core initialization failed`.** `/dev/shm` is too
  small; vLLM's engine processes communicate through it. The Deployment mounts a larger
  in-memory `/dev/shm`, so this only happens if that mount was removed.
- **Chat requests fail with a chat-template error.** The model ships without a chat template.
  Make sure the `vllm-qwen3-chat-template` ConfigMap exists and is mounted; re-running
  `02-run-model.sh` restores it.
- **`create-cluster.sh` always falls back to CPU.** Check your G-instance quota:
  `aws service-quotas get-service-quota --service-code ec2 --quota-code L-DB2E81BA`.
- **You have GPU nodes but `01-install-vllm.sh` reports no GPUs.** The NVIDIA device plugin isn't
  running. Check `kubectl get ds -n kube-system | grep nvidia`.
- **You need server logs.** Run `kubectl logs -n vllm deploy/vllm-qwen3 -f`.
