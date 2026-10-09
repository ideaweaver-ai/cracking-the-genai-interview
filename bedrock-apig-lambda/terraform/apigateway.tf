resource "aws_api_gateway_rest_api" "ask" {
  name        = "${var.project_name}-api"
  description = "Public POST /ask → Lambda → Bedrock Mantle"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "ask" {
  rest_api_id = aws_api_gateway_rest_api.ask.id
  parent_id   = aws_api_gateway_rest_api.ask.root_resource_id
  path_part   = "ask"
}

resource "aws_api_gateway_method" "ask_post" {
  rest_api_id   = aws_api_gateway_rest_api.ask.id
  resource_id   = aws_api_gateway_resource.ask.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "ask_post" {
  rest_api_id             = aws_api_gateway_rest_api.ask.id
  resource_id             = aws_api_gateway_resource.ask.id
  http_method             = aws_api_gateway_method.ask_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.ask.invoke_arn
}

# CORS preflight (handler also returns CORS headers on POST responses).
resource "aws_api_gateway_method" "ask_options" {
  rest_api_id   = aws_api_gateway_rest_api.ask.id
  resource_id   = aws_api_gateway_resource.ask.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "ask_options" {
  rest_api_id = aws_api_gateway_rest_api.ask.id
  resource_id = aws_api_gateway_resource.ask.id
  http_method = aws_api_gateway_method.ask_options.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "ask_options" {
  rest_api_id = aws_api_gateway_rest_api.ask.id
  resource_id = aws_api_gateway_resource.ask.id
  http_method = aws_api_gateway_method.ask_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "ask_options" {
  rest_api_id = aws_api_gateway_rest_api.ask.id
  resource_id = aws_api_gateway_resource.ask.id
  http_method = aws_api_gateway_method.ask_options.http_method
  status_code = aws_api_gateway_method_response.ask_options.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.ask_options]
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ask.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ask.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "ask" {
  rest_api_id = aws_api_gateway_rest_api.ask.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.ask.id,
      aws_api_gateway_method.ask_post.id,
      aws_api_gateway_integration.ask_post.id,
      aws_api_gateway_method.ask_options.id,
      aws_api_gateway_integration.ask_options.id,
      aws_api_gateway_integration_response.ask_options.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [
    aws_api_gateway_integration.ask_post,
    aws_api_gateway_integration.ask_options,
    aws_api_gateway_integration_response.ask_options,
  ]
}

resource "aws_api_gateway_stage" "ask" {
  rest_api_id   = aws_api_gateway_rest_api.ask.id
  deployment_id = aws_api_gateway_deployment.ask.id
  stage_name    = var.api_stage_name
}
