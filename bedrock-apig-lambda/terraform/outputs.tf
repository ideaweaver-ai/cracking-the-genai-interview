output "ask_url" {
  description = "POST JSON {\"question\":\"...\"} to this URL."
  value       = "${aws_api_gateway_stage.ask.invoke_url}/ask"
}

output "lambda_function_name" {
  description = "Deployed Lambda function name."
  value       = aws_lambda_function.ask.function_name
}

output "lambda_role_arn" {
  description = "IAM role ARN used by the Lambda."
  value       = aws_iam_role.lambda.arn
}

output "api_gateway_id" {
  description = "REST API ID."
  value       = aws_api_gateway_rest_api.ask.id
}

output "api_stage_name" {
  description = "API Gateway stage name."
  value       = aws_api_gateway_stage.ask.stage_name
}

output "curl_example" {
  description = "Sample curl against the deployed endpoint."
  value       = <<-EOT
    curl -sS -X POST "${aws_api_gateway_stage.ask.invoke_url}/ask" \
      -H "Content-Type: application/json" \
      -d '{"question":"What is Amazon Bedrock?"}'
  EOT
}
