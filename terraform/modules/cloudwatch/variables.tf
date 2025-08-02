# modules/cloudwatch/variables.tf

variable "function_name" {
  type        = string
  description = "Name of the Lambda function to monitor"
}

variable "distribution_id" {
  type        = string
  description = "CloudFront distribution ID to monitor"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}