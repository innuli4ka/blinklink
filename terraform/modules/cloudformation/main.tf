resource "aws_cloudformation_stack" "s3_website" {
  name          = "s3-static-site"
  template_body = file("${path.module}/s3-website.yml")

  capabilities = ["CAPABILITY_NAMED_IAM"]  # Needed to allow creation of the bucket policy

  parameters = {
    BucketName = var.bucket_name
  }

  tags = {
    Project = "StaticSite"
  }
}