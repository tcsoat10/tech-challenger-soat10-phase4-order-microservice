locals {
  use_mock = (terraform.workspace == "default" || terraform.workspace == "test")
}

data "terraform_remote_state" "rds" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_rds_outputs.tfstate"
  } : {
    bucket = "soattc-order-db"
    key    = "env:/${terraform.workspace}/order-microservice/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "aws" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_eks_outputs.tfstate"
  } : {
    bucket = "soattc-aws-infra"
    key    = "env:/${terraform.workspace}/aws-infra/terraform.tfstate"
    region = "us-east-1"
  }
}


data "terraform_remote_state" "stock" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_stock_outputs.tfstate"
  } : {
    bucket = "soattc-stock-app"
    key    = "env:/${terraform.workspace}/stock-microservice/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "payment" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_payment_outputs.tfstate"
  } : {
    bucket = "soattc-payment-app"
    key    = "env:/${terraform.workspace}/payment-microservice/terraform.tfstate"
    region = "us-east-1"
  }
}