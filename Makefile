.PHONY: deploy generate_script deploy-frontend all

deploy-backend:
	@echo "Running AWS credential setup..."
	bash setup.sh

	@echo "Initializing Terraform..."
	cd terraform && terraform init

	@echo "Running Terraform plan..."
	cd terraform && terraform plan -var-file=terraform.tfvars

	@echo "Applying Terraform..."
	cd terraform && terraform apply -var-file=terraform.tfvars -auto-approve

	@echo "Getting latest Lambda URL..."
	terraform output -raw lambda_function_url > lambda_url.txt


	@echo "Generating updated script.js from template..."
	$(MAKE) generate_script

	@echo "Cleaning up..."
	@rm lambda_url.txt

	@echo "Deploy complete"

generate_script:
	@sed "s|%%LAMBDA_URL%%|$(shell cat lambda_url.txt)|g" frontend/script.template.js > frontend/script.js
	@echo "✔ script.js generated with latest Lambda URL"

deploy-frontend:
	@echo "Deploying static site to S3 via CDK..."
	cd cdk && \
	export CDK_DEFAULT_ACCOUNT=$$(aws sts get-caller-identity --query Account --output text) && \
	export CDK_DEFAULT_REGION=us-west-2 && \
	pip install -r requirements.txt && \
	cdk bootstrap && \
	cdk deploy --require-approval never

all:
	@echo "Running full deploy: backend (Terraform) + frontend (CDK)..."
	$(MAKE) deploy-backend
	$(MAKE) deploy-frontend
	@echo "✔ All components deployed successfully"
