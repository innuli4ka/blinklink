
output "s3_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_cloudformation_stack.s3_website.outputs["BucketName"]
}