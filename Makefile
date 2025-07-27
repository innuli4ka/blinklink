.PHONY: deploy deploy-backend generate_script deploy-frontend all

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
	cd terraform && terraform output -raw lambda_function_url > ../lambda_url.txt

	@echo "Generating updated script.js from template..."
	$(MAKE) generate_script

	@echo "Deploying frontend files to S3..."
	$(MAKE) deploy-frontend

	@echo "Cleaning up..."
	@rm lambda_url.txt

	@echo "Deploy complete"

generate_script:
	@sed "s|%%LAMBDA_URL%%|$(shell cat lambda_url.txt)|g" frontend/script.template.js > frontend/script.js
	@echo "✔ script.js generated with latest Lambda URL"

deploy-frontend:
	cd terraform && terraform apply -target=null_resource.upload_static_site -var-file=terraform.tfvars -auto-approve
	@echo "✔ Frontend files uploaded to S3"

all: deploy-backend
