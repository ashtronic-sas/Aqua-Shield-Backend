.PHONY: setup deploy package prepare-layer publish-layer create-lambda

# Define variables
BUCKET_NAME=bucket-example
FUNCTION_NAME=lambda-function-example
REGION=us-east-1
LOCAL_ZIP=deployment_package.zip
LAMBDA_HANDLER=app.handler
LAYER_NAME=my-dependencies-layer
LAYER_ZIP=dependencies-layer.zip
ROLE_ARN=arn:aws:iam::038462791127:role/lambda-role-arn
LAYER_ARN=

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Activating virtual environment and installing dependencies..."
	. venv/bin/activate; pip install -r requirements.txt

# Package the application
package:
	@echo "Packaging the application..."
	. venv/bin/activate; cd app; zip -r9 ../$(LOCAL_ZIP) .

# Prepare the layer directory with dependencies
prepare-layer:
	@echo "Preparing layer directory..."
	mkdir -p layer
	. venv/bin/activate; pip install -r requirements.txt -t layer/
	@echo "Packaging the dependencies layer..."
	cd layer && zip -r9 ../$(LAYER_ZIP) .

# Publish the layer directly to AWS Lambda
publish-layer:
	@echo "Publishing the layer to AWS Lambda directly..."
	@LAYER_ARN=$$(aws lambda publish-layer-version --layer-name $(LAYER_NAME) --zip-file fileb://$(LAYER_ZIP) --compatible-runtimes python3.8 --query 'LayerVersionArn' --output text); \
	echo "Layer ARN: $$LAYER_ARN"; \
	export LAYER_ARN=$$LAYER_ARN

# Create the Lambda function if it doesn't exist
create-lambda:
	@echo "Checking if Lambda function exists..."
	@if aws lambda get-function --function-name $(FUNCTION_NAME) 2>&1 | grep -q 'ResourceNotFoundException'; then \
		echo "Lambda function does not exist, creating..."; \
		aws lambda create-function \
			--function-name $(FUNCTION_NAME) \
			--runtime python3.8 \
			--role $(ROLE_ARN) \
			--handler $(LAMBDA_HANDLER) \
			--zip-file fileb://$(LOCAL_ZIP) \
			--region $(REGION); \
		echo "Waiting for function to be created..."; \
		sleep 30; \
	else \
		echo "Lambda function exists."; \
	fi
	@echo "Updating Lambda function configuration with layer..."
	aws lambda update-function-configuration --function-name $(FUNCTION_NAME) --layers $(LAYER_ARN)

# Complete deployment process
deploy: setup package prepare-layer publish-layer create-lambda
	@echo "Deployment complete."
