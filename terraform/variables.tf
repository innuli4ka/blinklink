variable "aws_region" {
  type        = string
  description = "The AWS region where all resources will be created"
}

variable "table_name" {
  type        = string
  description = "Name of the DynamoDB table"
}

variable "function_name" {
  type        = string
  description = "Name of the Lambda function"
}


variable "handler" {
  type        = string
  description = "Lambda function handler (for example lambda_function.lambda_handler)"
}

variable "runtime" {
  type        = string
  description = "Runtime environment for the Lambda function, for example python3.12"
}

variable "architecture" {
  type        = string
  description = "Lambda architecture (e.g., arm64 or x86_64)"
}

variable "role_arn" {
  type        = string
  description = "ARN of the IAM role (LabRole) to attach to the Lambda function"
}

variable "bucket_name" {
  type        = string
  description = "The name of the S3 bucket for static website hosting"
}

variable "frontend_files" {
  type = list(object({
    source       = string
    key          = string
    content_type = string
  }))
}