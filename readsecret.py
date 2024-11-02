from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from kubernetes import client, config
import logging



@task(task_id='get_k8s_secret')
def get_k8s_secret(secret_name, namespace):
    """Task to get a Kubernetes secret"""
    # Load in-cluster configuration
    config.load_incluster_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Get the secret
    try:
        secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
        secret_data = {k: v.decode('utf-8') for k, v in secret.data.items()}
        logging.info("Secret data: %s", secret_data)
    except client.exceptions.ApiException as e:
        logging.error("Exception when calling CoreV1Api->read_namespaced_secret: %s\n" % e)



# Define the DAG
with DAG(
    dag_id='query_k8s_secret',
    default_args={'owner': 'airflow'},
    schedule_interval=None,
    start_date=days_ago(1),
) as dag:
    get_k8s_secret_task= get_k8s_secret(secret_name='airflowtest', namespace='dolphin-ns')


