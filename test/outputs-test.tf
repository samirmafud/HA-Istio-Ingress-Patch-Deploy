output "cluster_name" {
  description = "El nombre del clúster de EKS"
  value       = local.cluster_name
}

output "aws_region" {
  description = "Región de AWS"
  value       = var.aws_region
}

output "profile" {
  description = "Nombre de perfil para el despliegue de la infraestructura"
  value       = var.profile
}

output "subnets_id" {
  description = "ID de las subnets"
  value       = join(",", local.subnets_id)
}

output "lb_ssl_ports" {
  description = "Puertos SSL para el Load Balancer"
  value       = var.lb_ssl_ports
}

output "lb_ssl_cert" {
  description = "ARN del Certificado de Autoridad para el Load Balancer"
  value       = var.lb_ssl_cert
}

output "istio_namespace_gateway" {
  description = "Espacio de trabajo para los recursos de Istio"
  value       = var.istio_namespace_gateway
}

output "istio_service_gateway" {
  description = "Servicio de Istio para el istio-ingressgateway"
  value       = var.istio_service_gateway
}