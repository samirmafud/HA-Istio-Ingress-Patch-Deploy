# Especifica la versión requerida del proveedor AWS y Kubernetes
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# Configura el proveedor AWS especificando la región y el perfil de AWS
provider "aws" {
  region  = var.aws_region
  profile = var.profile
}

# Se especifica el bucket s3 donde está almacenado el terraform state del clúster de EKS
data "terraform_remote_state" "eks_out" {
  backend   = "s3"
  workspace = terraform.workspace
  config = {
    bucket               = var.bucket
    key                  = var.eks_tfstate_key
    workspace_key_prefix = var.workspace_key_prefix
    region               = var.bucket_region
    endpoints = {
      s3 = "https://s3.us-east-1.amazonaws.com"
    }
  }
}

# Se especifica el bucket s3 donde está almacenado el terraform state de Networking
data "terraform_remote_state" "ntw_out" {
  backend   = "s3"
  workspace = terraform.workspace
  config = {
    bucket               = var.bucket
    key                  = var.ntw_tfstate_key
    workspace_key_prefix = var.workspace_key_prefix
    region               = var.bucket_region
    endpoints = {
      s3 = "https://s3.us-east-1.amazonaws.com"
    }
  }
}

# Define las variables locales correspondientes al nombre del clúster de EKS y los ids de las subnets asociadas al clúster de EKS
locals {
  cluster_name = data.terraform_remote_state.eks_out.outputs.cluster_name
  subnets_id   = [for subnet_name, subnet_id in data.terraform_remote_state.ntw_out.outputs.subnets_id : subnet_id if can(regex("^(eks-a|eks-b)$", subnet_name))]
}

# Recupera la información de las subnets privadas existentes a partir de los IDs generados en 'var.subnets_id'
data "aws_subnet" "module_subnet" {
  for_each = toset(local.subnets_id)
  id       = each.value
}

# Ejecuta los comandos de Kubernetes para actualizar el kubeconfig del clúster de EKS
resource "null_resource" "configure_kubectl" {
  provisioner "local-exec" {
    command = "aws eks --region ${var.aws_region} update-kubeconfig --name ${local.cluster_name} --profile ${var.profile}"
  }
}

# Ejecuta un parche en el servicio istio-ingressgateway en el namespace especificado para configurar el Load Balancer y asociarlo a las subnets del clúster de EKS
resource "null_resource" "patch_deployment" {
  provisioner "local-exec" {
    command = <<-EOT
      kubectl -n ${var.istio_namespace_gateway} patch service ${var.istio_service_gateway} --patch '{
        "metadata": {
          "annotations": {
            "service.beta.kubernetes.io/aws-load-balancer-backend-protocol": "tcp",
            "service.beta.kubernetes.io/aws-load-balancer-ssl-ports": "${var.lb_ssl_ports}",
            "service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout": "3600",
            "service.beta.kubernetes.io/aws-load-balancer-type": "nlb",
            "service.beta.kubernetes.io/aws-load-balancer-internal": "true",
            "service.beta.kubernetes.io/aws-load-balancer-subnets": "${join(",", local.subnets_id)}"
          }
        }
      }'
    EOT
  }

  depends_on = [null_resource.configure_kubectl]
}