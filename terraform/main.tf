# provider "aws" {
#   region = var.aws_region
# }

# module "dynamodb" {
#   source     = "./modules/dynamodb"
#   table_name = var.table_name
# }

# module "lambda" {
#   source           = "./modules/lambda"
#   function_name    = var.function_name
#   handler          = var.handler
#   runtime          = var.runtime
#   architecture     = var.architecture
#   role_arn         = var.role_arn
# }

# module "function_url" {
#   source        = "./modules/function_url"
#   function_name = module.lambda.lambda_function_name
# }

# output "lambda_function_url" {
#   value       = module.function_url.function_url
#   description = "The HTTPS URL to invoke your Lambda function"
# }
# module "cloudformation" {
#   source         = "./modules/cloudformation"
#   bucket_name    = var.bucket_name
# }

# # First, create the script.js file using templatefile
# resource "null_resource" "upload_static_site" {
#   depends_on = [
#     module.cloudformation,
#     module.function_url
#   ]

#   # Use triggers to pass the values we need
#   triggers = {
#     lambda_url = module.function_url.function_url
#     bucket_name = module.cloudformation.s3_bucket_name
#   }

#   # Generate script.js using sed with the trigger values
#   provisioner "local-exec" {
#     command = "sed \"s|%%LAMBDA_URL%%|${self.triggers.lambda_url}|g\" ../frontend/script.template.js > ../frontend/script.js"
#   }

#   # Then upload all files
#   provisioner "local-exec" {
#     command = "aws s3 cp ../frontend/index.html s3://${self.triggers.bucket_name}/index.html && aws s3 cp ../frontend/script.js s3://${self.triggers.bucket_name}/script.js && aws s3 cp ../frontend/style.css s3://${self.triggers.bucket_name}/style.css"
#   }
# }


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

module "cloudfront" {
  source      = "./modules/cloudfront"
  bucket_name = var.bucket_name
  aws_region  = var.aws_region
}

# Add this new output:
output "s3_bucket_name" {
  value       = module.cloudformation.s3_bucket_name  
  description = "Name of the S3 bucket"
}

output "cloudfront_url" {
  value       = "https://${module.cloudfront.cloudfront_domain_name}"
  description = "CloudFront URL for the website"
}

output "cloudfront_distribution_id" {
  value       = module.cloudfront.cloudfront_distribution_id
  description = "CloudFront Distribution ID for cache invalidation"
}

module "cloudwatch" {
  source          = "./modules/cloudwatch"
  function_name   = var.function_name
  distribution_id = module.cloudfront.cloudfront_distribution_id
  aws_region      = var.aws_region
}