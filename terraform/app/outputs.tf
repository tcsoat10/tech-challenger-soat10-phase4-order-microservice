output "order_app_lb_endpoint" {
  description = "Endpoint do Load Balancer do order-app"
  value       = "{kubernetes_service.order_app_lb.status[0].load_balancer[0].ingress[0].hostname}/api/v1"
}