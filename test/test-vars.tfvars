aws_region              = "us-east-1"
profile                 = "apolo"
bucket                  = "s3hatest3"
eks_tfstate_key         = "tfstate/eks-test.tfstate"
ntw_tfstate_key         = "tfstate/networking-test.tfstate"
workspace_key_prefix    = "UnityHA"
bucket_region           = "us-east-1"
lb_ssl_ports            = "443"
lb_ssl_cert             = "arn:aws:acm:us-east-1:533267162190:certificate/5870c022-e6e6-4b86-ba80-299b7314be25"