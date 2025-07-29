resource "aws_lambda_function_url" "this" {
  function_name      = var.function_name
  authorization_type = "NONE"
}