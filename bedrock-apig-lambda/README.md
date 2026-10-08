# Bedrock Mantle + Lambda + API Gateway (Console-Only)

Ask a question via **API Gateway** → **Lambda** → **Amazon Bedrock Mantle** (OpenAI **Responses API**).

This project uses **`bedrock-mantle` only** — not `bedrock-runtime`, and not Converse / InvokeModel.

See: [Endpoints supported by Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html)

```text
User (curl / Postman)
        │  POST /ask  {"question":"..."}
        ▼
API Gateway (REST, no auth)
        │  Lambda proxy
        ▼
Lambda (Python + openai package)
        │  Responses API + Bedrock API key
        ▼
https://bedrock-mantle.us-west-2.api.aws/openai/v1/responses
        model: openai.gpt-5.6-luna
```

## Prerequisites

- An AWS account with permission to use Bedrock Mantle, Lambda, API Gateway, and IAM
- Deploy in **`us-west-2`** (Oregon) — matching the model region
- Local tools to package deps: Python 3.12+, `pip`, `zip` (and optionally `curl` / `jq` for testing)

No separate Bedrock “request model access” step is required for this setup.

**Important:**
- Putting `requirements.txt` in the Lambda console editor does **not** install packages.
- You must build a deployment zip that already contains `openai`, then upload that zip.
- On a Mac/Windows laptop, a normal `pip install -t` builds the **wrong OS binaries**. `openai` depends on `pydantic_core`, which needs **Linux** `.so` files. Always use `./scripts/package-lambda.sh` (it downloads `manylinux` wheels).

## Project layout

| Path | Description |
|------|-------------|
| `lambda/handler.py` | Source for the Lambda function |
| `lambda/lambda_function.py` | Same code (console default module name) |
| `lambda/requirements.txt` | `openai` (installed into the zip, not by the console) |
| `scripts/package-lambda.sh` | Builds `lambda/function.zip` with code + deps |
| `scripts/test-ask.sh` | Sample curl against your deployed URL |

## 1. Create an Amazon Bedrock API key

Mantle calls via the OpenAI SDK authenticate with a **Bedrock API key** (bearer token), not SigV4 in this sample.

1. Open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/) in **us-west-2**.
2. Go to **API keys** (or account / security settings for Bedrock keys).
3. Create a key (long-term is fine for learning; prefer short-term in real use).
4. Copy the key — you will paste it into the Lambda env var `BEDROCK_API_KEY`.

> Do **not** use an OpenAI.com API key. Point the SDK at Mantle and use a **Bedrock** key.

Model ID: `openai.gpt-5.6-luna`

## 2. Create the Lambda IAM role

1. **IAM** → **Roles** → **Create role**.
2. Trusted entity: **AWS service** → **Lambda** → Next.
3. Attach managed policy: **`AWSLambdaBasicExecutionRole`** → Next.
4. Role name: `bedrock-ask-lambda-role` → Create role.
5. Open the role → **Add permissions** → **Create inline policy** → JSON.

Replace `111122223333` with your account ID:

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

6. Name the policy `bedrock-mantle-inference` → Create policy.

> Shortcut for learning: attach AWS managed policy **`AmazonBedrockMantleInferenceAccess`** if available in your account, instead of the inline policy above.

## 3. Create the Lambda function in the AWS Console

### 3a. Create the function (console click-path)

1. Open the [Lambda console](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions) — confirm the top-right region is **US West (Oregon) `us-west-2`**.
2. Click **Create function**.
3. Choose **Author from scratch**.
4. Fill in:
   - **Function name:** `bedrock-ask`
   - **Runtime:** **Python 3.12** (must match the zip — do **not** pick 3.13/3.14)
   - **Architecture:** **x86_64** (must match the zip — do **not** pick arm64)
5. Under **Change default execution role** / **Permissions**:
   - Select **Use an existing role**
   - Role: `bedrock-ask-lambda-role` (from step 2)
6. Click **Create function**.

### 3b. Install `openai` locally and build a zip (required)

Lambda’s online editor cannot run `pip install`. You install dependencies on your laptop, zip them with your code, then upload.

From the repo root:

```bash
./scripts/package-lambda.sh
```

What that script does:

1. `pip install -r lambda/requirements.txt -t lambda/package/`
2. Copies your handler in as `lambda_function.py` (console default name)
3. Zips the **contents** of `package/` into `lambda/function.zip` (~8 MB)

Manual equivalent:

```bash
cd lambda
rm -rf package function.zip
mkdir package
pip install -r requirements.txt -t package/
cp handler.py package/lambda_function.py
cd package && zip -r ../function.zip . && cd ..
```

The zip root must look like:

```text
function.zip
├── lambda_function.py
├── openai/
├── httpx/
├── pydantic/
└── ... (other openai dependencies)
```

Not `function.zip/package/...` — files must be at the **root** of the zip.

### 3c. Upload the zip in the console

1. Lambda → **bedrock-ask** → **Code** tab
2. **Upload from** → **.zip file**
3. Choose `lambda/function.zip` → **Save**
4. Wait until the update succeeds
5. **Runtime settings** → **Edit** → Handler: `lambda_function.lambda_handler` → Save

After upload, the left file tree should show `lambda_function.py` **and** folders like `openai/`, `httpx/`, etc. If you only see your `.py` file, the zip was wrong.

> Optional alternative: put `openai` in a **Lambda layer** and keep only `lambda_function.py` in the function. For learning, the single zip above is simpler.

### 3d. Timeout, memory, and environment variables (console)

1. Open the **Configuration** tab → **General configuration** → **Edit**:
   - **Timeout:** 0 min **30** sec (or higher)
   - **Memory:** 256 MB
   - Save
2. **Configuration** → **Environment variables** → **Edit** → **Add environment variable** for each:

| Key | Value |
|-----|-------|
| `BEDROCK_API_KEY` | *(paste your Amazon Bedrock API key)* |
| `MODEL_ID` | `openai.gpt-5.6-luna` |
| `MAX_TOKENS` | `1024` |
| `BEDROCK_REGION` | `us-west-2` |

3. Save.

### 3e. Test the function in the console (before API Gateway)

1. Open the **Test** tab (or use your existing `ask-bedrock` event).
2. Event JSON:

```json
{
  "httpMethod": "POST",
  "body": "{\"question\": \"What is Amazon Bedrock Mantle?\"}"
}
```

3. Click **Test**.
4. You should see status `200` and a body with `answer`, `model`, and `endpoint: bedrock-mantle`.

If it fails, open **Monitor** → **View CloudWatch logs** and check for missing `BEDROCK_API_KEY`, IAM, or wrong region.

## 4. Create an open API Gateway REST API

1. Stay in **us-west-2**.
2. **API Gateway** → **Create API** → **REST API** → **Build**.
3. Name: `bedrock-ask-api` → Create API.
4. **Create resource** `/ask`.
5. **Create method** **POST** on `/ask`:
   - Integration: **Lambda function**
   - Enable **Lambda proxy integration**
   - Function: `bedrock-ask`
   - Authorization: **NONE** (open — learning only)
6. Deploy to stage **`dev`**.
7. Invoke URL:

```text
https://{api-id}.execute-api.us-west-2.amazonaws.com/dev/ask
```

> **Security note:** This endpoint is public. Anyone with the URL can call it and incur Mantle/Bedrock charges. Delete it when finished.

## 5. Test end-to-end

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
  "model": "openai.gpt-5.6-luna",
  "endpoint": "bedrock-mantle"
}
```

### Request body

| Field | Required | Notes |
|-------|----------|--------|
| `question` | yes* | User question |
| `prompt` | yes* | Alias for `question` |

\* One of `question` or `prompt` is required.

## How the Lambda calls Mantle

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["BEDROCK_API_KEY"],
    base_url="https://bedrock-mantle.us-west-2.api.aws/openai/v1",
)
response = client.responses.create(
    model="openai.gpt-5.6-luna",
    input=[{"role": "user", "content": question}],
    max_output_tokens=1024,
)
```

- Endpoint host: `bedrock-mantle.us-west-2.api.aws`
- Path for GPT-5.6 Luna: `/openai/v1/responses` (not Converse, not `bedrock-runtime`)
- IAM action: `bedrock-mantle:CreateInference` (+ `CallWithBearerToken` when using an API key)

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| Missing `BEDROCK_API_KEY` | Env var not set on Lambda |
| 401 / unauthorized | Wrong key, or OpenAI.com key instead of Bedrock key |
| AccessDenied / CreateInference | IAM role missing Mantle permissions |
| `model isn't supported on this route` | Wrong base path — Luna needs `/openai/v1` |
| Lambda/API in wrong region | Create resources in **us-west-2** |
| `No module named 'openai'` | Zip missing deps, or only pasted `.py` in the editor — rebuild with `./scripts/package-lambda.sh` and upload `function.zip` |
| API Gateway 502 / timeout | Raise Lambda timeout; cold start + model latency |

CloudWatch: **Lambda** → `bedrock-ask` → **Monitor** → **View CloudWatch logs**.

## Cleanup

1. Delete API Gateway `bedrock-ask-api`
2. Delete Lambda `bedrock-ask`
3. Delete IAM role `bedrock-ask-lambda-role`
4. Revoke / delete the Bedrock API key

## Out of scope (by design)

- `bedrock-runtime` / Converse / InvokeModel
- Cognito, API keys on API Gateway, WAF
- Streaming responses
- SAM / CDK / Terraform
