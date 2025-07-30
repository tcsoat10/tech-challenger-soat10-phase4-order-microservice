provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc-order-app"
    key    = "order-microservice/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

# data "terraform_remote_state" "aws" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-aws-infra"
#     key    = "order-microservice/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

# data "terraform_remote_state" "rds" {
#   backend = "s3"
#   config = {
#     bucket = "soattc-order-db"
#     key    = "order-microservice/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

resource "kubernetes_deployment" "order_app" {
  depends_on = [kubernetes_service.order_app_lb]
  metadata {
    name      = "order-app"
    namespace = "default"
    labels = {
      app = "order-app"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "order-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "order-app"
        }
      }
      spec {
        container {
          name  = "order-app"
          image = "086134737169.dkr.ecr.us-east-1.amazonaws.com/soattc-order-app:latest"
          env {
            name  = "MYSQL_HOST"
            value = replace(data.terraform_remote_state.rds.outputs.db_endpoint, ":3306", "")
          }
          env {
            name  = "MYSQL_USER"
            value = var.db_username
          }
          env {
            name  = "MYSQL_PASSWORD"
            value = var.db_password
          }
          env {
            name  = "MYSQL_PORT"
            value = "3306"
          }
          env {
            name  = "SECRET_KEY"
            value = var.secret_key
          }
          env {
            name = "PAYMENT_SERVICE_API_KEY"
            value = var.payment_service_api_key
          }
          env {
            name = "PAYMENT_SERVICE_URL"
            value = data.terraform_remote_state.payment.outputs.payment_app_lb_endpoint
          }
          env {
            name = "PAYMENT_NOTIFICATION_URL"
            value = "${kubernetes_service.order_app_lb.status[0].load_balancer[0].ingress[0].hostname}/api/v1/webhooks/payment_notification"
          }
          env {
            name = "ORDER_MICROSERVICE_X_API_KEY"
            value = var.order_microservice_api_key
          }
          env {
            name = "STOCK_MICROSERVICE_URL"
            value = data.terraform_remote_state.stock.outputs.stock_app_lb_endpoint
          }
          env {
            name = "STOCK_MICROSERVICE_X_API_KEY"
            value = var.stock_microservice_api_key
          }
          env {
            name = "MYSQL_DATABASE"
            value = data.terraform_remote_state.rds.outputs.db_name
          }
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "order_app_lb" {  
  metadata {
    name      = "order-app-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "order-app"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8000
    }
  }
}