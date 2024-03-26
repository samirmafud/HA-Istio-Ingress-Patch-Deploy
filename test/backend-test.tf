# Se especifica el backend para el estado de Terraform que se hospedará en un bucket S3.
terraform {
  backend "s3" {
    bucket               = "s3hatest3"
    key                  = "tfstate/istio-ingress-patch-test.tfstate"
    workspace_key_prefix = "UnityHA"
    region               = "us-east-1"
    endpoints = {
      s3 = "https://s3.us-east-1.amazonaws.com"
    }
  }
}