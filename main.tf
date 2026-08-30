terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3       = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
  }
}

# 1. إCreating S3 Bucket
resource "aws_s3_bucket" "demo_bucket" {
  bucket = "microservice-storage-bucket"

  tags = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}

# 2. Creating DynamoDB Table
resource "aws_dynamodb_table" "demo_table" {
  name         = "microservice-logs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LogID"

  attribute {
    name = "LogID"
    type = "S"
  }

  tags = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}