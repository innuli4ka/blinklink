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

variable "lambda_zip_file" {
  type        = string
  description = "Path to the zipped Lambda function code"
}

variable "handler" {
  type        = string
  description = "Lambda function handler (format: file.function)"
}

variable "runtime" {
  type        = string
  description = "Runtime environment for the Lambda function"
}

variable "architecture" {
  type        = string
  description = "Lambda architecture (e.g., arm64 or x86_64)"
}

variable "role_arn" {
  type        = string
  description = "ARN of the IAM role (LabRole) to attach to the Lambda function"
}
