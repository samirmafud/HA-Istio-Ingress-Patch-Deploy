output "cluster_name" {
  description = "El nombre del clúster de EKS"
  value       = data.terraform_remote_state.eks_out.outputs.cluster_name
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
  value       = join(",", [for subnet_name, subnet_id in data.terraform_remote_state.ntw_out.outputs.subnets_id : subnet_id if can(regex("^(eks-a|eks-b)$", subnet_name))])
}

output "lb_ssl_ports" {
  description = "Puertos SSL para el Load Balancer"
  value       = var.lb_ssl_ports
}

output "istio_namespace_gateway" {
  description = "Espacio de trabajo para los recursos de Istio"
  value       = var.istio_namespace_gateway
}

output "istio_service_gateway" {
  description = "Servicio de Istio para el istio-ingressgateway"
  value       = var.istio_service_gateway
}