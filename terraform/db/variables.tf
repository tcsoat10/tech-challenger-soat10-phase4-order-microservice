variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database user password"
  type        = string
}

variable "db_name" {
  default = "order_microservice_db"
}

variable "eks_sg_id" {
  description = "ID do Security Group do EKS (mock para CI)"
  type        = string
  default     = "sg-mockid123456789"
}