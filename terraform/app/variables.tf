variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "db_password" {
  description = "Database user password"
  type        = string
}

variable "db_name" {
  default = "order_microservice_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "payment_service_api_key" {
  description = "API key for payment microservice"
  type        = string
}

variable "secret_key" {
  description = "JWT Key"
  type        = string
}

variable "payment_service_url" {
  description = "URL to payment microservice"
  type        = string
}

variable "payment_notification_url" {
  description = "Notification url of the payment microservice"
  type        = string
}

variable "order_microservice_api_key" {
  description = "API Key to protect this microservice"
  type        = string
}

variable "stock_microservice_url" {
  description = "URL to stock microservice"
  type        = string
}

variable "stock_microservice_api_key" {
  description = "Stock microservice API key"
  type        = string
}