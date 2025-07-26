resource "aws_lambda_function_url" "this" {
  function_name      = var.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["Content-Type"]
  }
}