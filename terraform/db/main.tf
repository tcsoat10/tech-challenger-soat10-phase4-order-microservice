# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0
# Fiap Pos tech

terraform {
  backend "s3" {
    bucket = "soattc-order-db"
    key    = "order-microservice/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

provider "aws" {
  region = "us-east-1"
}

data "aws_vpc" "vpc" {
  cidr_block = "172.31.0.0/16"
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.vpc.id]
  }
}

data "aws_security_group" "eks_sg" {
  count = var.eks_sg_id == "" ? 1 : 0
  filter {
    name   = "group-name"
    values = ["eks-cluster-sg-soat10tc-cluster-eks*"]
  }
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.vpc.id]
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "rds-order-mysql-sg"
  description = "Allow inbound traffic to RDS MySQL instance"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    description     = "Allow MySQL traffic from EKS cluster"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [var.eks_sg_id != "" ? var.eks_sg_id : data.aws_security_group.eks_sg[0].id]
  }

  tags = {
    Name = "rds-order-mysql-sg"
  }
}

resource "aws_db_instance" "mysql" {
  identifier             = "order-microservice-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = true
  apply_immediately      = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}