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

# Verifica la instalación del parche en el Load Balancer
def test_istio_base_creation(terraform_output):
    # Declara el nombre del Namespace
    name_space = "istio-system"

    # Declara el nombre del servicio
    svc = "istio-ingressgateway"

    # Ejecuta el comando para actualizar el kubeconfig del clúster de EKS
    update_kubeconfig_cmd = f"aws eks update-kubeconfig --name {CLUSTER_NAME} --region {AWS_REGION} --profile {PROFILE}"
    subprocess.run(update_kubeconfig_cmd, shell=True, check=True)

    # Ejecuta el comando de kubectl para conocer el estado del Load Balancer
    cmd = f"kubectl describe svc {svc} -n {name_space}"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    # Verifica que el estado del Deployment sea "deployed" en la columna STATUS
    assert "Ensured load balancer" in result.stdout, f"El Load Balancer en {name_space} no está corriendo. Salida de kubectl:\n{result.stdout}"