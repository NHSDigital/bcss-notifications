terraform {
  backend "s3" {
    key    = "communication-management/terraform.tfstate"
    region = "eu-west-2"
  }
}

