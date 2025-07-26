#!/bin/bash

# This script asks for AWS credentials and saves them to ~/.aws so Terraform can use them

# Ask for the access key
read -p "Enter your AWS Access Key ID: " AWS_ACCESS_KEY_ID

# Ask for the secret key (hidden input)
read -s -p "Enter your AWS Secret Access Key (it won't be shown because of security measures): " AWS_SECRET_ACCESS_KEY
echo

# Ask for session token (optional, for temporary credentials)
read -s -p "Enter your AWS Session Token (it won't be shown because of security measures, you can press ENTER to skip): " AWS_SESSION_TOKEN
echo

# Ask for region (e.g., us-west-2)
read -p "Enter your AWS region: " AWS_REGION

# Make sure the .aws folder exists
mkdir -p ~/.aws

# Write credentials to the credentials file
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOF

# If the session token is not empty, add it to the credentials file
if [ ! -z "$AWS_SESSION_TOKEN" ]; then
  echo "aws_session_token = $AWS_SESSION_TOKEN" >> ~/.aws/credentials
fi

# ✅ FIX: This block was not closed in your version!
cat > ~/.aws/config <<EOF
[default]
region = $AWS_REGION
output = json
EOF

# 🔍 Now extract the actual IAM role
echo "🔍 Retrieving current IAM role ARN..."
CURRENT_ROLE_ARN=$(aws sts get-caller-identity --query Arn --output text)

# Convert assumed-role ARN to usable IAM role ARN
if [[ "$CURRENT_ROLE_ARN" == *"assumed-role"* ]]; then
  ROLE_NAME=$(echo "$CURRENT_ROLE_ARN" | cut -d'/' -f2)
  ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
  ACTUAL_ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"
else
  ACTUAL_ROLE_ARN="$CURRENT_ROLE_ARN"
fi

echo "✅ Using IAM Role ARN: $ACTUAL_ROLE_ARN"

# Write it into terraform/auto.tfvars
cat > terraform/auto.tfvars <<EOF
role_arn = "$ACTUAL_ROLE_ARN"
EOF

echo "✅ Credentials and role ARN configured successfully."
