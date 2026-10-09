# Terraform — Bedrock Mantle + Lambda + API Gateway

Deploys the same stack as the console lab:

```text
POST /{stage}/ask  →  API Gateway (no auth)  →  Lambda  →  Bedrock Mantle
```

## Prerequisites

- Terraform `>= 1.5`
- AWS credentials with permission to manage IAM, Lambda, API Gateway, and CloudWatch Logs
- Region with Bedrock Mantle access (default `us-west-2`)
- A Linux Lambda zip at `../lambda/function.zip`

Rebuild the zip after code or dependency changes:

```bash
../scripts/package-lambda.sh
```

## Deploy

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # optional overrides
terraform init
terraform plan
terraform apply
```

After apply:

```bash
terraform output ask_url
terraform output -raw curl_example | bash
```

## What this creates

| Resource | Purpose |
|----------|---------|
| IAM role + Mantle inline policy | Lambda execution + `bedrock-mantle` token/inference |
| Lambda `bedrock-ask` | Python 3.12 handler from `function.zip` |
| API Gateway REST API | `POST /ask` (proxy) + `OPTIONS` CORS |
| Stage (`dev` by default) | Public invoke URL |

## Destroy

```bash
terraform destroy
```

## Notes

- Auth is **NONE** (open URL), matching the learning lab. Do not use this as-is in production without auth, throttling, and WAF.
- Model access is account-specific. If `xai.grok-4.6` is unavailable, change `model_id` / `mantle_api_path` in `terraform.tfvars`.
- Remote state (S3 + DynamoDB lock) is recommended for shared environments; add a `backend "s3"` block when you are ready.
