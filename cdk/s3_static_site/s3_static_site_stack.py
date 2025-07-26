import os
import shutil
import tempfile

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy
)
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct


class S3StaticSiteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket_name: str, frontend_files: list, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create the public S3 bucket with website hosting and CORS
        website_bucket = s3.Bucket(self, "WebsiteBucket",
            bucket_name=bucket_name,
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            cors=[s3.CorsRule(
                allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.POST],
                allowed_origins=["*"],
                allowed_headers=["*"]
            )],
            removal_policy=RemovalPolicy.DESTROY  # Optional, useful for dev
        )

        self.bucket_url = website_bucket.bucket_website_url  # Optional output for reference

        # Create a temporary folder and copy selected frontend files into it
        temp_upload_dir = tempfile.mkdtemp()
        for filename in frontend_files:
            src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', filename))
            dst_path = os.path.join(temp_upload_dir, filename)

            # Validate file exists before copying
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
            else:
                raise FileNotFoundError(f"Frontend file not found: {src_path}")

        # Deploy only the selected files to the S3 bucket
        s3deploy.BucketDeployment(self, "DeployWebsiteFiles",
            destination_bucket=website_bucket,
            sources=[s3deploy.Source.asset(temp_upload_dir)],
        )
