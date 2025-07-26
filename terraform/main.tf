provider "aws" {
  region = var.aws_region
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = var.table_name
}

module "lambda" {
  source           = "./modules/lambda"
  function_name    = var.function_name
  handler          = var.handler
  runtime          = var.runtime
  architecture     = var.architecture
  role_arn         = var.role_arn
}

module "function_url" {
  source        = "./modules/function_url"
  function_name = module.lambda.lambda_function_name
}

output "lambda_function_url" {
  value       = module.function_url.function_url
  description = "The HTTPS URL to invoke your Lambda function"
}
