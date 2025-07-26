output "eks_cluster_name" {
  value = aws_eks_cluster.cluster.name
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.cluster.endpoint
}

output "eks_cluster_ca" {
  value = aws_eks_cluster.cluster.certificate_authority[0].data
}

output "eks_node_security_group_id" {
  value = aws_security_group.eks_sg.id
}

output "eks_vpc_id" {
  value = data.aws_vpc.vpc.id
}