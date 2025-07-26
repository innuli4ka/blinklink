#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from s3_static_site.s3_static_site_stack import S3StaticSiteStack

app = App()

# Define values
bucket_name = "blinklink-44"  # Must be globally unique
frontend_files = ["index.html", "style.css", "script.js"]

print(f"Using bucket: {bucket_name}")
# Instantiate the stack with explicit env
S3StaticSiteStack(app,
    "S3StaticSiteStack",
    env=Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT", os.environ.get("AWS_ACCOUNT_ID")),
        region=os.environ.get("CDK_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-west-2"))
    ),
    bucket_name=bucket_name,
    frontend_files=frontend_files,
)

app.synth()
