from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
from git_airflowdag.test.A import Aclass #NOICE
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'simple_dag2',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval=None,
)

start = EmptyOperator(
    task_id='start',
    dag=dag,
)

@task
def process_data():
    print("Processing data...")
    Aclass()

end = process_data()

start >> end