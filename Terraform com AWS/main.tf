terraform {
  required_version = "1.8.5"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.55.0"
    }
  }
}

provider "aws" {
    region = "us-east-1"
}

resource "aws_s3_bucket" "my-bucket-1" {
    bucket = "benihime-aratame-254678954674"

    tags = {
      name = "My bucket"
      Environment = "Dev"
      Managedby = "Terraform"
    }
}