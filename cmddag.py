from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'torchx_command_dag',
    default_args=default_args,
    description='A simple DAG to run a torchx command',
)

run_torchx_command = BashOperator(
    task_id='run_torchx_command',
    bash_command='torchx run -s kubernetes -cfg namespace=dolphin-ns,serviceaccount=airflow-sa,queue=dolphin-queu --workspace="" utils.echo --msg lmaohehehehe',
    dag=dag,
)

run_torchx_command