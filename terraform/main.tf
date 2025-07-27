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
module "cloudformation" {
  source         = "./modules/cloudformation"
  bucket_name    = var.bucket_name
}

resource "null_resource" "upload_static_site" {
  depends_on = [module.cloudformation]

  provisioner "local-exec" {
    command = <<EOT
      aws s3 cp ../frontend/index.html s3://${module.cloudformation.s3_bucket_name}/index.html
      aws s3 cp ../frontend/script.js s3://${module.cloudformation.s3_bucket_name}/script.js
      aws s3 cp ../frontend/style.css s3://${module.cloudformation.s3_bucket_name}/style.css
    EOT
  }
}