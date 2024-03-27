import pytest
import tftest
import subprocess
import os

# Define una ruta al directorio que contiene los archivos de configuración de Terraform
FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Configura la secuencia para desplegar los recursos
@pytest.fixture(scope="module", autouse=True)
def terraform_output():
    tf = tftest.TerraformTest(FIXTURES_DIR)
    tf.setup(workspace_name="test")
    tf.apply(tf_var_file="test-vars.tfvars")
    yield tf.output()
    tf.destroy(tf_var_file="test-vars.tfvars",auto_approve=True)

# Verifica el estado del Load Balancer
def test_load_balancer_status(terraform_output):

    # Define el nombre del clúster
    CLUSTER_NAME = terraform_output['cluster_name']

    # Define la región de AWS
    AWS_REGION = terraform_output['aws_region']

    # Define el perfil
    PROFILE = terraform_output['profile']

    # Define el espacio de trabajo de Istio
    NAME_SPACE = terraform_output['istio_namespace_gateway']

    # Define el nombre del servicio del Load Balancer
    SVC = terraform_output['istio_service_gateway']

    # Ejecuta el comando para actualizar el kubeconfig del clúster de EKS
    update_kubeconfig_cmd = f"aws eks update-kubeconfig --name {CLUSTER_NAME} --region {AWS_REGION} --profile {PROFILE}"
    subprocess.run(update_kubeconfig_cmd, shell=True, check=True)

    # Ejecuta el comando de kubectl para conocer el estado del Load Balancer
    cmd = f"kubectl describe svc {SVC} -n {NAME_SPACE}"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    # Verifica que el estado del Load balancer esté asegurado
    assert "Ensured load balancer" in result.stdout, f"El Load Balancer en {NAME_SPACE} no está corriendo. Salida de kubectl:\n{result.stdout}"

# Verifica la instalación del parche en el Load Balancer
def test_load_balancer_patch(terraform_output):

    # Define el nombre del clúster
    CLUSTER_NAME = terraform_output['cluster_name']

    # Define la región de AWS
    AWS_REGION = terraform_output['aws_region']

    # Define el perfil
    PROFILE = terraform_output['profile']

    # Define el espacio de trabajo de Istio
    NAME_SPACE = terraform_output['istio_namespace_gateway']

    # Define el nombre del servicio del Load Balancer
    SVC = terraform_output['istio_service_gateway']

    # Declara los parámetros que se configuran en el Load Balancer
    backend_protocol = "tcp"
    idle_timeout = "3600"
    internal = "true"
    ssl_cert = terraform_output['lb_ssl_cert']
    ssl_ports = terraform_output['lb_ssl_ports']
    subnets = terraform_output['subnets_id']
    type = "nlb"

    # Ejecuta el comando para actualizar el kubeconfig del clúster de EKS
    update_kubeconfig_cmd = f"aws eks update-kubeconfig --name {CLUSTER_NAME} --region {AWS_REGION} --profile {PROFILE}"
    subprocess.run(update_kubeconfig_cmd, shell=True, check=True)

    # Ejecuta el comando de kubectl para conocer el estado del Load Balancer
    cmd = f"kubectl describe svc {SVC} -n {NAME_SPACE}"
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    # Verifica que el parche se haya aplicado correctamente en los servicios indicados
    assert f"service.beta.kubernetes.io/aws-load-balancer-backend-protocol: {backend_protocol}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: {idle_timeout}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-internal: {internal}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-ssl-cert: {ssl_cert}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-ssl-ports: {ssl_ports}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-subnets: {subnets}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"
    assert f"service.beta.kubernetes.io/aws-load-balancer-type: {type}" in result.stdout, f"El servicio en {NAME_SPACE} no se modificó correctamente. Salida de kubectl:\n{result.stdout}"