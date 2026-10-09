locals {
  lambda_zip_abspath = abspath("${path.module}/${var.lambda_zip_path}")
}

resource "aws_lambda_function" "ask" {
  function_name = var.project_name
  role          = aws_iam_role.lambda.arn
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime
  architectures = var.lambda_architectures
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  filename         = local.lambda_zip_abspath
  source_code_hash = filebase64sha256(local.lambda_zip_abspath)

  environment {
    variables = {
      MODEL_ID         = var.model_id
      MANTLE_API_PATH  = var.mantle_api_path
      BEDROCK_REGION   = var.aws_region
      MAX_TOKENS       = var.max_tokens
      REASONING_EFFORT = var.reasoning_effort
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy.bedrock_mantle,
  ]
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.ask.function_name}"
  retention_in_days = 14
}
