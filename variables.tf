variable "aws_region" {
  description = "Región de AWS"
  type        = string
}

variable "profile" {
  description = "Nombre de perfil para el despliegue de la infraestructura"
  type        = string
}

variable "bucket" {
  description = "Nombre del Bucket de S3 donde está el terraform state de Networking"
  type        = string
}

variable "eks_tfstate_key" {
  description = "Llave del bucket S3 donde está el terraform state del EKS"
  type        = string
}

variable "ntw_tfstate_key" {
  description = "Llave del bucket S3 donde está el terraform state del Networking"
  type        = string
}

variable "workspace_key_prefix" {
  description = "Prefijo del espacio de trabajo para la Llave del bucket S3 donde está el terraform state"
  type        = string
}

variable "bucket_region" {
  description = "Región de AWS del Bucket de S3 donde está el terraform state"
  type        = string
}

# variable "istio_namespace_gateway" {
#   description = "Espacio de trabajo para el gateway de Istio"
#   type        = string
# }

# variable "istio_namespace" {
#   description = "Espacio de trabajo para los recursos de Istio"
#   type        = string
# }

# variable "istio_version" {
#   description = "Versión de istio"
#   type        = string
# }

variable "lb_ssl_ports" {
  description = "Puertos SSL para el Load Balancer"
  type        = string
}

variable "lb_ssl_cert" {
  description = "ARN del Certificado de Autoridad para el Load Balancer"
  type        = string
}