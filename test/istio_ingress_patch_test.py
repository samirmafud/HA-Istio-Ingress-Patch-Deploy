import pytest
import tftest
import subprocess
import os

# Define una ruta al directorio que contiene los archivos de configuración de Terraform
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Define la región de AWS como una variable global
AWS_REGION = "us-east-1"

# Define el nombre del clúster como una variable global
CLUSTER_NAME = "bcpl-eks-dev-apolo"

# Define el perfil como una variable global
PROFILE = "apolo"

# Configura la secuencia para desplegar los recursos
@pytest.fixture(scope="module", autouse=True)
def terraform_output():
    tf = tftest.TerraformTest(FIXTURES_DIR)
    tf.setup(workspace_name="dev")
    tf.apply(tf_var_file="test-vars.tfvars")
    yield tf.output()
    tf.destroy(tf_var_file="test-vars.tfvars",auto_approve=True)

# Verifica el estado del Load Balancer
def test_load_balancer_status(terraform_output):
    # Declara el nombre del Namespace
    name_space = "istio-ingress"

    # Declara el nombre del servicio
    svc = "istio-ingressgateway"

    # Ejecuta el comando para actualizar el kubeconfig del clúster de EKS
    update_kubeconfig_cmd = f"aws eks update-kubeconfig --name {CLUSTER_NAME} --region {AWS_REGION} --profile {PROFILE}"
    subprocess.run(update_kubeconfig_cmd, shell=True, check=True)

    # Ejecuta el comando de kubectl para conocer el estado del Load Balancer
    cmd = f"kubectl describe svc {svc} -n {name_space}"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    # Verifica que el estado del Load balancer esté asegurado
    assert "Ensured load balancer" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"

# Verifica la instalación del parche en el Load Balancer
def test_load_balancer_patch(terraform_output):
    # Declara el nombre del Namespace
    name_space = "istio-ingress"

    # Declara el nombre del servicio
    svc = "istio-ingressgateway"

    # Ejecuta el comando para actualizar el kubeconfig del clúster de EKS
    update_kubeconfig_cmd = f"aws eks update-kubeconfig --name {CLUSTER_NAME} --region {AWS_REGION} --profile {PROFILE}"
    subprocess.run(update_kubeconfig_cmd, shell=True, check=True)

    # Ejecuta el comando de kubectl para conocer el estado del Load Balancer
    cmd = f"kubectl describe svc {svc} -n {name_space}"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    # Verifica que el parche se haya aplicado correctamente en los servicios indicados
    assert "service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: 3600" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-internal: true" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-east-1:533267162190:certificate/5870c022-e6e6-4b86-ba80-299b7314be25" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-ssl-ports: https" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-subnets: subnet-0fad6edde9b8cde59,subnet-0585bf6783ec9d761" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"
    assert "service.beta.kubernetes.io/aws-load-balancer-type: nlb" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"