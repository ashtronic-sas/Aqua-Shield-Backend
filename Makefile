.PHONY: setup deploy package upload create-bucket update-lambda publish-layer

# Define variables
BUCKET_NAME=bucket-example
FUNCTION_NAME=your-lambda-function-name
REGION=us-east-1
LOCAL_ZIP=deployment_package.zip
LAMBDA_HANDLER=app.handler
LAYER_NAME=my-dependencies-layer
LAYER_ZIP=dependencies-layer.zip

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

# Create the S3 bucket if it doesn't exist
create-bucket:
	@echo "Checking if S3 bucket exists..."
	@if ! aws s3 ls "s3://$(BUCKET_NAME)" 2>&1 | grep -q 'NoSuchBucket'; then \
		echo "Bucket already exists"; \
	else \
		echo "Creating S3 bucket..."; \
		aws s3 mb s3://$(BUCKET_NAME) --region $(REGION); \
	fi

# Upload the deployment package to S3
upload:
	@echo "Uploading the deployment package to S3..."
	aws s3 cp $(LOCAL_ZIP) s3://$(BUCKET_NAME)/$(LOCAL_ZIP)

# Package and publish layer
publish-layer:
	@echo "Packaging the dependencies layer..."
	cd layer && zip -r ../$(LAYER_ZIP) .
	@echo "Publishing the layer to AWS Lambda..."
	aws lambda publish-layer-version --layer-name $(LAYER_NAME) --zip-file fileb://$(LAYER_ZIP) --compatible-runtimes python3.8

# Deploy or update the Lambda function
update-lambda: publish-layer
	@echo "Deploying or updating Lambda function..."
	aws lambda update-function-code --function-name $(FUNCTION_NAME) --s3-bucket $(BUCKET_NAME) --s3-key $(LOCAL_ZIP)
	aws lambda update-function-configuration --function-name $(FUNCTION_NAME) --layers $(LAYER_ARN)

# Complete deployment process
deploy: setup package create-bucket upload update-lambda
	@echo "Deployment complete."
