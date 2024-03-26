# Configuración de Terraform para el despliegue del parche en el Istio Ingress

La configuración de Terraform ejecuta la aplicación de un parche al servicio istio-ingressgateway en un clúster de EKS para desplegar el Load Balancer en Istio.

- [Características](#características)
- [Uso](#uso)
- [Variables de Entrada](#variables-de-entrada)
- [Variables de Salida](#variables-de-salida)
- [Recursos Creados](#recursos-creados)
- [Dependencias](#dependencias)
- [Consideraciones](#consideraciones)

## Características

- Automatiza la actualización del kubeconfig para el clúster de EKS.

- Aplica parches al servicio 'istio-ingressgateway` para configurar el Load Balancer en el clúster de EKS.

## Uso

Para aplicar el parche al servicio Istio, se deben seguir los siguientes puntos:

Definir las credenciales de la cuenta AWS para poder implementar los recursos y acceder al bucket donde se almacenará el archivo del estado de Terraform .tfstate

Clonar el repositorio respectivo.

bash
Copy code
$ git clone <URL-del-repositorio>
Cambiar al directorio correspondiente.

bash
Copy code
$ cd <nombre-del-directorio>
Inicializar el proveedor y la configuración del backend ejecutando.

bash
Copy code
$ terraform init
Seleccionar el espacio de trabajo de Terraform.

bash
Copy code
$ terraform workspace select nombre_del_workspace
Si no existe el espacio de trabajo, se crea con el siguiente comando.

bash
Copy code
$ terraform workspace new nombre_del_workspace
Ejecutar el plan y verificarlo.

bash
Copy code
$ terraform plan -var-file="<archivo-variables>"
Si el plan es correcto, aplicar y aceptar la creación de los recursos.

bash
Copy code
$ terraform apply -var-file="<archivo-variables>"
Variables de entrada
Las variables de entrada utilizadas en el código incluyen:

aws_region: La región de AWS donde desea desplegar el parche.
profile: Nombre del perfil para el despliegue de la infraestructura.
bucket: Nombre del Bucket de S3 donde está el estado de Terraform.
eks_tfstate_key: Llave del bucket S3 donde está el estado de Terraform para el EKS.
ntw_tfstate_key: Llave del bucket S3 donde está el estado de Terraform para el Networking.
workspace_key_prefix: Prefijo del espacio de trabajo para la Llave del bucket S3 donde está el estado de Terraform.
bucket_region: Región de AWS del Bucket de S3 donde está el estado de Terraform.
lb_ssl_ports: Puertos SSL para el Load Balancer.
lb_ssl_cert: ARN del Certificado de Autoridad para el Load Balancer.
Recursos creados
La configuración de Terraform crea los siguientes recursos:

Configura el proveedor AWS especificando la región y el perfil.
Recupera el estado remoto de Terraform desde los buckets S3 especificados.
Realiza operaciones relacionadas con el clúster de EKS usando los comandos de Kubernetes.
Actualiza el servicio istio-ingressgateway con los parches necesarios en el clúster de EKS.