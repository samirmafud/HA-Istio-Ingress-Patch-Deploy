# Configuración de Terraform para el despliegue del parche en el Istio Ingress

La configuración de Terraform ejecuta la aplicación de un parche al servicio istio-ingressgateway en un clúster de EKS para configurar los parámetros necesarios en el Load Balancer de Istio.

- [Características](#características)
- [Uso](#uso)
- [Variables de Entrada](#variables-de-entrada)
- [Variables de Salida](#variables-de-salida)
- [Recursos Creados](#recursos-creados)
- [Dependencias](#dependencias)
- [Consideraciones](#consideraciones)
- [Pruebas](#pruebas)

## Características

- Configura el proveedor AWS especificando la región y el perfil.

- Recupera el estado remoto de Terraform desde los buckets S3 especificados.

- Automatiza la actualización del kubeconfig para el clúster de EKS.

- Aplica un parche al servicio 'istio-ingressgateway' para configurar el Load Balancer en el clúster de EKS.


## Uso

Para poder utilizar este módulo de despliegue y aplicar el parche al servicio Istio, se deben realizar los siguientes puntos:

- Definir las credenciales de la cuenta AWS para poder implementar los recursos y acceder al bucket donde se almacenará el archivo del estado de Terraform .tfstate.

- Clonar el repositorio respectivo en el espacio de trabajo donde se realizará el despliegue:

```bash
$ git clone <URL-del-repositorio>
```

- Cambiar al directorio recién creado.

```bash
$ cd <nombre-del-directorio>
```
- Asegurar que las subnets a las que se apunta en la variable 'var.subents_id' en el archivo 'main.tf' estén etiquetadas correctamente.

- Asegurar que los valores de las variables definidas en el archivo .tfvars sean correctos.

- Se deben especificar correctamente los valores del bucket S3 donde está almacenado el estado de Terraform .tfstate del clúster de EKS y los recursos de red en las variables 'var.bucket', 'var.eks_tfstate_key', 'var.ntw_tfstate_key', 'var.workspace_key_prefix' y 'var.bucket_region'.

- Se deben especificar correctamente los valores del bucket S3 donde estará almacenado el estado de Terraform .tfstate de este módulo en el archivo 'backend.tf'.

Una vez se completa con lo anterior, se ejecuta el comando para inicializar el proveedor y la configuración del backend.

```bash
$ terraform init
```

Después se selecciona el workspace de Terraform en el cual se esté trabajando.

```bash
$ terraform workspace select <nombre_del_workspace>
```

En caso de que no exista el workspace seleccionado, se debe crear con el siguiente comando.

```bash
$ terraform workspace new <nombre_del_workspace>
```

Posteriormente, se ejecuta el plan y se verifica el mismo, para asegurar la creación de la configuración deseada para cada uno de los recursos.

```bash
$ terraform plan -var-file="<archivo .tfvars de los valores de la configuración>" -var "profile=<iniciativa de Unity>" -out=plan
```

Si la información proporcionada por el plan es correcta, se aplica y acepta para la creación de los recursos.

```bash
$ terraform apply plan
```


## Variables de entrada

- `aws_region` - La región de AWS a utilizar.

- `profile` - Nombre del perfil para el despliegue de la infraestructura.

- `bucket` - Nombre del Bucket de S3 donde está el estado de Terraform.

- `eks_tfstate_key` - Llave del bucket S3 donde está el estado de Terraform del clúster de EKS.

- `ntw_tfstate_key` - Llave del bucket S3 donde está el estado de Terraform del clúster del Networking.

- `workspace_key_prefix` - Prefijo del espacio de trabajo para la Llave del bucket S3 donde está el estado de Terraform.

- `bucket_region` - Región de AWS del Bucket de S3 donde está el estado de Terraform.

- `istio_namespace_gateway` - Nombre del espacio de trabajo para el gateway de Istio.

- `istio_service_gateway` - Nombre del Servicio de Istio para el istio-ingressgateway.

- `lb_ssl_ports` - Puertos SSL para el Load Balancer.


## Variables de salida

El código actualmente no produce variables de salida.


## Recursos creados

El despliegue de Terraform crea los siguientes recursos en la cuenta de AWS:

- Configura el proveedor AWS especificando la región y el perfil de AWS.

- Trae el estado remoto de Terraform desde el bucket S3 especificado donde se encuentra el estado remoto del clúster de EKS y de los recursos de red.

- Crea un recurso para ejecutar la actualización de la configuración y el contexto del Kubeconfig del clúster de EKS.

- Crea un recurso para ejecutar un parche en el servicio istio-ingressgateway para que el Load Balancer esté configurado y asociado a las subredes del clúster de EKS.


## Dependencias

Este módulo depende de los siguientes recursos:

- Recursos de red desplegados en la cuenta de AWS obtenidos del módulo Unity-Networking-deploy y un bucket S3 donde se almacena el estado de Terraform de este módulo.

- Un clúster de EKS desplegado en la cuenta de AWS obtenido del módulo Unity-EKS-deploy y un bucket S3 donde se almacena el estado de Terraform de este módulo.

- Tener configurados los recursos de Istio ('istio_base', 'istio_d' e 'istio_ingress') en el clúster de EKS obtenidos del módulo Unity-Istio-deploy.


## Consideraciones

- Asegurar que las subnets a las que se apunta en la variable 'var.subents_id' en el archivo 'main.tf' estén etiquetadas correctamente.

- Asegurar que los valores de las variables definidas en el archivo .tfvars sean correctos.

- Se deben especificar correctamente los valores del bucket S3 donde está almacenado el estado de Terraform .tfstate del clúster de EKS y los recursos de red en las variables 'var.bucket', 'var.eks_tfstate_key', 'var.ntw_tfstate_key', 'var.workspace_key_prefix' y 'var.bucket_region'.

- Se deben especificar correctamente los valores del bucket S3 donde estará almacenado el estado de Terraform .tfstate de este módulo en el archivo 'backend.tf'.


## Pruebas

Este módulo incorpora pruebas unitarias desarrolladas con `tftest` y `pytest`, las cuales pertencen a liberías de `python`. Las pruebas se encuentran en el directorio `test`. Para su ejecución, se deben seguir los siguientes pasos:

1. Se debe de navegar hasta el directorio `test` dentro del repositorio.
    ```bash
    cd test
2. Asegurarse de tener`python` instalado en la máquina donde se llevarán a cabo las pruebas, además de instalar las siguientes librerías.
    ```python
      # tftest
      pip install tftest

      # pytest
      pip install pytest

      #boto3
      pip install boto3
    ```
4. Se debe de ejecutar el siguiente comando para ejecutar las pruebas:
    ```bash
    pytest
    ```
    #### Nota
    Deben configurarse las credenciales de AWS correspondientes como variables de entorno, ya que la prueba implica la creación de infraestructura real en una cuenta de AWS, lo cual podría incurrir en cargos.