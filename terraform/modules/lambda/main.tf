data "archive_file" "example" {
  type        = "zip"
  source_dir  = "${path.module}/../../../backend"
  output_path = "${path.module}/lambda.zip"
}


resource "aws_lambda_function" "this" {
  filename         = data.archive_file.example.output_path
  function_name    = var.function_name
  role             = var.role_arn  
  handler          = var.handler
  source_code_hash = data.archive_file.example.output_base64sha256
  architectures = [var.architecture]
  runtime = var.runtime
  }