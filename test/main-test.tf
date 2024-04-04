# Se especifica la versión de los proveedores necesarios
terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
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

# Ejecuta el módulo para aplicar el parche en el NLB de Istio y se le proporcionan los valores de las variables
module "istio_ingress_patch" {
  #source                  = "git::https://github.com/SF-Bancoppel/unity-istio-module.git?ref=feature-istio-module"
  source                  = "git::https://github.com/samirmafud/HA-Istio-Ingress-Patch-Module.git?ref=main"
  aws_region              = var.aws_region
  profile                 = var.profile
  cluster_name            = data.terraform_remote_state.eks_out.outputs.cluster_name
  subnets_id              = [for subnet_name, subnet_id in data.terraform_remote_state.ntw_out.outputs.subnets_id : subnet_id if can(regex("^(eks-a|eks-b)$", subnet_name))]
  lb_ssl_ports            = var.lb_ssl_ports
  istio_namespace_gateway = var.istio_namespace_gateway
  istio_service_gateway   = var.istio_service_gateway
}