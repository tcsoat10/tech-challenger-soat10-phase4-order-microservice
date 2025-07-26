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