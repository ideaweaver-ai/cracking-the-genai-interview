data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    sid     = "AllowLambdaAssume"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda" {
  name               = "${var.project_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Mantle permissions for short-term bearer tokens + inference (matches console lab).
data "aws_iam_policy_document" "bedrock_mantle" {
  statement {
    sid    = "BedrockMantleInference"
    effect = "Allow"
    actions = [
      "bedrock-mantle:CreateInference",
      "bedrock-mantle:Get*",
      "bedrock-mantle:List*",
    ]
    resources = [
      "arn:aws:bedrock-mantle:${var.aws_region}:${data.aws_caller_identity.current.account_id}:project/*",
    ]
  }

  statement {
    sid       = "BedrockMantleApiKeyAccess"
    effect    = "Allow"
    actions   = ["bedrock-mantle:CallWithBearerToken"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "bedrock_mantle" {
  name   = "${var.project_name}-bedrock-mantle"
  role   = aws_iam_role.lambda.id
  policy = data.aws_iam_policy_document.bedrock_mantle.json
}
