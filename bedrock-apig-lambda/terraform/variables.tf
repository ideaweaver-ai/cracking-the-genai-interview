variable "aws_region" {
  description = "AWS region for all resources (must match Bedrock Mantle availability)."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Name prefix for resources."
  type        = string
  default     = "bedrock-ask"
}

variable "lambda_zip_path" {
  description = "Path to the Linux Lambda deployment package (relative to this terraform/ directory)."
  type        = string
  default     = "../lambda/function.zip"
}

variable "lambda_handler" {
  description = "Lambda handler."
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  description = "Lambda runtime. Must match the packaged dependencies."
  type        = string
  default     = "python3.12"
}

variable "lambda_architectures" {
  description = "Lambda CPU architectures."
  type        = list(string)
  default     = ["x86_64"]
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 60
}

variable "lambda_memory_size" {
  description = "Lambda memory in MB."
  type        = number
  default     = 256
}

variable "model_id" {
  description = "Bedrock Mantle model ID."
  type        = string
  default     = "xai.grok-4.6"
}

variable "mantle_api_path" {
  description = "Mantle OpenAI-compatible API path prefix."
  type        = string
  default     = "/openai/v1"
}

variable "max_tokens" {
  description = "MAX_TOKENS env var for the Lambda."
  type        = string
  default     = "4096"
}

variable "reasoning_effort" {
  description = "REASONING_EFFORT env var for the Lambda (e.g. low, medium, high)."
  type        = string
  default     = "low"
}

variable "api_stage_name" {
  description = "API Gateway stage name."
  type        = string
  default     = "dev"
}

variable "tags" {
  description = "Tags applied to supported resources via the provider default_tags."
  type        = map(string)
  default = {
    Project   = "bedrock-ask"
    ManagedBy = "terraform"
  }
}
