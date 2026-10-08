# Bedrock Mantle + Lambda + API Gateway (Console-Only)

Ask a question via **API Gateway** → **Lambda** → **Amazon Bedrock Mantle** (OpenAI-compatible **Responses API**).

This project uses **`bedrock-mantle` only** — not `bedrock-runtime`, and not Converse / InvokeModel.

Default model: **`xai.grok-4.6`** in **`us-west-2`**.

See: [Endpoints supported by Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)

```text
User (curl / Postman)
        │  POST /ask  {"question":"..."}
        ▼
API Gateway (REST, no auth)
        │  Lambda proxy
        ▼
Lambda (Python + openai SDK package)
        │  Responses API (short-term Bedrock token from IAM role)
        ▼
https://bedrock-mantle.us-west-2.api.aws/openai/v1/responses
        model: xai.grok-4.6
```

## Prerequisites

- An AWS account with permission to use Bedrock Mantle, Lambda, API Gateway, and IAM
- Deploy in **`us-west-2`** (Oregon)
- Local tools to package deps (optional if you use the prebuilt zip): Python 3.12+, `pip`, `zip` (and optionally `curl` / `jq` for testing)

**Important:**
- Putting `requirements.txt` in the Lambda console editor does **not** install packages.
- Upload `lambda/function.zip` (prebuilt in this repo) **or** rebuild with `./scripts/package-lambda.sh`.
- On a Mac/Windows laptop, a normal `pip install -t` builds the **wrong OS binaries**. Always use `./scripts/package-lambda.sh` (manylinux wheels for Lambda Python 3.12 / x86_64).

## Project layout

| Path | Description |
|------|-------------|
| `lambda/handler.py` | Source for the Lambda function |
| `lambda/lambda_function.py` | Same code (console default module name) |
| `lambda/requirements.txt` | `openai` + `aws-bedrock-token-generator` |
| `lambda/function.zip` | Prebuilt Linux deployment package (upload this in the console) |
| `scripts/package-lambda.sh` | Rebuilds `lambda/function.zip` with code + deps |
| `scripts/test-ask.sh` | Sample curl against your deployed URL |

## 1. Create the Lambda IAM role

1. **IAM** → **Roles** → **Create role**.
2. Trusted entity: **AWS service** → **Lambda** → Next.
3. Attach managed policies:
   - **`AWSLambdaBasicExecutionRole`**
   - **`AmazonBedrockMantleInferenceAccess`** (if available)
4. Role name: `bedrock-ask-lambda-role` → Create role.

If the managed Mantle policy is missing, add this inline policy (replace `111122223333` with your account ID):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockMantleInference",
      "Effect": "Allow",
      "Action": [
        "bedrock-mantle:CreateInference",
        "bedrock-mantle:Get*",
        "bedrock-mantle:List*"
      ],
      "Resource": "arn:aws:bedrock-mantle:us-west-2:111122223333:project/*"
    },
    {
      "Sid": "BedrockMantleApiKeyAccess",
      "Effect": "Allow",
      "Action": "bedrock-mantle:CallWithBearerToken",
      "Resource": "*"
    }
  ]
}
```

> The Lambda generates a **short-term Bedrock bearer token from its IAM role** (`aws-bedrock-token-generator`). A static `BEDROCK_API_KEY` is optional.

## 2. Create the Lambda function in the AWS Console

### 2a. Create the function

1. Open the [Lambda console](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions) in **us-west-2**.
2. **Create function** → **Author from scratch**
   - Name: `bedrock-ask`
   - Runtime: **Python 3.12** (must match the zip — not 3.13/3.14)
   - Architecture: **x86_64**
   - Role: `bedrock-ask-lambda-role`
3. Create function.

### 2b. Upload `function.zip`

**Option A — use the prebuilt zip in this repo**

1. **Code** → **Upload from** → **.zip file**
2. Choose `lambda/function.zip` → **Save**
3. **Runtime settings** → Handler: `lambda_function.lambda_handler`

**Option B — rebuild locally**

```bash
./scripts/package-lambda.sh
```

Then upload the new `lambda/function.zip` the same way.

After upload, the file tree should show `lambda_function.py` **and** folders like `openai/`, `httpx/`, `pydantic_core/`.

### 2c. Timeout, memory, and environment variables

1. **Configuration** → **General configuration**:
   - Timeout: **60** seconds
   - Memory: **256** MB (or more)
2. **Environment variables**:

| Key | Value |
|-----|-------|
| `MODEL_ID` | `xai.grok-4.6` |
| `MANTLE_API_PATH` | `/openai/v1` |
| `BEDROCK_REGION` | `us-west-2` |
| `MAX_TOKENS` | `4096` |
| `REASONING_EFFORT` | `low` |

> Grok spends tokens on reasoning. If `MAX_TOKENS` is too low (e.g. 1024), you may get an empty/`incomplete` answer. Keep `REASONING_EFFORT=low` for simple Q&A.

### 2d. Test in the console

```json
{
  "httpMethod": "POST",
  "body": "{\"question\": \"What is Amazon Bedrock?\"}"
}
```

Expect `200` with `answer`, `model: xai.grok-4.6`, and `endpoint: bedrock-mantle`.

## 3. Create an open API Gateway REST API

1. Stay in **us-west-2**.
2. **API Gateway** → **REST API** → name `bedrock-ask-api`.
3. Resource `/ask`, method **POST**, Lambda proxy → `bedrock-ask`, Authorization **NONE**.
4. Deploy stage **`dev`**.

Invoke URL (must include stage **and** `/ask`):

```text
https://{api-id}.execute-api.us-west-2.amazonaws.com/dev/ask
```

> Wrong URLs (missing `/dev` or `/ask`) return `{"message":"Missing Authentication Token"}` even when the API is open.

## 4. Test end-to-end

```bash
export API_URL="https://YOUR_API_ID.execute-api.us-west-2.amazonaws.com/dev/ask"

curl -sS -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Amazon Bedrock?"}'
```

Or:

```bash
chmod +x scripts/test-ask.sh
export API_URL="https://YOUR_API_ID.execute-api.us-west-2.amazonaws.com/dev/ask"
./scripts/test-ask.sh
```

### Expected success response

```json
{
  "answer": "...",
  "model": "xai.grok-4.6",
  "endpoint": "bedrock-mantle"
}
```

## How the Lambda calls Mantle

```python
from openai import OpenAI
from aws_bedrock_token_generator import provide_token

client = OpenAI(
    api_key=provide_token(region="us-west-2"),
    base_url="https://bedrock-mantle.us-west-2.api.aws/openai/v1",
)
response = client.responses.create(
    model="xai.grok-4.6",
    input=[{"role": "user", "content": question}],
    max_output_tokens=4096,
    reasoning={"effort": "low"},
)
```

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| `Missing Authentication Token` | Wrong API URL — use `.../dev/ask` |
| Empty answer / `incomplete` | Raise `MAX_TOKENS`; set `REASONING_EFFORT=low` |
| AccessDenied / model not available | Account agreement / model access for that model ID |
| `model isn't supported on this route` | Wrong `MANTLE_API_PATH` (`/openai/v1` for Grok) |
| `No module named 'openai'` / `pydantic_core` | Bad zip or wrong Python runtime — use Python 3.12 + prebuilt zip |
| API Gateway 502 / timeout | Raise Lambda timeout (60s+) |

## Cleanup

1. Delete API Gateway `bedrock-ask-api`
2. Delete Lambda `bedrock-ask`
3. Delete IAM role `bedrock-ask-lambda-role`

## Out of scope (by design)

- `bedrock-runtime` / Converse / InvokeModel
- Cognito, API keys on API Gateway, WAF
- Streaming responses
- SAM / CDK / Terraform
